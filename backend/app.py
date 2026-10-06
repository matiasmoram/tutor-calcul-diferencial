"""FastAPI server: exercise list, tutoring sessions, static frontend."""

from __future__ import annotations

import base64
import binascii
import os
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Literal
from pathlib import Path

import anthropic
import openai
from google.genai import errors as genai_errors
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ValidationError

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

from tutor.fitxes import load_llistes  # noqa: E402
from tutor.llm import LLMError, default_stage_configs, make_llm, provider  # noqa: E402
from tutor.pipeline import Sessio, Tutor  # noqa: E402
from tutor.teoria import PDF_PROBLEMES, SOURCES_DIR, load_temes, load_teoria, parse_ref, pdf_url  # noqa: E402
from tutor.transcripcio import ImatgeInvalida, transcribe, validate_image  # noqa: E402
from tutor import afirmacions, db, errades  # noqa: E402
from tutor.politica import EstatSessio  # noqa: E402

FRONTEND = ROOT / "frontend"

app = FastAPI(title="Tutor socràtic — Càlcul Diferencial")
TEORIA = load_teoria()
# Fails at startup if a sheet cites a theory item that doesn't exist.
LLISTES, EXERCICIS = load_llistes(teoria=TEORIA)
SESSIONS: dict[str, Sessio] = {}  # hot cache; the database (tutor/db.py) is the source of truth


def _persist(fn, *a, **kw) -> None:
    """Storage failures are logged, never shown to the student: the tutor keeps working without the database."""
    db._safe(fn, *a, **kw)


def _sync_db() -> None:
    """On startup: load the course content into an empty database and mirror the generated-content caches."""
    db.init()
    if db.compta_contingut() == 0:
        db.import_contingut(LLISTES, EXERCICIS, TEORIA, load_temes())
    for tipus, mod in (("errades", errades), ("afirmacions", afirmacions)):
        for path in Path(mod.CACHE_DIR).glob("*/*/*.json"):
            dades = __import__("json").loads(path.read_text(encoding="utf-8"))
            db.desa_generat(tipus, f"{tipus}:{dades.get('id', path.stem)}", path.parent.parent.name, path.parent.name, dades)


_persist(_sync_db)
KEY_VARS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}
_tutor: Tutor | None = None


def tutor() -> Tutor:
    global _tutor
    if _tutor is None:
        # Every model call (tutor, transcription, generation, grading) is recorded in the crides_llm table.
        _tutor = Tutor(db.LoggingLLM(make_llm()), TEORIA)
    return _tutor


class NovaSessio(BaseModel):
    exercici_id: str


