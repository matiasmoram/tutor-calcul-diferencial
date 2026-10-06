"""TEMPORARY (phases 3-5 of work/ARQUITECTURA.md): the new tutor decides, says and sends exactly what the old one did.

Deleted together with backend/tutor in phase 6."""

import random
from collections.abc import Mapping, Sequence

import pytest

from core.shared.llm.client import JsonObject, LLMError, Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from core.tutoring.application.turn_handler import TurnInput
from core.tutoring.domain.fallback import fallback_message
from core.tutoring.domain.policy import allowed_content, allowed_theory, decide
from core.tutoring.domain.theory_access import background_theory, concept_question_ids, sheet_theory
from core.tutoring.domain.values.diagnosis import Diagnosis
from core.tutoring.domain.values.session_state import SessionState
from core.tutoring.infra import prompts as new_prompts
from core.tutoring.infra.llm_schemas import diagnosis_schema, guard_schema, transcription_schema
from tests.core.tutoring.builders import COURSE, OK, diagnosis_json, tutoring
from tests.core.tutoring.policy_fuzzer import PROFILES, diagnosis_sequence
from tests.fakes.llm import ScriptedLLMClient
from tutor import llm as old_llm
from tutor import pipeline as old_pipeline
from tutor import prompts as old_prompts
from tutor import transcripcio as old_transcription
from tutor.fitxes import load_llistes
from tutor.politica import INSTRUCCIONS, NIVELLS_DESCRIPCIO, EstatSessio
from tutor.politica import allowed_content as old_allowed_content
from tutor.politica import allowed_theory as old_allowed_theory
from tutor.politica import decide as old_decide
from tutor.schemas import Diagnosi, diagnosi_schema, guardia_schema, normalize_diagnosi
from tutor.teoria import load_teoria

OLD_THEORY = load_teoria()
_, OLD_EXERCISES = load_llistes(teoria=OLD_THEORY)
OLD_STAGES = {"diagnosi": Stage.DIAGNOSIS, "resposta": Stage.REPLY, "guardia": Stage.GUARD}
STUDENT_TEXTS = ["(missatge de l'alumne)", "per camins dona 0, per tant el límit és 0"]


def _with_concept_question(data: JsonObject, concept_ids: Sequence[str], rng: random.Random) -> JsonObject:
    """The fuzzer never asks about theory: pick items (allowed or not) so the concept gate is exercised too."""
    if data["intencio"] != "pregunta_conceptual" or not concept_ids:
        return data
    return data | {"teoria_pregunta": rng.sample([*concept_ids, "T6.999"], k=min(3, len(concept_ids)))}


# ---------- (a) the policy over the fuzzer's inputs, on every exercise ----------


@pytest.mark.parametrize("ex_id", sorted(COURSE.exercises))
def test_policy_decides_exactly_like_the_legacy_one(ex_id: str) -> None:
    ex, old_ex = COURSE.exercise(ex_id), OLD_EXERCISES[ex_id]
    concept_ids = concept_question_ids(COURSE, ex)
    assert concept_ids == old_prompts.diagnosi_teoria_ids(old_ex, OLD_THEORY)
    for profile, seeds in zip(PROFILES, (4, 1, 1), strict=True):
        for seed in range(seeds):
            rng = random.Random(seed)
            state, old_state = SessionState(), EstatSessio()
            for data in diagnosis_sequence(ex, seed, 14, profile):
                data = _with_concept_question(data, concept_ids, rng)
                d = Diagnosis.model_validate(data).normalized(ex.step_ids, concept_ids)
                old_d = normalize_diagnosi(Diagnosi.model_validate(data), old_ex, concept_ids)
                assert d.model_dump() == old_d.model_dump()

                plan, state = decide(ex, d, state, STUDENT_TEXTS)
                old_plan, old_state = old_decide(old_ex, old_d, old_state, STUDENT_TEXTS)
                where = (ex_id, profile, seed, state.turns)
                assert plan.model_dump() == old_plan.model_dump(), where
                assert state.model_dump() == old_state.model_dump(), where

                content = allowed_content(ex, plan, state.completed, state.shown)
                assert content == old_allowed_content(old_ex, old_plan, old_state.completats, old_state.mostrats)
                theory = allowed_theory(COURSE, ex, plan, state.completed)
                old_theory = old_allowed_theory(old_ex, old_plan, old_state.completats, OLD_THEORY)
                assert [it.id for it in theory] == [it.id for it in old_theory], where
                assert fallback_message(ex, plan, theory) == old_pipeline.fallback_message(old_ex, old_plan, old_theory)


