"""Simulated-student harness: metrics with a scripted student, tutor and judge (no network)."""

from collections.abc import Sequence

import pytest

from core.course.domain.entities.exercise import Exercise
from core.shared.domain.ids import SessionId
from core.shared.llm.client import CallMeta, JsonObject, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from core.tutoring.application.turn_handler import TurnResult
from core.tutoring.domain.values.chat_message import ChatMessage
from core.tutoring.domain.values.turn_trace import TurnTrace
from tests.core.tutoring.builders import COURSE, OK, diagnosis_json
from tests.fakes.llm import ScriptedLLMClient
from tests.scripts.loader import load_script

sim = load_script("eval/simulate")
EX = COURSE.exercises


# ---------- fakes ----------


class FakeStudent:
    def __init__(self, messages: Sequence[str]) -> None:
        self.messages = list(messages)
        self.views: list[tuple[str, str]] = []

    async def next(self, ex: Exercise, persona: sim.Persona, history: Sequence[ChatMessage]) -> tuple[str, CallMeta]:
        self.views.append(sim.student_prompt(ex, persona, history))
        meta = CallMeta(stage="alumne", model="gpt-5-mini", latency_ms=1, input_tokens=1000, output_tokens=100)
        return self.messages.pop(0), meta


def _state(completats=(), estats=None, mostrats=(), confirmat=False) -> dict[str, object]:
    return {
        "completats": list(completats),
        "estats": estats or {},
        "mostrats": list(mostrats),
        "resultat_confirmat": confirmat,
    }


class FakeTutor:
    """Each scripted turn: (accio, pas, nivell, completats_after, intencio, fallback, n_intents)."""

    def __init__(self, script) -> None:
        self.script = list(script)
        self.completed: dict[SessionId, list[str]] = {}

    async def start(self, exercise_id: str) -> SessionId:
        session_id = SessionId.generate()
        self.completed[session_id] = []
        return session_id

    async def turn(self, session_id: SessionId, text: str) -> TurnResult:
        accio, pas, nivell, completats, intencio, fallback, n_int = self.script.pop(0)
        prev = self.completed[session_id]
        rejected = {"missatge": "x", "referencies": [], "determinista": ["fuita: patró prohibit"], "llm": None}
        approved = {"missatge": "x", "referencies": [], "determinista": [], "llm": OK}
        trace = TurnTrace.model_validate(
            {
                "torn": 1,
                "origen": "text",
                "pla": {
                    "accio": accio,
                    "motiu": "",
                    "pas_objectiu": pas,
                    "nivell_pista": nivell,
                    "pot_dir_resultat": accio == "tancar",
                },
                "diagnosi": diagnosis_json(intencio=intencio, errors_detectats=[]),
                "contingut_permes": "",
                "teoria_permesa": [],
                "intents": [rejected] * (n_int - 1) + [approved],
                "fallback": fallback,
                "estat_previ": _state(prev, dict.fromkeys(prev, "completat")),
                "estat": _state(completats, dict.fromkeys(completats, "completat")),
                "crides": [
                    {
                        "stage": "diagnosis",
                        "model": "gpt-5.4-mini",
                        "input_tokens": 10000,
                        "cached_tokens": 5000,
                        "output_tokens": 500,
                        "latency_ms": 1,
                    }
                ],
                "latencia_ms": 1,
            }
        )
        self.completed[session_id] = list(completats)
        return TurnResult(message=f"tutor {accio}", references=[], trace=trace)


class FakeJudge:
    def __init__(self, verdicts) -> None:
        self.verdicts = list(verdicts)
        self.seen: list[tuple[str, list[str]]] = []

    async def judge(
        self, ex: Exercise, missatge: str, completats: list[str], permes: str = ""
    ) -> tuple[JsonObject, CallMeta]:
        self.seen.append((missatge, list(completats)))
        return self.verdicts.pop(0), CallMeta(stage="jutge", model="gpt-5.4-mini", latency_ms=1)


NO_LEAK = {"revela_resultat_final": False, "passos_revelats": [], "explicacio": ""}
EX1 = EX["t2-4c"]
S0, S1 = EX1.step_ids[0], EX1.step_ids[1]


async def run(student_msgs, tutor_script, verdicts=None, max_torns=10):
    judge = FakeJudge(verdicts or [NO_LEAK] * 20)
    persona = sim.personas_for(EX1, "captaire")[0]
    conv = await sim.run_conversation(
        EX1, persona, FakeTutor(tutor_script), FakeStudent(student_msgs), judge, max_torns
    )
    return conv, judge


# ---------- loops ----------


