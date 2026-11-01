"""Shared test data for the "troba l'error" context: the legacy test documents and the wiring of the use cases."""

import random

from core.mistakes.application.mistake_exercise_generator import MistakeExerciseGenerator
from core.mistakes.application.parted_mistake_exercise_generator import PartedMistakeExerciseGenerator
from core.mistakes.domain.entities.mistake_exercise import MistakeExercise, Verification
from core.mistakes.domain.entities.parted_mistake_exercise import MistakePart, PartedMistakeExercise
from core.mistakes.domain.services.generation_checks import validate_generation
from core.mistakes.domain.services.part_checks import check_corruption, check_resolution
from core.mistakes.domain.values.difficulty import Difficulty
from core.mistakes.domain.values.llm_outputs import CorruptionDraft, GenerationDraft, ResolutionDraft
from core.mistakes.domain.values.mistake_source import ProblemSource, TheorySource
from core.mistakes.domain.values.resolution import Resolution
from core.mistakes.infra.llm_mistake_generator import LLMMistakeGenerator
from core.mistakes.infra.llm_mistake_verifier import LLMMistakeVerifier
from core.mistakes.infra.llm_part_corrupter import LLMPartCorrupter
from core.mistakes.infra.llm_part_verifier import LLMPartVerifier
from core.mistakes.infra.llm_resolution_verifier import LLMResolutionVerifier
from core.mistakes.infra.llm_resolution_writer import LLMResolutionWriter
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
    """The legacy tests' document: two errors, in fragments 2 and 3."""
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


# The per-parts test resolution of t2-4c (steps candidat, acotar, concloure), correct, two fragments per part.
PARTS: list[tuple[str, list[str]]] = [
    ("candidat", ["Provem camins: amb $y=kx$ el quocient tendeix a $0$.", "El candidat a límit és $0$."]),
    ("acotar", ["Com que $x^4 \\le x^4+y^2$, el quocient està fitat per $|x|$.", "Per tant $|f(x,y)|\\le |x|$."]),
    ("concloure", ["Pel criteri del sandvitx, $|f|\\le |x|\\to 0$.", "Per tant el límit és $0$."]),
]
THEORY_STATEMENT = [r"Sigui $f:U\subseteq\mathbb{R}^n\to\mathbb{R}$ de classe $\mathcal{C}^1$ en un obert $U$."]
THEORY_PARTS: list[tuple[str, list[str]]] = [
    ("Derivades direccionals", [r"Prenem $a\in U$ i una direcció $v$.", "Per la definició, $D_vf(a)=Df(a)v$."]),
    ("Conclusió", ["Com que $v$ és arbitrari, $f$ és diferenciable."]),
]


def written(parts: list[tuple[str, list[str]]] = PARTS) -> JsonObject:
    """Stage A's answer for a problem."""
    return {"parts": [{"pas": step, "fragments": fragments} for step, fragments in parts]}


def theory_written(
    statement: list[str] = THEORY_STATEMENT, parts: list[tuple[str, list[str]]] = THEORY_PARTS
) -> JsonObject:
    return {"enunciat": statement, "parts": [{"titol": t, "fragments": f} for t, f in parts]}


def resolution_checked(ok: bool = True, *problems: JsonObject) -> JsonObject:
    """The blind check of the correct resolution."""
    return {"problemes": list(problems), "valoracio": "ok", "arriba_al_resultat": ok}


def edit(fragment: int, original: str, nou: str) -> JsonObject:
    return {"fragment": fragment, "original": original, "nou": nou}


def corruption(
    edits: list[JsonObject], cita: str, tipus: str = "desigualtat", apte: bool = True, pista: str = "z"
) -> JsonObject:
    """Stage B's answer."""
    return {
        "apte": apte,
        "canvis": edits,
        "cita": cita,
        "tipus": tipus,
        "explicacio": "x",
        "correccio": "y",
        "pista": pista,
    }