@pytest.mark.parametrize("ex_id", sorted(COURSE.exercises)[::7])
def test_session_theory_and_prompts_match_the_legacy_ones(ex_id: str) -> None:
    ex, old_ex = COURSE.exercise(ex_id), OLD_EXERCISES[ex_id]
    reserved = old_ex.reserved_ids(OLD_THEORY)
    old_background = [
        i for i in dict.fromkeys(r.split("+")[0] for r in old_ex.teoria) if i in OLD_THEORY and i not in reserved
    ]
    assert [it.id for it in background_theory(COURSE, ex)] == old_background
    assert {u.item.id: (u.used_in, u.reserved) for u in sheet_theory(COURSE, ex)} == {
        i: (on, i in reserved) for i, on in _old_sheet_theory(old_ex, reserved).items()
    }
    assert new_prompts.diagnosis_context(COURSE, ex) == old_prompts.diagnosi_context(old_ex, OLD_THEORY)
    assert new_prompts.guard_context(COURSE, ex) == old_prompts.guardia_context(old_ex, OLD_THEORY)
    ids = concept_question_ids(COURSE, ex)
    assert diagnosis_schema(ex, ids) == diagnosi_schema(old_ex, list(ids))
    assert new_prompts.transcription_user(ex) in _old_transcription_user(old_ex)


def _old_sheet_theory(old_ex, reserved: set[str]) -> dict[str, list[str]]:
    used: dict[str, list[str]] = {}
    for r in old_ex.teoria:
        used.setdefault(r.split("+")[0], []).append("enunciat")
    for p in old_ex.passos:
        for r in p.teoria:
            used.setdefault(r.split("+")[0], []).append(p.id)
    for r in old_ex.teoria_reservada:
        used.setdefault(r.split("+")[0], [])
    for i in reserved:
        used.setdefault(i, [])
    return {i: on for i, on in used.items() if i in OLD_THEORY}


def _old_transcription_user(old_ex) -> str:
    return f"<enunciat>\n{old_ex.enunciat_md()}\n</enunciat>\n\nTranscriu el treball de l'alumne que apareix a la foto."


def test_fixed_prompts_and_schemas_are_the_legacy_ones() -> None:
    assert new_prompts.DIAGNOSIS_SYSTEM == old_prompts.DIAGNOSI_SYSTEM
    assert new_prompts.REPLY_SYSTEM == old_prompts.RESPOSTA_SYSTEM
    assert new_prompts.GUARD_SYSTEM == old_prompts.GUARDIA_SYSTEM
    assert new_prompts.TRANSCRIPTION_SYSTEM == old_transcription.TRANSCRIPCIO_SYSTEM
    assert guard_schema() == guardia_schema()
    assert transcription_schema() == old_transcription.transcripcio_schema()
    assert dict(new_prompts.INSTRUCTIONS) == INSTRUCCIONS
    assert dict(new_prompts.LEVEL_DESCRIPTIONS) == NIVELLS_DESCRIPCIO


# ---------- (b) whole turns: same scripted model outputs, same replies, traces and prompts ----------

type Script = dict[str, list[JsonObject | str]]  # per legacy stage; a str is an LLMError with that message


class LegacyScriptedLLM:
    def __init__(self, script: Script) -> None:
        self.script = {k: list(v) for k, v in script.items()}
        self.requests: list[tuple[str, str, str, dict | None, str | None]] = []

    def structured(self, stage, system, user, schema, image=None, context=None):
        self.requests.append((stage, system, user, schema, context))
        out = self.script[stage].pop(0)
        if isinstance(out, str):
            raise old_llm.LLMError(out)
        return out, old_llm.CallMeta(stage=stage, model="scripted", latency_ms=1)


def _new_llm(script: Script) -> ScriptedLLMClient:
    return ScriptedLLMClient(
        {OLD_STAGES[k]: [LLMError(o) if isinstance(o, str) else o for o in v] for k, v in script.items()}
    )


REJECTED: JsonObject = {"veredicte": "rebutjat", "infraccions": ["revela_pas_futur"], "explicacio": "avança la fita"}


