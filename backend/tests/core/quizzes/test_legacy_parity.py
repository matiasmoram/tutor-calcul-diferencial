"""TEMPORARY (phases 2-5 of work/ARQUITECTURA.md): the quizzes context behaves exactly as tutor/afirmacions.py.

Same prompts and schemas, same requests for the same scripted model outputs, the same quiz and the same grading.
Deleted together with backend/tutor in phase 6."""

import copy
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import pytest

from core.quizzes.domain.entities.grading import Answer
from core.quizzes.domain.entities.quiz import Quiz
from core.quizzes.domain.sources import focus_items, quiz_source
from core.quizzes.infra import llm_schemas, prompts
from core.quizzes.infra.json_quiz_files import JsonQuizFiles
from core.shared.llm.client import JsonObject, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from settings import BACKEND_DIR
from tests.core.quizzes.builders import (
    ITERATED,
    QUIZ_ID,
    answers_grader,
    check,
    generator,
    grader,
    idea,
    item,
    ok_audit,
    ok_solver,
    transcriber,
)
from tests.fakes.llm import ScriptedLLMClient
from tests.fixtures.course import authored_course
from tutor import afirmacions as af
from tutor.llm import LLMError

COURSE = authored_course()
PREGENERATED = BACKEND_DIR / "generats" / "afirmacions"
OLD_STAGES: Mapping[Stage, str] = {
    Stage.QUIZ_GENERATION: "afirmacions_generacio",
    Stage.QUIZ_VERIFICATION: "afirmacions_verificacio",
    Stage.QUIZ_AUDIT: "afirmacions_auditoria",
    Stage.QUIZ_GRADING: "afirmacions_correccio",
    Stage.QUIZ_EXTRACTION: "afirmacions_extraccio",
}


@dataclass
class _OldMeta:
    model: str = "scripted"
    latency_ms: int = 1
    input_tokens: int = 10
    output_tokens: int = 2
    cached_tokens: int = 0


class OldScriptedLLM:
    """The legacy StructuredLLM interface, replaying the same outputs as ScriptedLLMClient."""

    def __init__(self, script: Mapping[Stage, Sequence[JsonObject]]) -> None:
        self.script = {OLD_STAGES[s]: list(v) for s, v in copy.deepcopy(dict(script)).items()}
        self.seen: list[tuple[str, str, str, object, str | None]] = []

    def structured(self, stage, system, user, schema, image=None, context=None):
        self.seen.append((stage, system, user, schema, context))
        if not self.script.get(stage):
            raise LLMError(f"{stage}: script exhausted")
        return self.script[stage].pop(0), _OldMeta()


def _same_requests(old: OldScriptedLLM, new: ScriptedLLMClient) -> None:
    for stage, name in OLD_STAGES.items():
        old_calls = [(s, u, sc, c) for st, s, u, sc, c in old.seen if st == name]
        new_calls = [(r.system, r.user, r.schema, r.context) for r in new.requests[stage]]
        if stage in (Stage.QUIZ_VERIFICATION, Stage.QUIZ_AUDIT, Stage.QUIZ_GRADING, Stage.QUIZ_EXTRACTION):
            old_calls, new_calls = sorted(old_calls, key=repr), sorted(new_calls, key=repr)
        assert new_calls == old_calls, stage


# ---------- prompts, schemas, sources ----------


def test_same_prompts_and_schemas() -> None:
    assert prompts.GENERATION_SYSTEM == af.GENERACIO_SYSTEM
    assert prompts.SOLVER_SYSTEM == af.SOLUCIONADOR_SYSTEM
    assert prompts.AUDIT_SYSTEM == af.AUDITORIA_SYSTEM
    assert prompts.EXTRACTION_SYSTEM == af.EXTRACCIO_SYSTEM
    assert prompts.GRADING_SYSTEM == af.CORRECCIO_SYSTEM
    refs = af.Font(2).refs_permeses()
    assert llm_schemas.generation_schema(refs) == af.generacio_schema(refs)
    assert llm_schemas.solver_schema() == af.solucionador_schema()
    assert llm_schemas.audit_schema() == af.auditoria_schema()
    assert llm_schemas.STUDENT_CHECK_SCHEMA == af.CHECK_ALUMNE_SCHEMA
    assert llm_schemas.grading_schema(["a1", "a3"]) == af.correccio_schema(["a1", "a3"])
    assert llm_schemas.extraction_schema(["a2"]) == af.extraccio_schema(["a2"])


