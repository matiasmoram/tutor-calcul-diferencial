"""Diagnoses, sessions and wired use cases for the tutoring tests (the LLM is the scripted fake)."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from core.shared.llm.client import JsonObject, LLMClient
from core.shared.storage.session_provider import SQLModelSessionProvider
from core.tutoring.application.photo_transcriber import PhotoTranscriber
from core.tutoring.application.session_browser import SessionBrowser
from core.tutoring.application.session_starter import SessionStarter
from core.tutoring.application.turn_handler import TurnHandler
from core.tutoring.domain.services.policy import decide
from core.tutoring.domain.values.diagnosis import Diagnosis
from core.tutoring.domain.values.plan import Plan
from core.tutoring.domain.values.session_state import SessionState
from core.tutoring.infra.llm_diagnoser import LLMDiagnoser
from core.tutoring.infra.llm_reply_judge import LLMReplyJudge
from core.tutoring.infra.llm_reply_writer import LLMReplyWriter
from core.tutoring.infra.llm_transcriber import LLMTranscriber
from core.tutoring.infra.sqlmodel_repository import SQLModelTutorSessionRepository
from tests.fixtures.course import authored_course

COURSE = authored_course()
EX4C = COURSE.exercise("t2-4c")
OK: JsonObject = {"veredicte": "ok", "infraccions": [], "explicacio": ""}


def diagnosis_json(ex_id: str = "t2-4c", steps: Mapping[str, str] | None = None, **kw: object) -> JsonObject:
    """A diagnosis as the model returns it (Catalan keys); `steps` overrides some step states."""
    ex = COURSE.exercise(ex_id)
    steps = steps or {}
    base: JsonObject = {
        "evidencia": "",
        "resum_alumne": "",
        "estat_passos": [{"pas": s, "estat": steps.get(s, "no_iniciat")} for s in ex.step_ids],
        "pas_actual": ex.step_ids[0],
        "errors_detectats": [],
        "error_altre": "",
        "resultat_proposat": "cap",
        "resultat_justificat": False,
        "nivell_desorientacio": "encallat",
        "intencio": "mostra_treball",
    }
    return base | kw


def diagnosis(ex_id: str = "t2-4c", steps: Mapping[str, str] | None = None, **kw: object) -> Diagnosis:
    return Diagnosis.model_validate(diagnosis_json(ex_id, steps, **kw))


def run_policy(seq: Sequence[Mapping[str, object]], ex_id: str = "t2-4c") -> tuple[list[Plan], SessionState]:
    ex = COURSE.exercise(ex_id)
    state = SessionState()
    plans: list[Plan] = []
    for kw in seq:
        plan, state = decide(ex, diagnosis(ex_id, **kw), state)  # type: ignore[arg-type]
        plans.append(plan)
    return plans, state


@dataclass
class Tutoring:
    sessions: SQLModelTutorSessionRepository
    starter: SessionStarter
    turns: TurnHandler
    transcriber: PhotoTranscriber
    browser: SessionBrowser


def tutoring(llm: LLMClient, provider: SQLModelSessionProvider) -> Tutoring:
    sessions = SQLModelTutorSessionRepository(provider)
    return Tutoring(
        sessions=sessions,
        starter=SessionStarter(COURSE, sessions),
        turns=TurnHandler(COURSE, sessions, LLMDiagnoser(llm, COURSE), LLMReplyWriter(llm), LLMReplyJudge(llm, COURSE)),
        transcriber=PhotoTranscriber(COURSE, sessions, LLMTranscriber(llm)),
        browser=SessionBrowser(sessions),
    )
