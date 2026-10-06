"""One tutor turn: diagnosis -> policy -> reply -> guard (with bounded retries)."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import asdict, dataclass, field

from pydantic import ValidationError

from . import prompts
from .fitxes import Exercici
from .guardia import deterministic_check
from .llm import CallMeta, LLMError, StructuredLLM
from .politica import EstatSessio, Pla, allowed_content, allowed_theory, decide
from .schemas import (
    Diagnosi,
    Resposta,
    VeredicteGuardia,
    diagnosi_schema,
    guardia_schema,
    normalize_diagnosi,
)
from .teoria import ItemTeoria, cited_items, load_teoria

MAX_INTENTS = 3  # first draft + 2 rewrites

FALLBACKS = {
    "tancar": "Molt bé, has arribat al resultat amb una justificació correcta!",
    "despres_de_tancar": "Aquest exercici ja està resolt. Si vols, pots triar-ne un altre de la llista.",
    "redirigir": "Tornem a l'exercici: on t'havies quedat?",
    "demanar_conclusio": "Ja tens totes les peces. Com formularies la conclusió final?",
    "demanar_raonament": "Com hi has arribat? Explica'm el raonament que et porta a aquest resultat.",
    "demanar_intent": "Prova de fer tu el primer càlcul d'aquest pas, encara que no estiguis segur, i ensenya'm què et surt.",
}


@dataclass
class Sessio:
    exercici: Exercici
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    # One turn at a time per session: two tabs (or a retry) must not interleave reads and writes of the state.
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)
    darrer_us: float = field(default_factory=time.time)
    historial: list[dict] = field(default_factory=list)
    estat: EstatSessio = field(default_factory=EstatSessio)
    traces: list[dict] = field(default_factory=list)


def fallback_message(ex: Exercici, pla: Pla, teoria: list[ItemTeoria] = ()) -> str:
    """Safe message built only from authored content, used when every draft is rejected.

    It delivers what the plan promised at its level (objective at 1, idea at 2-3, full step at 4), so the
    hint ladder never records a level the student did not receive. Authored step texts never match a
    regex the plan vetoes (see politica._forbidden_regexes and scripts/check_fitxes.py).
    """
    if pla.accio == "mostrar_conclusio":
        return f"Amb tots els passos resolts, la conclusió és: {ex.resultat.valor.strip()} Ho veus clar?"
    if pla.accio in FALLBACKS:
        return FALLBACKS[pla.accio]
    if pla.accio == "explicar_concepte" and teoria:
        it = teoria[0]
        return f"Mira la {it.etiqueta.split(' (')[0]} del Tema {it.tema} als apunts. Com creus que s'aplica a aquest exercici?"
    if pla.pregunta_suggerida:
        return pla.pregunta_suggerida
    if pla.pas_objectiu:
        p = ex.pas(pla.pas_objectiu)
        if pla.nivell_pista >= 4:
            return f"Aquest pas es fa així: {p.detall.strip()} Com continuaries a partir d'aquí?"
        if pla.nivell_pista >= 2:
            return f"Una idea per avançar: {p.idea.strip()} Com ho aplicaries?"
        return f"Ara l'objectiu és aquest: {p.objectiu.strip()} Com ho començaries?"
    return "Explica'm amb les teves paraules què has fet fins ara i on t'has encallat."


class Tutor:
    def __init__(self, llm: StructuredLLM, teoria: dict[str, ItemTeoria] | None = None):
        self.llm = llm
        self.teoria = teoria if teoria is not None else load_teoria()

    def _diagnose(self, s: Sessio, calls: list[CallMeta]) -> Diagnosi:
        ex = s.exercici
        ids = prompts.diagnosi_teoria_ids(ex, self.teoria)
        data, meta = self.llm.structured(
            "diagnosi",
            prompts.DIAGNOSI_SYSTEM,
            prompts.diagnosi_user(ex, s.estat, s.historial),
            diagnosi_schema(ex, ids),
            context=prompts.diagnosi_context(ex, self.teoria),
        )
        calls.append(meta)
        return normalize_diagnosi(Diagnosi.model_validate(data), ex, ids)

    def _draft(
        self, s: Sessio, pla: Pla, contingut: str, teoria: list[ItemTeoria], feedback: str | None, calls: list[CallMeta]
    ) -> Resposta:
        data, meta = self.llm.structured(
            "resposta",
            prompts.RESPOSTA_SYSTEM,
            prompts.resposta_user(s.exercici, s.historial, pla, contingut, feedback, teoria),
            None,  # plain text: LaTeX-heavy prose survives intact, and small models need no JSON
        )
        calls.append(meta)
        missatge = (data.get("text") or "").strip()
        if not missatge:
            raise LLMError("resposta: empty message")
        # References are the allowed items the message actually cites ("Teorema 12 del Tema 3").
        return Resposta(missatge=missatge, referencies=cited_items(missatge, teoria, s.exercici.tema))

    def _judge(
        self, s: Sessio, pla: Pla, contingut: str, teoria: list[ItemTeoria], r: Resposta, calls: list[CallMeta]
    ) -> VeredicteGuardia:
        data, meta = self.llm.structured(
            "guardia",
            prompts.GUARDIA_SYSTEM,
            prompts.guardia_user(pla, contingut, s.historial, r.missatge, teoria, r.referencies),
            guardia_schema(),
            context=prompts.guardia_context(s.exercici, self.teoria),
        )
        calls.append(meta)
        v = VeredicteGuardia.model_validate(data)
        # A verdict can't be "ok" with listed violations, or "rejected" with none.
        if v.infraccions and v.veredicte == "ok":
            v.veredicte = "rebutjat"
        if not v.infraccions and v.veredicte == "rebutjat":
            v.infraccions = ["no_segueix_l_accio"]
        return v

    def turn(self, s: Sessio, text_alumne: str, origen: str = "text") -> dict:
        estat_previ = s.estat.model_copy(deep=True)
        historial_previ = list(s.historial)
        try:
            return self._turn(s, text_alumne, origen, estat_previ)
        except Exception:
            # The turn is atomic: on any failure the session is exactly as before, and the student can resend.
            s.historial = historial_previ
            s.estat = estat_previ
            raise

    def _turn(self, s: Sessio, text_alumne: str, origen: str, estat_previ: EstatSessio) -> dict:
        t0 = time.perf_counter()
        calls: list[CallMeta] = []
        s.historial.append({"rol": "alumne", "text": text_alumne})

        diag = self._diagnose(s, calls)
        textos_alumne = [m["text"] for m in s.historial if m["rol"] == "alumne"]
        pla, nou_estat = decide(s.exercici, diag, s.estat, textos_alumne)
        contingut = allowed_content(s.exercici, pla, nou_estat.completats, nou_estat.mostrats)
        teoria = allowed_theory(s.exercici, pla, nou_estat.completats, self.teoria)

        # Where the reply may legitimately take formulas from (the sympy guard compares against these).
        permeses = [contingut, s.exercici.enunciat_md(), *[it.enunciat for it in teoria], *textos_alumne]
        intents: list[dict] = []
        final: Resposta | None = None
        feedback: str | None = None
        for _ in range(MAX_INTENTS):
            try:
                draft = self._draft(s, pla, contingut, teoria, feedback, calls)
            except (LLMError, ValidationError) as e:
                intents.append({"missatge": None, "error": str(e)})
                continue
            det = deterministic_check(draft.missatge, pla, permeses)
            intent: dict = {"missatge": draft.missatge, "referencies": draft.referencies, "determinista": det, "llm": None}
            if not det:
                # Only pay for the LLM judge once the cheap checks pass.
                try:
                    v = self._judge(s, pla, contingut, teoria, draft, calls)
                    intent["llm"] = v.model_dump()
                except (LLMError, ValidationError) as e:
                    # Fail closed: an unverified draft never reaches the student.
                    intent["llm"] = {"veredicte": "rebutjat", "infraccions": [], "explicacio": f"guardià no disponible: {e}"}
            intents.append(intent)
            if not det and intent["llm"]["veredicte"] == "ok":
                final = draft
                break
            reasons = det + (intent["llm"]["infraccions"] if intent["llm"] else [])
            if intent["llm"] and intent["llm"]["explicacio"]:
                reasons.append(intent["llm"]["explicacio"])
            feedback = "\n".join(f"- {r}" for r in reasons)

        used_fallback = final is None
        if used_fallback:
            final = Resposta(missatge=fallback_message(s.exercici, pla, teoria), referencies=[])

        s.estat = nou_estat
        s.historial.append({"rol": "tutor", "text": final.missatge})
        trace = {
            "torn": nou_estat.torns,
            "origen": origen,
            "diagnosi": diag.model_dump(),
            "pla": pla.model_dump(),
            "contingut_permes": contingut,
            "teoria_permesa": [it.id for it in teoria],
            "intents": intents,
            "fallback": used_fallback,
            "estat_previ": estat_previ.model_dump(),
            "estat": nou_estat.model_dump(),
            "crides": [asdict(c) for c in calls],
            "latencia_ms": int((time.perf_counter() - t0) * 1000),
        }
        s.traces.append(trace)
        return {
            "missatge": final.missatge,
            "referencies": [self.teoria[i].public() for i in final.referencies],
            "trace": trace,
        }