def test_same_sources_with_the_same_context(monkeypatch: pytest.MonkeyPatch) -> None:
    topics = af.load_temes()
    monkeypatch.setattr(af, "load_temes", lambda: topics)  # the legacy loader re-reads the YAML on every call
    assert [it.id for it in focus_items(COURSE)] == [it.id for it in af.items_focus()]
    ids = [f"tema-{n}" for n in range(1, 7)] + [it.id for it in af.items_focus()]
    for source_id in ids:
        old, new = af.font_de(source_id), quiz_source(COURSE, source_id)
        assert (new.id, new.topic) == (old.id, old.tema), source_id
        assert list(new.allowed_refs) == old.refs_permeses(), source_id
        assert prompts.source_context(new) == old.context(), source_id


# ---------- generation ----------


def _replacement_script() -> dict[Stage, list[JsonObject]]:
    bad_check = check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0")
    round1 = [
        item("F1 $a$.", checks=[ITERATED]),
        item("F2.", checks=[check("no_limit", "sin(1/y)", variable="y")]),
        item("F3.", checks=[bad_check]),
        item("C1.", "cert", teoria=["T2.12", "T2.12", "T1.1"]),
        item("C2.", "cert"),
        item("F2 ", contraexemple="x"),  # duplicate of F2
        item("ignored beyond k + 2"),
    ]
    round2 = [item("F4.", pista="És fals?"), item("F5.  "), item("C3.", "cert"), item("C4.", "cert")]
    round3 = [item("F6.")]
    return {
        Stage.QUIZ_GENERATION: [{"afirmacions": round1}, {"afirmacions": round2}, {"afirmacions": round3}],
        Stage.QUIZ_VERIFICATION: [
            ok_solver(["fals", "fals", "cert", "fals"]),
            {"respostes": [{"num": 1, "veredicte": "fals", "confianca": "baixa", "ben_plantejada": True,
                            "justificacio": "no ho sé"}, *ok_solver(["fals", "cert", "cert"])["respostes"][1:]]},
            ok_solver(["fals"]),
        ],
        Stage.QUIZ_AUDIT: [ok_audit(4), ok_audit(3), ok_audit(1)],
    }  # fmt: skip


def _focus_script() -> dict[Stage, list[JsonObject]]:
    return {
        Stage.QUIZ_GENERATION: [
            {"afirmacions": [item(f"F{i}.") for i in range(3)] + [item("C1.", "cert"), item("C2.", "cert")]},
            {"afirmacions": [item("C3.", "cert"), item("F9."), item("F10.")]},
        ],
        Stage.QUIZ_VERIFICATION: [ok_solver(["fals"] * 3 + ["cert", "cert"]), ok_solver(["cert", "fals", "fals"])],
        Stage.QUIZ_AUDIT: [
            ok_audit(5),
            {"revisions": [*ok_audit(3)["revisions"][:2], {"num": 3, "resolucio_correcta": True,
                                                            "teoria_correcta": False, "pista_neutra": True,
                                                            "problemes": "cita malament"}]},
        ],
    }  # fmt: skip


def _comparable(doc: Mapping[str, object]) -> dict[str, object]:
    """The quiz without what depends on the clock and the shuffle (ids) or on the fake's call metadata."""
    statements = doc["afirmacions"]
    assert isinstance(statements, list)
    verification = doc["verificacio"]
    assert isinstance(verification, dict)
    rounds = [
        {k: v for k, v in r.items() if k not in ("generacio", "solucionador", "auditoria")}
        | {"verified": "solucionador" in r}
        for r in verification["rondes"]
    ]
    return {
        "font": doc["font"],
        "tema": doc["tema"],
        "dificultat": doc["dificultat"],
        "afirmacions": sorted(({k: v for k, v in s.items() if k != "id"} for s in statements), key=repr),
        "rondes": rounds,
    }