async def test_loop_detected_when_same_plan_repeats_without_progress():
    conv, _ = await run(
        ["a", "b", "c", "d"],
        [
            ("pista", S0, 1, [], "demana_solucio", False, 1),
            ("pista", S0, 1, [], "demana_solucio", False, 1),  # loop
            ("pista", S0, 1, [], "demana_solucio", False, 1),  # loop
            ("pista", S0, 2, [], "demana_solucio", False, 1),  # level rose: no loop
        ],
        max_torns=4,
    )
    assert conv["metriques"]["loops"] == [2, 3]


async def test_repeat_with_progress_is_not_a_loop():
    conv, _ = await run(
        ["a", "b"],
        [
            ("validar_i_avancar", S1, 1, [S0], "mostra_treball", False, 1),
            ("validar_i_avancar", S1, 1, [S0, "extra"], "mostra_treball", False, 1),  # completed set grew
        ],
        max_torns=2,
    )
    assert conv["metriques"]["loops"] == []


def test_loop_events_ignore_errored_turns():
    torns = [
        {"n": 1, "accio": "pista", "pas_objectiu": "p", "nivell": 1, "progres": False},
        {"n": 2, "alumne": "x", "error": "boom"},
    ]
    assert sim.loop_events(torns) == []


# ---------- completion, ending, counters ----------


async def test_completion_stops_at_tancar_and_counts_turns():
    conv, judge = await run(
        ["a", "b", "c"],
        [
            ("pista", S0, 1, [], "demana_pista", False, 2),
            ("demanar_raonament", S0, 1, [], "proposa_resultat", True, 3),
            ("tancar", None, 0, EX1.step_ids, "proposa_resultat", False, 1),
        ],
    )
    m = conv["metriques"]
    assert m["completat"] and m["torns_fins_tancar"] == 3 and conv["final"] == "tancar"
    assert m["fallbacks"] == 1 and m["drafts"] == 6
    assert m["rebuigs"] == {"fuita": 3}
    assert len(judge.seen) == 2  # the closing turn is not judged
    assert m["cost_tutor_usd"] > 0 and m["cost_simulacio_usd"] > 0


async def test_student_fi_ends_without_completion():
    conv, _ = await run(["a", "[FI]"], [("pista", S0, 1, [], "demana_pista", False, 1)])
    m = conv["metriques"]
    assert conv["final"] == "fi_alumne" and not m["completat"] and m["torns_fins_tancar"] is None and m["torns"] == 1


async def test_max_turns_cap():
    conv, _ = await run(
        ["a"] * 5, [("pista", S0, n, [], "demana_pista", False, 1) for n in (1, 2, 3, 3, 3)], max_torns=3
    )
    assert conv["final"] == "max_torns" and conv["metriques"]["torns"] == 3


async def test_ignored_concept_questions():
    conv, _ = await run(
        ["a", "b", "c"],
        [
            ("explicar_concepte", S0, 0, [], "pregunta_conceptual", False, 1),
            ("pista", S0, 1, [], "pregunta_conceptual", False, 1),  # ignored
            ("pista", S0, 2, [], "demana_pista", False, 1),
        ],
        max_torns=3,
    )
    m = conv["metriques"]
    assert m["preguntes_conceptuals"] == 2 and m["preguntes_ignorades"] == 1


# ---------- leaks ----------


def test_leak_verdict_only_counts_unallowed_content():
    v = {"revela_resultat_final": True, "passos_revelats": ["a", "b"], "explicacio": ""}
    assert sim.leak_verdict(v, ["a"], resultat_permes=False) == {
        "fuga": True,
        "fuga_resultat": True,
        "passos_filtrats": ["b"],
    }
    assert sim.leak_verdict(v, ["a", "b"], resultat_permes=True)["fuga"] is False


async def test_judge_gets_completed_steps_and_leaks_are_recorded():
    leak = {"revela_resultat_final": False, "passos_revelats": [S1], "explicacio": "dona la fita"}
    conv, judge = await run(
        ["a", "b"],
        [
            ("validar_i_avancar", S1, 1, [S0], "mostra_treball", False, 1),
            ("pista", S1, 1, [S0], "demana_pista", False, 1),
        ],
        verdicts=[NO_LEAK, leak],
        max_torns=2,
    )
    assert judge.seen[0][1] == [S0]
    assert conv["metriques"]["fuites"] == [2] and conv["metriques"]["fuites_resultat"] == []


def test_mostrar_pas_target_is_allowed():
    trace = {
        "pla": {"accio": "mostrar_pas", "pas_objectiu": "p2", "pot_dir_resultat": False},
        "estat_previ": _state(["p1"], mostrats=["p0"]),
        "estat": _state(["p1"]),
    }
    assert sim.allowed_for_leaks(trace) == (["p1", "p0", "p2"], False)


def test_judge_schema_is_strict_and_closed_on_step_ids():
    sch = sim.judge_schema(EX1)
    assert sch["additionalProperties"] is False and set(sch["required"]) == set(sch["properties"])
    assert sch["properties"]["passos_revelats"]["items"]["enum"] == EX1.step_ids


