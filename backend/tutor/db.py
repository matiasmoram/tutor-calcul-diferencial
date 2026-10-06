"""Persistent storage: everything the app keeps lives in one database, not in process memory or files.

`DATABASE_URL` selects it:
  - production: Supabase Postgres, e.g. `postgresql+psycopg://postgres.<ref>:<password>@<host>:6543/postgres`
  - local/tests (default): SQLite at `data/tutor.db` in the project root.

Tables
  temes, items_teoria, llistes, exercicis   course content (imported from the authoring YAML)
  sessions                                   one row per tutoring / "troba l'error" / quiz session (state + history)
  torns                                      every tutor turn: student text, reply, plan, full trace
  crides_llm                                 LOG of every model call: stage, model, tokens, latency, raw response
  contingut_generat                          generated and verified content ("troba l'error", quizzes)
  correccions, transcripcions                gradings and photo transcriptions
The schema is created here (SQLAlchemy Core) and mirrored in supabase/migrations/ for the hosted database.
"""

from __future__ import annotations

import os
import time
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    create_engine,
    delete,
    func,
    insert,
    select,
    update,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_URL = f"sqlite:///{(ROOT / 'data' / 'tutor.db').as_posix()}"

Json = JSON().with_variant(JSONB(), "postgresql")
meta = MetaData()