@pytest.mark.parametrize(
    ("source_id", "difficulty", "script"),
    [("tema-2", "facil", _replacement_script()), ("T2.12", "facil", _focus_script())],
)
async def test_generation_gives_the_same_quiz(source_id: str, difficulty: str, script: dict) -> None:
    old_llm = OldScriptedLLM(script)
    old_quiz, _ = af.generate(old_llm, af.font_de(source_id), difficulty, en_proces=True)  # type: ignore[arg-type]
    new_llm = ScriptedLLMClient(copy.deepcopy(script))
    new_quiz = await generator(new_llm).generate(quiz_source(COURSE, source_id), difficulty)  # type: ignore[arg-type]
    _same_requests(old_llm, new_llm)
    assert _comparable(new_quiz.model_dump(mode="json")) == _comparable(json.loads(old_quiz.model_dump_json()))
    old_ids = sorted(a.id for a in old_quiz.afirmacions)
    assert sorted(s.id for s in new_quiz.statements) == old_ids


async def test_generation_gives_up_at_the_same_round() -> None:
    script: dict[Stage, list[JsonObject]] = {
        Stage.QUIZ_GENERATION: [{"afirmacions": [item(f"X{i}.", contraexemple="") for i in range(5)]}] * 10
    }
    old_llm = OldScriptedLLM(script)
    with pytest.raises(LLMError) as old_error:
        af.generate(old_llm, af.Font(2), "normal", en_proces=True)
    new_llm = ScriptedLLMClient(copy.deepcopy(script))
    with pytest.raises(Exception) as new_error:
        await generator(new_llm).generate(quiz_source(COURSE, "tema-2"), "normal")
    assert str(new_error.value) == str(old_error.value)
    _same_requests(old_llm, new_llm)


# ---------- grading ----------


def _old_quiz() -> af.Questionari:
    def a(aid: str, text: str, verdict: str, counterexample: str = "", ideas: list[str] | None = None) -> af.Afirmacio:
        return af.Afirmacio(id=aid, enunciat=text, veredicte=verdict, concepte="c",  # type: ignore[arg-type]
                            trampa="reciproc", contraexemple=counterexample, resolucio="r",
                            idees_clau=ideas or ["i"], pista="p", teoria=["T2.12"],
                            comprovacions=[af.Comprovacio(**ITERATED, estat="ok", calculat="m/(m**2 + 1)")])  # fmt: skip

    return af.Questionari(
        id=QUIZ_ID,
        font="tema-2",
        tema=2,
        dificultat="facil",
        afirmacions=[
            a("a1", "A.", "fals", "xy"),
            a("a2", "B.", "cert", ideas=["contrarecíproc", "els dos iterats valdrien L", "contradicció"]),
            a("a3", "C.", "fals", "z"),
            a("a4", "D.", "cert"),
        ],
    )