# ---------- Wilson ----------


def test_wilson_interval():
    assert sim.wilson(0, 0) == (None, None, None)
    p, lo, hi = sim.wilson(8, 10)
    assert p == 0.8 and lo == pytest.approx(0.4902, abs=1e-3) and hi == pytest.approx(0.9433, abs=1e-3)
    p, lo, hi = sim.wilson(0, 20)
    assert lo == 0.0 and hi == pytest.approx(0.1611, abs=1e-3)
    assert sim.wilson(20, 20)[2] == 1.0


async def test_aggregate_rates():
    conv1, _ = await run(
        ["a", "b"],
        [("pista", S0, 1, [], "demana_pista", False, 1), ("pista", S0, 1, [], "demana_pista", True, 1)],
        max_torns=2,
    )
    conv2, _ = await run(["a"], [("tancar", None, 0, EX1.step_ids, "proposa_resultat", False, 1)])
    a = sim.aggregate([conv1, conv2])
    assert a["completat"]["k"] == 1 and a["completat"]["n"] == 2
    assert a["loops"] == sim._rate(1, 1) and a["fallback"]["k"] == 1 and a["fallback"]["n"] == 3
    assert a["torns_fins_tancar_mitjana"] == 1


# ---------- the student never sees the solution ----------


def _solution_texts(ex: Exercise) -> list[str]:
    texts = [ex.full_reference()]
    for s in ex.steps:
        texts += [s.objective.strip(), s.idea.strip(), s.detail.strip()]
    texts += [m.question.strip() for m in ex.common_mistakes]
    return [t for t in texts if len(t) > 15]


@pytest.mark.parametrize("ex_id", sorted(EX))
def test_student_prompt_never_contains_the_solution(ex_id):
    ex = EX[ex_id]
    personas = [p for spec in [*sim.ARQUETIPS, "errors"] for p in sim.personas_for(ex, spec)]
    history = [ChatMessage.from_student("no sé"), ChatMessage.from_tutor("Què demana l'enunciat?")]
    for persona in personas:
        system, user = sim.student_prompt(ex, persona, history)
        prompt = system + user
        assert ex.statement_md() in prompt
        for t in _solution_texts(ex):
            if t not in ex.statement_md():
                assert t not in prompt, (ex_id, persona.name, t[:60])
        # The result appears only if the statement or the persona's own misconception already says it.
        res = ex.result.value.strip()
        if len(res) > 6 and res not in ex.statement_md() and res not in persona.description:
            assert res not in prompt, (ex_id, persona.name)
        assert "RESULTAT CORRECTE" not in prompt and "PASSOS DE LA SOLUCIÓ" not in prompt


async def test_student_sees_only_the_conversation_with_the_real_tutor_pipeline(
    session_provider: SQLModelSessionProvider,
):
    """End to end with the real use cases over a scripted LLM: what the student is shown is statement + persona + chat."""
    llm = ScriptedLLMClient(
        {
            Stage.DIAGNOSIS: [diagnosis_json(nivell_desorientacio="perdut", intencio="demana_pista")],
            Stage.REPLY: [{"text": "Què passa si t'acostes a l'origen per diferents camins?"}],
            Stage.GUARD: [OK],
        }
    )
    student = FakeStudent(["no sé per on començar", "[FI]"])
    tutor = sim.LocalTutor(COURSE, session_provider, llm)
    conv = await sim.run_conversation(EX1, sim.personas_for(EX1, "perdut")[0], tutor, student, FakeJudge([NO_LEAK]), 5)
    assert conv["final"] == "fi_alumne" and conv["metriques"]["torns"] == 1
    _, user = student.views[1]
    assert "TUTOR: Què passa si t'acostes" in user and EX1.step(S0).detail.strip() not in user


def test_personas_specs():
    assert len(sim.personas_for(EX1, "errors")) == len(EX1.common_mistakes)
    one = sim.personas_for(EX1, "error", seed=3)
    assert len(one) == 1 and one == sim.personas_for(EX1, "error", seed=3) and one[0].archetype == "error"
    m = EX1.common_mistakes[0]
    assert m.description.strip() in sim.personas_for(EX1, f"error:{m.id}")[0].description
    with pytest.raises(ValueError):
        sim.personas_for(EX1, "nope")


def test_stratified_sample_is_seeded_and_balanced():
    a = sim.sample_exercises(EX, 12, seed=1)
    assert a == sim.sample_exercises(EX, 12, seed=1) and len(set(a)) == 12
    topics = [EX[i].topic for i in a]
    assert max(topics.count(t) for t in set(topics)) - min(topics.count(t) for t in set(topics)) <= 1