# The errors of the test documents: part 2 gets a reversed inequality, part 3 a wrong limit; part 1, when chosen, a
# wrong candidate.
PART1_ERROR = corruption([edit(1, "tendeix a $0$", "tendeix a $1$")], "tendeix a $1$", tipus="calcul")
PART2_ERROR = corruption([edit(1, "x^4 \\le", "x^4 \\ge")], "$x^4 \\ge x^4+y^2$", pista="pista 2")
PART3_ERROR = corruption([edit(2, "és $0$", "és $1$")], "el límit és $1$", tipus="calcul", pista="pista 3")


def part_checked(*problems: JsonObject, context_ok: bool = True, alert: str = "") -> JsonObject:
    """The blind check of one corrupted part."""
    return {"problemes": list(problems), "valoracio": "", "context_correcte": context_ok, "alerta_context": alert}


def resolution(parts: list[tuple[str, list[str]]] = PARTS) -> Resolution:
    check = check_resolution(ResolutionDraft.model_validate(written(parts)), problem_source())
    assert check.valid, check.problems
    return check.resolution


def parted(
    exercise_id: str = "0000000000bb", errors: dict[int, JsonObject] | None = None, difficulty: Difficulty = "normal"
) -> PartedMistakeExercise:
    """The per-parts test document: by default, errors in parts 2 and 3."""
    clean = resolution()
    errors = {2: PART2_ERROR, 3: PART3_ERROR} if errors is None else errors
    parts: list[MistakePart] = []
    for i, p in enumerate(clean.parts, 1):
        if i not in errors:
            parts.append(MistakePart(title=p.title, step=p.step, fragments=p.fragments))
            continue
        draft = CorruptionDraft.model_validate(errors[i])
        mistake_id = f"e{sum(1 for q in parts if q.mistake is not None) + 1}"
        check = check_corruption(p.fragments, draft, clean.first_fragment(i), mistake_id, False)
        assert check.valid, check.problems
        parts.append(
            MistakePart(
                title=p.title,
                step=p.step,
                fragments=p.fragments,
                flawed_fragments=check.flawed_fragments,
                mistake=check.mistake,
                verification=Verification(origin="test"),
            )
        )
    return PartedMistakeExercise(
        id=exercise_id,
        source_id="t2-4c",
        difficulty=difficulty,
        parts=parts,
        verification=Verification(origin="test"),
        created_at=1.0,
    )


def theory_parted() -> PartedMistakeExercise:
    """The per-parts test document read as theory: part 1 is the statement (2 fragments), so it has an error."""
    data = parted(errors={1: PART1_ERROR, 3: PART3_ERROR}).model_dump(mode="json")
    return PartedMistakeExercise.model_validate(data | {"font": "teoria", "exercici": "T3.21", "n_enunciat": 2})


class FixedClock(Clock):
    def __init__(self, start: float = 1_700_000_000.0) -> None:
        self.t = start

    def now(self) -> float:
        return self.t

    def monotonic(self) -> float:
        return self.t


def exercise_generator(llm: LLMClient, clock: Clock | None = None) -> MistakeExerciseGenerator:
    return MistakeExerciseGenerator(LLMMistakeGenerator(llm), LLMMistakeVerifier(llm), clock or FixedClock())


def seed_choosing(*first: int, n_parts: int = 3) -> int:
    """A seed for `parted_generator` whose choice of a problem's parts starts with `first`, in that order: the parts
    to corrupt, then the unused ones a failing part is swapped for."""
    for seed in range(1000):
        parts = list(range(1, n_parts + 1))
        random.Random(seed).shuffle(parts)
        if parts[: len(first)] == list(first):
            return seed
    raise AssertionError(f"no seed starts with {first}")


def parted_generator(
    llm: LLMClient, clock: Clock | None = None, seed: int = 0, deadline_s: float = 300.0
) -> PartedMistakeExerciseGenerator:
    return PartedMistakeExerciseGenerator(
        LLMResolutionWriter(llm),
        LLMResolutionVerifier(llm),
        LLMPartCorrupter(llm),
        LLMPartVerifier(llm),
        clock or FixedClock(),
        random.Random(seed),
        deadline_s,
    )