PARABOLA = "x**2*(x**2)/(x**4+(x**2)**2)"
GRADING_CASES: list[tuple[list[dict[str, str]], set[str], dict[Stage, list[JsonObject]]]] = [
    (
        [
            {"id": "a1", "veredicte": "fals", "justificacio": "sobre $y=mx$ dona $0$"},
            {"id": "a2", "veredicte": "fals", "justificacio": "no"},
            {"id": "a3", "veredicte": "fals", "justificacio": "Està bé."},
            {"id": "a4", "veredicte": "", "justificacio": ""},
            {"id": "a9", "veredicte": "cert", "justificacio": "no existeix"},
        ],
        {"a3", "a4"},
        {
            Stage.QUIZ_GRADING: [grader(
                {"id": "a1", "idees": [idea(1, "sobre $y=mx$")], "justificacio": "correcta", "feedback": "f1"},
                {"id": "a2", "idees": [idea(1, "no")], "justificacio": "correcta", "feedback": "f2"},
                {"id": "a3", "idees": [idea(1, "Està bé"), idea(2, "Està bé")], "justificacio": "parcial",
                 "feedback": "f3"},
                summary="Bé",
            )],
            Stage.QUIZ_EXTRACTION: [transcriber(
                a1=[check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0") | {"cita_alumne": "sobre $y=mx$ dona $0$"}],
            )],
        },
    ),
    (
        [
            {"id": "a1", "veredicte": "fals", "justificacio": r"$\frac{x^2y}{x^4+y^2}$: sobre $y = x^2$ el límit és $1$."},
            {"id": "a3", "veredicte": "fals", "justificacio": "Sobre les rectes dona 0."},
            {"id": "a2", "veredicte": "cert", "justificacio": "Per la proposició 12."},
        ],
        set(),
        {
            Stage.QUIZ_GRADING: [grader(
                {"id": "a1", "idees": [idea(1, "sobre $y = x^2$")], "justificacio": "correcta", "feedback": ""},
                {"id": "a3", "idees": [idea(1, "Sobre les rectes")], "justificacio": "inventada", "feedback": ""},
                {"id": "a2", "idees": [idea(1, "Per la proposició 12"), idea(2, "Per la proposició 12"),
                                       idea(3, "per tant contradicció"), idea(7, "Per la")],
                 "justificacio": "correcta", "feedback": "x"},
            )],
            Stage.QUIZ_EXTRACTION: [transcriber(
                a1=[
                    check("limit", PARABOLA, "1") | {"cita_alumne": "sobre $y = x^2$ el límit és $1$"},
                    check("limit", PARABOLA, "1/2") | {"cita_alumne": "sobre $y = x^2$ el límit és $1$"},
                ],
                a3=[check("limit", "x", "0") | {"cita_alumne": "sobre y=x^2 el límit és 1"}],
                a2=[check("no_limit", "sin(1/x)") | {"cita_alumne": "Per la proposició"}],
            )],
        },
    ),
    ([], {"a1"}, {}),
]  # fmt: skip


@pytest.mark.parametrize(("answers", "hints", "script"), GRADING_CASES)
async def test_grading_gives_the_same_result(
    answers: list[dict[str, str]],
    hints: set[str],
    script: dict[Stage, list[JsonObject]],
    session_provider: SQLModelSessionProvider,
) -> None:
    old_quiz = _old_quiz()
    old_llm = OldScriptedLLM(script)
    old = af.grade(old_llm, af.Font(2), old_quiz, [af.Resposta(**a) for a in answers], hints, en_proces=True)  # type: ignore[arg-type]

    new_llm = ScriptedLLMClient(copy.deepcopy(script))
    new_quiz = Quiz.model_validate_json(old_quiz.model_dump_json())
    result = await answers_grader(new_llm, session_provider).grade_answers(
        quiz_source(COURSE, "tema-2"), new_quiz, [Answer.model_validate(a) for a in answers], hints
    )
    new = result.model_dump(mode="json")
    _same_requests(old_llm, new_llm)
    old_call, new_call = old.pop("crida"), new.pop("crida")
    assert (old_call is None) == (new_call is None)
    assert new == json.loads(json.dumps(old))


# ---------- pre-generated quizzes ----------

FILES = sorted(PREGENERATED.glob("*/*/*.json"))


@pytest.mark.parametrize("path", FILES, ids=lambda p: "/".join(p.parts[-3:]))
def test_every_pregenerated_quiz_loads_and_keeps_its_document(path: Path) -> None:
    raw = json.loads(path.read_text(encoding="utf-8"))
    new = Quiz.model_validate(raw)
    assert new.model_dump(mode="json") == raw
    old = af.Questionari.model_validate(raw)
    assert json.loads(new.model_dump_json()) == json.loads(old.model_dump_json())
    assert (new.source_id, new.difficulty) == (path.parent.parent.name, path.parent.name)


def test_the_json_source_reads_what_the_legacy_cache_reads() -> None:
    assert FILES, "no pre-generated quizzes"
    loaded = JsonQuizFiles(PREGENERATED).load_all()
    legacy = [q for d in sorted({(p.parent.parent.name, p.parent.name) for p in FILES}) for q in af.cached(*d)]
    assert sorted(q.id for q in loaded) == sorted(q.id for q in legacy)
    assert {(q.source_id, q.difficulty): 0 for q in loaded}.keys() == {
        (s, d): 0 for s, ds in af.disponibles().items() for d in ds
    }.keys()