temes = Table(
    "temes", meta,
    Column("tema", Integer, primary_key=True),
    Column("titol", Text, nullable=False),
    Column("dades", Json, nullable=False),
)
items_teoria = Table(
    "items_teoria", meta,
    Column("id", String(32), primary_key=True),
    Column("tema", Integer, nullable=False, index=True),
    Column("tipus", String(24), nullable=False),
    Column("num", Integer),
    Column("dades", Json, nullable=False),
)
llistes = Table(
    "llistes", meta,
    Column("id", String(64), primary_key=True),
    Column("dades", Json, nullable=False),
)
exercicis = Table(
    "exercicis", meta,
    Column("id", String(32), primary_key=True),
    Column("llista_id", String(64), ForeignKey("llistes.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("problema", Integer, nullable=False),
    Column("apartat", String(8)),
    Column("dades", Json, nullable=False),
    Column("actualitzat", Float, nullable=False),
)
sessions = Table(
    "sessions", meta,
    Column("id", String(64), primary_key=True),
    Column("tipus", String(24), nullable=False),  # tutor | errades | afirmacions
    Column("font_id", String(64), nullable=False, index=True),  # exercise (or source) id
    Column("creat", Float, nullable=False),
    Column("actualitzat", Float, nullable=False, index=True),
    Column("tancat", Boolean, nullable=False, default=False),
    Column("estat", Json, nullable=False),
    Column("historial", Json, nullable=False),
)
torns = Table(
    "torns", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sessio_id", String(64), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
    Column("n", Integer, nullable=False),
    Column("creat", Float, nullable=False),
    Column("origen", String(16), nullable=False, default="text"),
    Column("alumne", Text, nullable=False),
    Column("tutor", Text, nullable=False),
    Column("accio", String(32)),
    Column("pas", String(64)),
    Column("nivell", Integer),
    Column("fallback", Boolean, nullable=False, default=False),
    Column("latencia_ms", Integer),
    Column("trace", Json, nullable=False),
    Index("ix_torns_sessio_n", "sessio_id", "n"),
)
crides_llm = Table(
    "crides_llm", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sessio_id", String(64), index=True),  # no FK: calls also happen outside sessions (scripts, generation)
    Column("torn", Integer),
    Column("creat", Float, nullable=False, index=True),
    Column("stage", String(32), nullable=False),
    Column("model", String(96), nullable=False),
    Column("latencia_ms", Integer),
    Column("input_tokens", Integer),
    Column("output_tokens", Integer),
    Column("cached_tokens", Integer),
    Column("ok", Boolean, nullable=False),
    Column("error", Text),
    Column("resposta", Json),  # the parsed output, or {"text": ...} in plain-text mode
    Column("system", Text),  # prompts only when TUTOR_LOG_PROMPTS=1 (they are large)
    Column("prompt", Text),
)
contingut_generat = Table(
    "contingut_generat", meta,
    Column("id", String(64), primary_key=True),
    Column("tipus", String(24), nullable=False),  # errades | afirmacions
    Column("font_id", String(64), nullable=False),
    Column("dificultat", String(16), nullable=False),
    Column("creat", Float, nullable=False),
    Column("dades", Json, nullable=False),
    Index("ix_generat_tipus_font", "tipus", "font_id", "dificultat"),
)
correccions = Table(
    "correccions", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sessio_id", String(64), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True),
    Column("creat", Float, nullable=False),
    Column("entrada", Json, nullable=False),
    Column("resultat", Json, nullable=False),
)
transcripcions = Table(
    "transcripcions", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sessio_id", String(64), ForeignKey("sessions.id", ondelete="CASCADE"), index=True),
    Column("creat", Float, nullable=False),
    Column("resultat", Json, nullable=False),
)


# ---------------------------------------------------------------- engine


def url() -> str:
    return os.getenv("DATABASE_URL") or DEFAULT_URL


@lru_cache(maxsize=4)
def _engine(database_url: str) -> Engine:
    if database_url.startswith("sqlite"):
        Path(database_url.removeprefix("sqlite:///")).parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(database_url, connect_args={"check_same_thread": False})
        meta.create_all(engine)  # local: the schema is created on first use
        return engine
    # Hosted Postgres (Supabase): the schema comes from supabase/migrations; pre-ping survives pooler restarts.
    return create_engine(database_url, pool_pre_ping=True, pool_size=5, max_overflow=5)


def engine() -> Engine:
    return _engine(url())


def init(database_url: str | None = None) -> Engine:
    """Create the schema if missing (also on Postgres, for development databases without migrations)."""
    eng = _engine(database_url or url())
    meta.create_all(eng)
    return eng


@contextmanager
def tx() -> Iterator:
    with engine().begin() as conn:
        yield conn


def _upsert(conn, table: Table, key: str, row: dict) -> None:
    exists = conn.execute(select(table.c[key]).where(table.c[key] == row[key])).first()
    if exists:
        conn.execute(update(table).where(table.c[key] == row[key]).values(**row))
    else:
        conn.execute(insert(table).values(**row))


# ---------------------------------------------------------------- content


def import_contingut(llistes_data: dict, exercicis_data: dict, teoria_data: dict, temes_data: list[dict]) -> dict:
    """Replace the course content with the given models (fitxes.Llista / Exercici, teoria.ItemTeoria)."""
    now = time.time()
    with tx() as c:
        c.execute(delete(exercicis))
        c.execute(delete(llistes))
        c.execute(delete(items_teoria))
        c.execute(delete(temes))
        for t in temes_data:
            c.execute(insert(temes).values(tema=t["tema"], titol=t["titol"], dades=t))
        for it in teoria_data.values():
            c.execute(insert(items_teoria).values(id=it.id, tema=it.tema, tipus=it.tipus, num=it.num, dades=it.model_dump()))
        for l in llistes_data.values():
            c.execute(insert(llistes).values(id=l.id, dades=l.model_dump()))
        for ex in exercicis_data.values():
            c.execute(insert(exercicis).values(id=ex.id, llista_id=ex.llista, problema=ex.problema, apartat=ex.apartat,
                                               dades=ex.model_dump(), actualitzat=now))
    return {"temes": len(temes_data), "items_teoria": len(teoria_data), "llistes": len(llistes_data),
            "exercicis": len(exercicis_data)}


def load_contingut() -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """Raw rows (temes, theory items, lists, exercises) for the loaders to validate into models."""
    with tx() as c:
        return (
            [r.dades for r in c.execute(select(temes.c.dades).order_by(temes.c.tema))],
            [r.dades for r in c.execute(select(items_teoria.c.dades))],
            [r.dades for r in c.execute(select(llistes.c.dades))],
            [r.dades for r in c.execute(select(exercicis.c.dades))],
        )


def compta_contingut() -> int:
    with tx() as c:
        return c.execute(select(func.count()).select_from(exercicis)).scalar_one()


# ---------------------------------------------------------------- sessions and turns


def desa_sessio(sessio_id: str, tipus: str, font_id: str, estat: dict, historial: list, tancat: bool = False) -> None:
    now = time.time()
    with tx() as c:
        exists = c.execute(select(sessions.c.creat).where(sessions.c.id == sessio_id)).first()
        if exists:
            c.execute(update(sessions).where(sessions.c.id == sessio_id)
                      .values(estat=estat, historial=historial, tancat=tancat, actualitzat=now))
        else:
            c.execute(insert(sessions).values(id=sessio_id, tipus=tipus, font_id=font_id, creat=now, actualitzat=now,
                                              tancat=tancat, estat=estat, historial=historial))


def carrega_sessio(sessio_id: str) -> dict | None:
    with tx() as c:
        r = c.execute(select(sessions).where(sessions.c.id == sessio_id)).mappings().first()
        return dict(r) if r else None


def afegeix_torn(sessio_id: str, n: int, alumne: str, tutor: str, trace: dict, origen: str = "text") -> None:
    pla = trace.get("pla") or {}
    with tx() as c:
        c.execute(insert(torns).values(
            sessio_id=sessio_id, n=n, creat=time.time(), origen=origen, alumne=alumne, tutor=tutor,
            accio=pla.get("accio"), pas=pla.get("pas_objectiu"), nivell=pla.get("nivell_pista"),
            fallback=bool(trace.get("fallback")), latencia_ms=trace.get("latencia_ms"), trace=trace,
        ))


def torns_de(sessio_id: str) -> list[dict]:
    with tx() as c:
        return [dict(r) for r in c.execute(select(torns).where(torns.c.sessio_id == sessio_id).order_by(torns.c.n)).mappings()]


def _flags(rows: list[dict]) -> dict:
    plans = [(r["accio"], r["pas"], r["nivell"]) for r in rows]
    loops = sum(1 for a, b in zip(plans, plans[1:]) if a == b and a[0] not in ("despres_de_tancar", "redirigir"))
    return {
        "torns": len(rows),
        "tancat": any(p[0] in ("tancar", "mostrar_conclusio") for p in plans),
        "fallbacks": sum(1 for r in rows if r["fallback"]),
        "rebutjos_guardia": sum(max(0, len(r["trace"].get("intents") or []) - 1) for r in rows),
        "bucles": loops,
        "mostrar_pas": sum(1 for p in plans if p[0] == "mostrar_pas"),
        "frustracio": sum(1 for r in rows if (r["trace"].get("diagnosi") or {}).get("intencio") == "frustracio"),
    }


def llista_sessions(tipus: str = "tutor", limit: int = 200) -> list[dict]:
    """Sessions for the professor review page, most recent first, with the flags worth a look."""
    with tx() as c:
        ss = c.execute(select(sessions).where(sessions.c.tipus == tipus)
                       .order_by(sessions.c.actualitzat.desc()).limit(limit)).mappings().all()
        out = []
        for s in ss:
            rows = [dict(r) for r in c.execute(select(torns).where(torns.c.sessio_id == s["id"]).order_by(torns.c.n)).mappings()]
            if rows:
                out.append({"id": s["id"], "exercici": s["font_id"], "inici": s["creat"], "darrer": s["actualitzat"]}
                           | _flags(rows))
        return out


def esborra_sessions_antigues(abans_de: float) -> int:
    with tx() as c:
        return c.execute(delete(sessions).where(sessions.c.actualitzat < abans_de)).rowcount or 0


# ---------------------------------------------------------------- LLM call log

# Who is calling: set by the request handlers so every model call is filed under its session and turn.
CONTEXT: ContextVar[dict] = ContextVar("tutor_db_context", default={})


@contextmanager
def context(**kw) -> Iterator[None]:
    token = CONTEXT.set(CONTEXT.get() | kw)
    try:
        yield
    finally:
        CONTEXT.reset(token)


def registra_crida(stage: str, model: str, *, ok: bool, meta=None, resposta: Any = None, error: str | None = None,
                   system: str | None = None, prompt: str | None = None) -> None:
    ctx = CONTEXT.get()
    keep_prompts = os.getenv("TUTOR_LOG_PROMPTS") == "1"
    with tx() as c:
        c.execute(insert(crides_llm).values(
            sessio_id=ctx.get("sessio_id"), torn=ctx.get("torn"), creat=time.time(), stage=stage, model=model,
            latencia_ms=getattr(meta, "latency_ms", None), input_tokens=getattr(meta, "input_tokens", None),
            output_tokens=getattr(meta, "output_tokens", None), cached_tokens=getattr(meta, "cached_tokens", None),
            ok=ok, error=error, resposta=resposta,
            system=system if keep_prompts else None, prompt=prompt if keep_prompts else None,
        ))


def crides_de(sessio_id: str | None = None, limit: int = 500) -> list[dict]:
    q = select(crides_llm).order_by(crides_llm.c.id.desc()).limit(limit)
    if sessio_id:
        q = q.where(crides_llm.c.sessio_id == sessio_id)
    with tx() as c:
        return [dict(r) for r in c.execute(q).mappings()]


class LoggingLLM:
    """Wraps any StructuredLLM and records every call (success or failure) in `crides_llm`.

    Logging never breaks a turn: a storage error is swallowed after the model call has been made.
    """

    def __init__(self, inner):
        self.inner = inner

    def __getattr__(self, name):
        return getattr(self.inner, name)

    def structured(self, stage: str, system: str, user: str, schema: dict | None, image=None, context: str | None = None):
        prompt = f"{context}\n\n{user}" if context else user
        try:
            data, meta = self.inner.structured(stage, system, user, schema, image=image, context=context)
        except Exception as e:
            _safe(registra_crida, stage, _model_of(self.inner, stage), ok=False, error=f"{type(e).__name__}: {e}"[:2000],
                  system=system, prompt=prompt)
            raise
        _safe(registra_crida, stage, meta.model, ok=True, meta=meta, resposta=data, system=system, prompt=prompt)
        return data, meta


def _model_of(llm, stage: str) -> str:
    try:
        return llm.stages[stage].model
    except Exception:
        return "?"


def _safe(fn, *a, **kw) -> None:
    try:
        fn(*a, **kw)
    except Exception:  # noqa: BLE001 — the log must never take the tutor down
        import logging

        logging.getLogger("tutor.db").exception("could not store an LLM call")


# ---------------------------------------------------------------- generated content and gradings


def desa_generat(tipus: str, item_id: str, font_id: str, dificultat: str, dades: dict) -> None:
    with tx() as c:
        _upsert(c, contingut_generat, "id", {"id": item_id, "tipus": tipus, "font_id": font_id, "dificultat": dificultat,
                                             "creat": time.time(), "dades": dades})


def generats(tipus: str, font_id: str | None = None, dificultat: str | None = None) -> list[dict]:
    q = select(contingut_generat.c.dades).where(contingut_generat.c.tipus == tipus)
    if font_id:
        q = q.where(contingut_generat.c.font_id == font_id)
    if dificultat:
        q = q.where(contingut_generat.c.dificultat == dificultat)
    with tx() as c:
        return [r.dades for r in c.execute(q.order_by(contingut_generat.c.creat))]


def recompte_generats(tipus: str) -> dict[str, dict[str, int]]:
    q = (select(contingut_generat.c.font_id, contingut_generat.c.dificultat, func.count())
         .where(contingut_generat.c.tipus == tipus).group_by(contingut_generat.c.font_id, contingut_generat.c.dificultat))
    out: dict[str, dict[str, int]] = {}
    with tx() as c:
        for font_id, dif, n in c.execute(q):
            out.setdefault(font_id, {})[dif] = n
    return out


def afegeix_correccio(sessio_id: str, entrada: Any, resultat: Any) -> None:
    with tx() as c:
        c.execute(insert(correccions).values(sessio_id=sessio_id, creat=time.time(), entrada=entrada, resultat=resultat))


def afegeix_transcripcio(sessio_id: str | None, resultat: Any) -> None:
    with tx() as c:
        c.execute(insert(transcripcions).values(sessio_id=sessio_id, creat=time.time(), resultat=resultat))


def nou_id() -> str:
    return uuid.uuid4().hex
