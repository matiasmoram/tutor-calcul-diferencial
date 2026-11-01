"""Shared test data for the "troba l'error" context: the reference document and the wiring of the use cases."""

from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise, Verification
from core.mistakes.domain.services.generation_checks import validate_generation
from core.mistakes.domain.values.llm_outputs import GenerationDraft
from core.mistakes.domain.values.mistake_source import ProblemSource, TheorySource
from core.mistakes.infra.llm_mistake_generator import LLMMistakeGenerator
from core.mistakes.infra.llm_mistake_verifier import LLMMistakeVerifier
from core.shared.domain.clock import Clock
from core.shared.llm.client import JsonObject, LLMClient
from tests.fixtures.course import authored_course

COURSE = authored_course()

FRAGS = [
    "Provem camins: amb $y=kx$ el quocient tendeix a $0$.",
    "Com que $x^4 \\ge x^4+y^2$, el quocient està fitat per $|x|$.",
    "Això demostra que el límit existeix.",
    "Pel criteri del sandvitx, $|f|\\le |x|\\to 0$.",
    "Per tant el límit és $0$.",
]
TFRAGS = [
    r"Sigui $f:U\subseteq\mathbb{R}^n\to\mathbb{R}$ diferenciable en un obert $U$.",
    r"Aleshores $f$ és de classe $\mathcal{C}^1$ a $U$.",
    r"Prenem $a\in U$ i una direcció $v$.",
    "Per la definició de diferencial, $D_vf(a)=Df(a)v$.",
    "Com que $v$ és arbitrari, les parcials són contínues.",
]


def gen(errors: list[JsonObject], frags: list[str] = FRAGS) -> JsonObject:
    return {"fragments": frags, "errors": errors}


def err(fragment: int, cita: str) -> JsonObject:
    return {
        "fragment": fragment,
        "cita": cita,
        "tipus": "desigualtat",
        "explicacio": "x",
        "correccio": "y",
        "pista": "z",
    }


def tgen(errors: list[JsonObject], n_enunciat: int = 2, frags: list[str] = TFRAGS) -> JsonObject:
    return {"n_enunciat": n_enunciat, "fragments": frags, "errors": errors}


def terr(fragment: int, cita: str, tipus: str = "hipotesi") -> JsonObject:
    return {"fragment": fragment, "cita": cita, "tipus": tipus, "explicacio": "x", "correccio": "y", "pista": "z"}


def finding(fragment: int, cita: str, gravetat: str = "error", explicacio: str = "") -> JsonObject:
    return {"fragment": fragment, "cita": cita, "gravetat": gravetat, "explicacio": explicacio}


def draft(data: JsonObject) -> GenerationDraft:
    return GenerationDraft.model_validate(data)


def problem_source(exercise_id: str = "t2-4c") -> ProblemSource:
    return ProblemSource.of(COURSE, COURSE.exercise(exercise_id))


def theory_source(item_id: str = "T3.21") -> TheorySource:
    return TheorySource.of(COURSE, COURSE.theory_item(item_id))


def solution(exercise_id: str = "0000000000aa") -> MistakeExercise:
    """The reference document: two errors, in fragments 2 and 3."""
    check = validate_generation(draft(gen([err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")])), 2)
    return MistakeExercise(
        id=exercise_id,
        source_id="t2-4c",
        difficulty="normal",
        fragments=check.fragments,
        mistakes=check.mistakes,
        verification=Verification(origin="test"),
        created_at=1.0,
    )


class FixedClock(Clock):
    def __init__(self, start: float = 1_700_000_000.0) -> None:
        self.t = start

    def now(self) -> float:
        return self.t

    def monotonic(self) -> float:
        return self.t


def exercise_generator(llm: LLMClient, clock: Clock | None = None) -> MistakeExerciseGenerator:
    return MistakeExerciseGenerator(LLMMistakeGenerator(llm), LLMMistakeVerifier(llm), clock or FixedClock())