class Missatge(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    origen: Literal["text", "foto"] = "text"


class Foto(BaseModel):
    imatge: str = Field(max_length=9_000_000, description="data:image/...;base64,...")


@app.get("/api/llistes")
def llistes() -> list[dict]:
    return [l.public() for l in LLISTES.values()]


@app.get("/api/llistes/{llista_id}")
def llista(llista_id: str) -> dict:
    l = LLISTES.get(llista_id)
    if l is None:
        raise HTTPException(404, "Llista desconeguda")
    return l.public() | {
        "exercicis": [EXERCICIS[e].public() for e in l.exercicis],
        "problemes": [p.model_dump() for p in l.problemes],
    }


@app.get("/api/teoria")
def teoria_index() -> dict:
    """Every numbered item of the notes, grouped by tema, with a link to its page in the PDF."""
    items = [it.index_entry() for it in TEORIA.values()]
    return {
        "temes": [t | {"items": [i for i in items if i["tema"] == t["tema"]]} for t in load_temes()],
        "problemes_pdf": pdf_url(PDF_PROBLEMES),
    }


@app.get("/api/teoria/{item_id}")
def teoria_item(item_id: str) -> dict:
    it = TEORIA.get(item_id)
    if it is None:
        raise HTTPException(404, "Ítem de teoria desconegut")
    return it.public()


def es_professor(request: Request) -> bool:
    """With TUTOR_CLAU_PROFESSOR set, only requests carrying that key see solutions and traces.
    Without it the app runs in demo mode (everything visible), as before."""
    clau = os.getenv("TUTOR_CLAU_PROFESSOR")
    return not clau or request.headers.get("X-Clau-Professor") == clau


@app.get("/api/config")
def config(request: Request) -> dict:
    return {
        "panell_professor": es_professor(request),
        "provider": provider(),
        "api_key": bool(os.getenv(KEY_VARS[provider()])),
        "stages": {k: vars(v) for k, v in default_stage_configs().items()},
    }


SESSION_TTL_S = 6 * 3600  # in-memory sessions idle for longer are dropped


def _evict_idle() -> None:
    limit = time.time() - SESSION_TTL_S
    for sid in [k for k, s in SESSIONS.items() if s.darrer_us < limit]:
        SESSIONS.pop(sid, None)


@app.post("/api/sessions")
def nova_sessio(body: NovaSessio, request: Request) -> dict:
    ex = EXERCICIS.get(body.exercici_id)
    if ex is None:
        raise HTTPException(404, "Exercici desconegut")
    _evict_idle()
    s = Sessio(exercici=ex)
    SESSIONS[s.id] = s
    _persist(db.desa_sessio, s.id, "tutor", ex.id, s.estat.model_dump(), s.historial)
    out = {
        "session_id": s.id,
        "exercici": ex.public(),
        "llista": LLISTES[ex.llista].public(),
        # Background theory the student may read from the start (never the items that solve the exercise).
        "teoria": [TEORIA[i].public() for i in _background_ids(ex)],
    }
    if es_professor(request):
        out |= {
            "passos": [{"id": p.id, "titol": p.titol} for p in ex.passos],
            "nota_professor": ex.nota_professor,
            "resultat": ex.resultat.valor,
            # Professor panel: every item the sheet cites, with where it is used.
            "teoria_fitxa": _sheet_theory(ex),
        }
    return out


def _background_ids(ex) -> list[str]:
    reserved = ex.reserved_ids(TEORIA)
    ids = [parse_ref(r)[0] for r in ex.teoria]
    return [i for i in dict.fromkeys(ids) if i in TEORIA and i not in reserved]


def _sheet_theory(ex) -> list[dict]:
    reserved = ex.reserved_ids(TEORIA)
    used: dict[str, list[str]] = {}
    for r in ex.teoria:
        used.setdefault(parse_ref(r)[0], []).append("enunciat")
    for p in ex.passos:
        for r in p.teoria:
            used.setdefault(parse_ref(r)[0], []).append(p.id)
    for r in ex.teoria_reservada:
        used.setdefault(parse_ref(r)[0], [])
    for i in reserved:
        used.setdefault(i, [])
    return [
        {"id": i, "etiqueta": TEORIA[i].etiqueta, "nom": TEORIA[i].nom, "on": on, "reservada": i in reserved}
        for i, on in used.items()
        if i in TEORIA
    ]


def _session(session_id: str) -> Sessio:
    s = SESSIONS.get(session_id) or _rehydrate(session_id)
    if s is None:
        raise HTTPException(404, "Sessió desconeguda")
    s.darrer_us = time.time()
    key_var = KEY_VARS[provider()]
    if not os.getenv(key_var):
        raise HTTPException(503, f"Falta la clau d'API: posa {key_var} al fitxer .env i reinicia el servidor.")
    return s


def _rehydrate(session_id: str) -> Sessio | None:
    """A session evicted from memory (or from before a restart) is rebuilt from the database."""
    try:
        row = db.carrega_sessio(session_id)
    except Exception:  # noqa: BLE001 — no database: behave as before (unknown session)
        return None
    if not row or row["tipus"] != "tutor" or row["font_id"] not in EXERCICIS:
        return None
    s = Sessio(exercici=EXERCICIS[row["font_id"]], id=session_id, historial=list(row["historial"]),
               estat=EstatSessio(**row["estat"]))
    SESSIONS[s.id] = s
    return s


def _call_llm(fn, what: str):
    """Run an LLM-backed action, mapping provider errors to clear HTTP errors."""
    try:
        return fn()
    except anthropic.AuthenticationError:
        raise HTTPException(401, "Clau d'API d'Anthropic invàlida o absent (ANTHROPIC_API_KEY al fitxer .env).")
    except anthropic.RateLimitError:
        raise HTTPException(429, "Límit de peticions de l'API. Torna-ho a provar en uns segons.")
    except anthropic.APIStatusError as e:
        raise HTTPException(502, f"Error de l'API ({e.status_code}): {e.message}")
    except anthropic.APIConnectionError:
        raise HTTPException(502, "No s'ha pogut connectar amb l'API d'Anthropic.")
    except anthropic.AnthropicError as e:
        raise HTTPException(500, f"Configuració del client d'Anthropic: {e}")
    except openai.RateLimitError as e:
        raise HTTPException(429, f"Límit de l'API d'OpenAI: {e.message}")
    except openai.APIStatusError as e:
        raise HTTPException(502, f"Error de l'API d'OpenAI ({e.status_code}): {e.message}")
    except openai.APIConnectionError:
        raise HTTPException(502, "No s'ha pogut connectar amb l'API d'OpenAI.")
    except genai_errors.APIError as e:
        raise HTTPException(502 if e.code != 429 else 429, f"Error de l'API de Gemini ({e.code}): {e.message}")
    except (LLMError, ValidationError) as e:
        raise HTTPException(502, f"{what} ha fallat: {e}")


@app.post("/api/sessions/{session_id}/missatges")
def enviar(session_id: str, body: Missatge, request: Request) -> dict:
    s = _session(session_id)
    if not s.lock.acquire(blocking=False):
        raise HTTPException(409, "Encara s'està responent el missatge anterior.")
    try:
        with db.context(sessio_id=s.id, torn=s.estat.torns + 1):
            out = _call_llm(lambda: tutor().turn(s, body.text.strip(), origen=body.origen), "La diagnosi")
        _persist(db.desa_sessio, s.id, "tutor", s.exercici.id, s.estat.model_dump(), s.historial, s.estat.tancat)
        _persist(db.afegeix_torn, s.id, s.estat.torns, body.text.strip(), out["missatge"], out["trace"], body.origen)
    finally:
        s.lock.release()
    if not es_professor(request):
        # The trace holds the allowed content and rejected drafts: students only get the reply.
        out = {"missatge": out["missatge"], "referencies": out["referencies"], "trace": {"fallback": out["trace"]["fallback"]}}
    return out


@app.get("/api/professor/sessions")
def professor_sessions(request: Request) -> list[dict]:
    if not es_professor(request):
        raise HTTPException(403, "Només per al professorat.")
    return db.llista_sessions("tutor")


@app.get("/api/professor/sessions/{session_id}")
def professor_sessio(session_id: str, request: Request) -> list[dict]:
    if not es_professor(request):
        raise HTTPException(403, "Només per al professorat.")
    torns = db.torns_de(session_id)
    if not torns:
        raise HTTPException(404, "Sessió desconeguda")
    exercici = (db.carrega_sessio(session_id) or {}).get("font_id", "")
    return [{"t": t["creat"], "exercici": exercici, "alumne": t["alumne"], "tutor": t["tutor"], "trace": t["trace"]}
            for t in torns]


@app.post("/api/sessions/{session_id}/transcripcio")
def transcriure(session_id: str, body: Foto) -> dict:
    s = _session(session_id)
    try:
        header, b64 = body.imatge.split(",", 1)
        media_type = header.removeprefix("data:").removesuffix(";base64")
        if not header.endswith(";base64"):
            raise ValueError
        image = validate_image(base64.b64decode(b64, validate=True), media_type)
    except ImatgeInvalida as e:
        raise HTTPException(400, str(e))
    except (ValueError, binascii.Error):
        raise HTTPException(400, "La imatge no és un data URL base64 vàlid.")
    with db.context(sessio_id=s.id):
        t, meta = _call_llm(lambda: transcribe(tutor().llm, s.exercici, image), "La transcripció")
    _persist(db.afegeix_transcripcio, s.id, t.model_dump())
    return t.model_dump() | {"crida": asdict(meta)}


class NovaErrada(BaseModel):
    # Exactly one source: an exercise of the collection ("resolució dolenta") or a result of the notes.
    exercici_id: str | None = None
    teoria_id: str | None = None
    dificultat: errades.Dificultat = "normal"
    nova: bool = False
    excepte: str | None = Field(default=None, max_length=40)  # document just seen: prefer another one


class Correccio(BaseModel):
    anotacions: list[errades.Anotacio] = Field(max_length=40)


@dataclass
class SessioErrada:
    font: errades.FontProblema | errades.FontTeoria
    sol: errades.SolucioAmbErrors
    resultat: dict | None = None
    darrer_us: float = field(default_factory=time.time)
    lock: threading.Lock = field(default_factory=threading.Lock)


ERRADES_SESSIONS: dict[str, SessioErrada] = {}
ITEMS_ERRADES = {it.id: it for it in errades.items_teoria(TEORIA)}


def _key_or_503() -> None:
    key_var = KEY_VARS[provider()]
    if not os.getenv(key_var):
        raise HTTPException(503, f"Falta la clau d'API: posa {key_var} al fitxer .env i reinicia el servidor.")


def _font(body: NovaErrada) -> errades.FontProblema | errades.FontTeoria:
    if bool(body.exercici_id) == bool(body.teoria_id):
        raise HTTPException(422, "Cal indicar un exercici o un resultat dels apunts (només un).")
    if body.exercici_id:
        ex = EXERCICIS.get(body.exercici_id)
        if ex is None:
            raise HTTPException(404, "Exercici desconegut")
        return errades.FontProblema(ex)
    it = ITEMS_ERRADES.get(body.teoria_id)
    if it is None:
        raise HTTPException(404, "Resultat dels apunts desconegut o sense demostració")
    return errades.FontTeoria(it)


@app.get("/api/errades/teoria")
def errades_teoria() -> dict:
    """Results of the notes available for the theory activity, by tema, with the ready documents per difficulty."""
    ready = errades.disponibles()
    items = [it.index_entry() | {"disponibles": ready.get(it.id, {})} for it in ITEMS_ERRADES.values()]
    return {"temes": [t | {"items": [i for i in items if i["tema"] == t["tema"]]} for t in load_temes()]}


@app.get("/api/errades/disponibles")
def errades_disponibles() -> dict:
    """{source id: {difficulty: n}} of documents ready without calling the API."""
    return errades.disponibles()


@app.post("/api/errades/sessions")
def nova_errada(body: NovaErrada) -> dict:
    font = _font(body)
    if body.nova or not errades.cached(font.id, body.dificultat):
        _key_or_503()
    sid = uuid.uuid4().hex
    with db.context(sessio_id=sid):
        sol, fresh = _call_llm(
            lambda: errades.get_or_generate(tutor().llm, font, body.dificultat, body.nova, excepte=body.excepte),
            "La generació",
        )
    limit = time.time() - SESSION_TTL_S
    for k in [k for k, s in ERRADES_SESSIONS.items() if s.darrer_us < limit]:
        ERRADES_SESSIONS.pop(k, None)
    ERRADES_SESSIONS[sid] = SessioErrada(font, sol)
    if fresh:
        _persist(db.desa_generat, "errades", f"errades:{sol.id}", font.id, body.dificultat, sol.model_dump())
    _persist(db.desa_sessio, sid, "errades", font.id, {"solucio": sol.id, "dificultat": body.dificultat}, [])
    out = {"session_id": sid, "font": font.tipus, "solucio": sol.public(), "generada_ara": fresh}
    if isinstance(font, errades.FontProblema):
        out |= {"exercici": font.ex.public(), "llista": LLISTES[font.ex.llista].public()}
    else:
        # Only the label: the statement of the notes is the answer key until the correction.
        out |= {"teoria": font.item.index_entry()}
    return out


@app.post("/api/errades/sessions/{session_id}/correccio")
def corregir(session_id: str, body: Correccio) -> dict:
    s = ERRADES_SESSIONS.get(session_id)
    if s is None:
        raise HTTPException(404, "Sessió desconeguda")
    if not s.lock.acquire(blocking=False):
        raise HTTPException(409, "Ja s'està corregint aquest document.")
    try:
        # One correction per document: the result reveals every error, so resubmitting would be free points.
        if s.resultat is None:
            _key_or_503()
            with db.context(sessio_id=session_id):
                s.resultat = _call_llm(lambda: errades.grade(tutor().llm, s.font, s.sol, body.anotacions), "La correcció")
            if isinstance(s.font, errades.FontTeoria):
                s.resultat["original"] = s.font.item.public()
            _persist(db.afegeix_correccio, session_id, body.model_dump(), s.resultat)
        s.darrer_us = time.time()
        return s.resultat
    finally:
        s.lock.release()


class NouQuestionari(BaseModel):
    font: str = Field(max_length=20)  # "tema-2" or a result of the notes ("T2.12") as the focus
    dificultat: afirmacions.Dificultat = "normal"
    nova: bool = False
    excepte: str | None = Field(default=None, max_length=40)


class Respostes(BaseModel):
    respostes: list[afirmacions.Resposta] = Field(max_length=20)


@dataclass
class SessioAfirmacions:
    font: afirmacions.Font
    q: afirmacions.Questionari
    pistes: set[str] = field(default_factory=set)
    resultat: dict | None = None
    darrer_us: float = field(default_factory=time.time)
    lock: threading.Lock = field(default_factory=threading.Lock)


AFIRMACIONS_SESSIONS: dict[str, SessioAfirmacions] = {}


def _sessio_afirmacions(session_id: str) -> SessioAfirmacions:
    s = AFIRMACIONS_SESSIONS.get(session_id)
    if s is None:
        raise HTTPException(404, "Sessió desconeguda")
    s.darrer_us = time.time()
    return s


@app.get("/api/afirmacions/fonts")
def afirmacions_fonts() -> dict:
    """Temes (whole-tema quizzes) and the results of the notes that can be the focus, with ready quizzes."""
    ready = afirmacions.disponibles()
    items = [it.index_entry() | {"disponibles": ready.get(it.id, {})} for it in afirmacions.items_focus(TEORIA)]
    return {
        "temes": [
            t | {"id": f"tema-{t['tema']}", "disponibles": ready.get(f"tema-{t['tema']}", {}),
                 "items": [i for i in items if i["tema"] == t["tema"]]}
            for t in load_temes()
        ],
        "mida": afirmacions.N_AFIRMACIONS,
    }


@app.post("/api/afirmacions/sessions")
def nou_questionari(body: NouQuestionari) -> dict:
    try:
        font = afirmacions.font_de(body.font)
    except KeyError:
        raise HTTPException(404, "Tema o resultat dels apunts desconegut")
    if body.nova or not afirmacions.cached(font.id, body.dificultat):
        _key_or_503()
    sid = uuid.uuid4().hex
    with db.context(sessio_id=sid):
        q, fresh = _call_llm(
            lambda: afirmacions.get_or_generate(tutor().llm, font, body.dificultat, body.nova, excepte=body.excepte),
            "La generació",
        )
    limit = time.time() - SESSION_TTL_S
    for k in [k for k, s in AFIRMACIONS_SESSIONS.items() if s.darrer_us < limit]:
        AFIRMACIONS_SESSIONS.pop(k, None)
    AFIRMACIONS_SESSIONS[sid] = SessioAfirmacions(font, q)
    if fresh:
        _persist(db.desa_generat, "afirmacions", f"afirmacions:{q.id}", font.id, body.dificultat, q.model_dump())
    _persist(db.desa_sessio, sid, "afirmacions", font.id, {"questionari": q.id, "dificultat": body.dificultat}, [])
    return {
        "session_id": sid,
        "questionari": q.public(),
        "generat_ara": fresh,
        "focus": font.focus.index_entry() if font.focus else None,
    }


@app.post("/api/afirmacions/sessions/{session_id}/pista/{afirmacio_id}")
def afirmacio_pista(session_id: str, afirmacio_id: str) -> dict:
    """Hints are served one at a time and recorded: a used hint lowers that statement's score."""
    s = _sessio_afirmacions(session_id)
    a = s.q.afirmacio(afirmacio_id)
    if a is None:
        raise HTTPException(404, "Afirmació desconeguda")
    if s.resultat is None:
        s.pistes.add(a.id)
    return {"id": a.id, "pista": a.pista}


@app.post("/api/afirmacions/sessions/{session_id}/correccio")
def corregir_afirmacions(session_id: str, body: Respostes) -> dict:
    s = _sessio_afirmacions(session_id)
    if not s.lock.acquire(blocking=False):
        raise HTTPException(409, "Ja s'està corregint aquest qüestionari.")
    try:
        # One correction per quiz: the result reveals every verdict and solution.
        if s.resultat is None:
            if any(r.veredicte for r in body.respostes):
                _key_or_503()
            with db.context(sessio_id=session_id):
                s.resultat = _call_llm(
                    lambda: afirmacions.grade(tutor().llm, s.font, s.q, body.respostes, s.pistes), "La correcció"
                )
            refs = {r for it in s.q.afirmacions for r in it.teoria}
            s.resultat["teoria"] = {i: TEORIA[i].public() for i in refs if i in TEORIA}
            _persist(db.afegeix_correccio, session_id, body.model_dump() | {"pistes": sorted(s.pistes)}, s.resultat)
        return s.resultat
    finally:
        s.lock.release()


@app.get("/")
def index() -> FileResponse:
    # Always revalidate the shell page so new asset versions (?v=N) are picked up.
    return FileResponse(FRONTEND / "index.html", headers={"Cache-Control": "no-cache"})


app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
# Course PDFs (theory notes and problem collection): citations in the chat open them at the cited page.
app.mount("/pdf", StaticFiles(directory=SOURCES_DIR), name="pdf")