def _scenarios() -> list[tuple[str, str, list[str], Script]]:
    ex = COURSE.exercise("t2-4c")
    background = ex.theory[0].item_id
    item = COURSE.theory_item(background)
    cite = f"Recorda la {item.label.split(' (')[0]} del Tema {item.topic} i el Teorema 4 del Tema 6. Com ho aplicaries?"
    out = [
        (
            "t2-4c a full session",
            "t2-4c",
            ["no sé per on començar", "He provat y=kx i dona 0", "Què vol dir que existeixi el límit?", "Ja ho tinc"],
            {
                "diagnosi": [
                    diagnosis_json(intencio="demana_pista", nivell_desorientacio="perdut"),
                    diagnosis_json(steps={"candidat": "completat"}, nivell_desorientacio="en_cami"),
                    diagnosis_json(
                        steps={"candidat": "completat"}, intencio="pregunta_conceptual", teoria_pregunta=[background]
                    ),
                    diagnosis_json(
                        steps=dict.fromkeys(ex.step_ids, "completat"),
                        resultat_proposat="correcte",
                        resultat_justificat=True,
                        intencio="proposa_resultat",
                        nivell_desorientacio="en_cami",
                    ),
                ],
                "resposta": [
                    {"text": "Què passa si t'acostes a l'origen per diferents camins?"},
                    {"text": r"El límit és 0 perquè $\le |x|$. Ho veus?"},
                    {"text": "Bona feina. Com podries fitar el quocient per una cosa que tendeixi a 0?"},
                    {"text": cite},
                    {"text": "Molt bé, ho has justificat."},
                ],
                "guardia": [OK, OK, OK, OK],
            },
        ),
        (
            "t2-4c mistakes, failures and fallbacks",
            "t2-4c",
            ["dona 0 per tots els camins", "doncs és 0 per camins", "no sé"],
            {
                "diagnosi": [
                    diagnosis_json(errors_detectats=["camins_com_a_prova"], intencio="proposa_resultat"),
                    diagnosis_json(errors_detectats=["camins_com_a_prova"], intencio="proposa_resultat"),
                    diagnosis_json(intencio="frustracio", nivell_desorientacio="perdut"),
                ],
                "resposta": [
                    "resposta: output truncated",
                    {"text": "Pensa-hi, d'acord?"},
                    {"text": ""},
                    {"text": "Pensa-hi, d'acord?"},
                    {"text": "Estàs segur? Què passa amb la paràbola?"},
                    {"text": "Ànims. Quin camí provaries?"},
                    *[{"text": "Quin camí provaries ara?"}] * 6,
                ],
                "guardia": [
                    REJECTED,
                    "guardia: model refused",
                    OK,
                    {**OK, "infraccions": ["revela_resultat"]},
                    REJECTED,
                    *[OK] * 6,
                ],
            },
        ),
    ]
    rng = random.Random(7)
    for ex_id in sorted(COURSE.exercises)[3::41]:
        ex = COURSE.exercise(ex_id)
        diagnoses = diagnosis_sequence(ex, 3, 6, "random")
        concept_ids = concept_question_ids(COURSE, ex)
        replies: list[JsonObject | str] = [
            {"text": rng.choice(["Què has provat?", "Com continuaries?", "D'acord.", ex.result.value, "Bé. Ho veus?"])}
            for _ in range(18)
        ]
        verdicts: list[JsonObject | str] = [rng.choice([OK, OK, REJECTED]) for _ in range(18)]
        out.append(
            (
                f"{ex_id} fuzzed",
                ex_id,
                [f"missatge {i}" for i in range(len(diagnoses))],
                {
                    "diagnosi": [_with_concept_question(d, concept_ids, rng) for d in diagnoses],
                    "resposta": replies,
                    "guardia": verdicts,
                },
            )
        )
    return out


def _comparable(trace: Mapping[str, object]) -> dict[str, object]:
    out = {k: v for k, v in trace.items() if k not in ("latencia_ms", "crides")}
    calls = trace["crides"]
    assert isinstance(calls, list)
    out["crides"] = [OLD_STAGES.get(c["stage"], c["stage"]) for c in calls]
    return out


SCENARIOS = _scenarios()


@pytest.mark.parametrize(("name", "ex_id", "texts", "script"), SCENARIOS, ids=[s[0] for s in SCENARIOS])
async def test_turns_match_the_legacy_pipeline(
    session_provider: SQLModelSessionProvider, name: str, ex_id: str, texts: list[str], script: Script
) -> None:
    old_llm_fake = LegacyScriptedLLM(script)
    old_tutor = old_pipeline.Tutor(old_llm_fake, OLD_THEORY)
    old_session = old_pipeline.Sessio(exercici=OLD_EXERCISES[ex_id])
    new_llm = _new_llm(script)
    t = tutoring(new_llm, session_provider)
    sid = (await t.starter.start(COURSE.exercise(ex_id).id)).session.id

    for i, text in enumerate(texts):
        origin = "foto" if i == 1 else "text"
        old = old_tutor.turn(old_session, text, origen=origin)
        new = await t.turns.handle(TurnInput(session_id=sid, text=text, origin=origin))
        assert new.message == old["missatge"], (name, i)
        assert [it.id for it in new.references] == [r["id"] for r in old["referencies"]], (name, i)
        assert _comparable(new.trace.model_dump(mode="json")) == _comparable(old["trace"]), (name, i)

    stored = await t.sessions.get(sid)
    assert [m.model_dump() for m in stored.history] == old_session.historial
    assert stored.state.model_dump() == old_session.estat.model_dump()
    # The model was asked exactly the same things.
    new_requests = [
        (stage, r) for stage in (Stage.DIAGNOSIS, Stage.REPLY, Stage.GUARD) for r in new_llm.requests[stage]
    ]
    old_requests = [r for stage in OLD_STAGES for r in old_llm_fake.requests if r[0] == stage]
    assert len(new_requests) == len(old_requests)
    for (stage, new_r), (old_stage, system, user, schema, context) in zip(new_requests, old_requests, strict=True):
        assert stage == OLD_STAGES[old_stage]
        assert (new_r.system, new_r.user, new_r.schema, new_r.context) == (system, user, schema, context)
