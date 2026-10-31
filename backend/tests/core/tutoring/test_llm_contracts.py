"""The JSON contracts with the model: closed enums, Catalan keys, normalization of what comes back."""

from core.tutoring.domain.services.theory_access import concept_question_ids
from core.tutoring.domain.values.guard_verdict import GuardVerdict
from core.tutoring.domain.values.session_state import SessionState
from core.tutoring.infra.llm_schemas import DIAGNOSIS_KEYS, diagnosis_schema, guard_schema
from tests.core.tutoring.builders import COURSE, EX4C, diagnosis, diagnosis_json


def test_diagnosis_schema_uses_closed_enums() -> None:
    schema = diagnosis_schema(EX4C)
    props = schema["properties"]
    assert isinstance(props, dict)
    assert props["pas_actual"]["enum"] == [*EX4C.step_ids, "cap"]
    assert "altre" in props["errors_detectats"]["items"]["enum"]
    assert schema["required"] == DIAGNOSIS_KEYS == list(props)
    assert DIAGNOSIS_KEYS[0] == "evidencia" and DIAGNOSIS_KEYS[-1] == "teoria_pregunta"


def test_guard_schema_lists_every_violation() -> None:
    props = guard_schema()["properties"]
    assert isinstance(props, dict)
    assert props["veredicte"]["enum"] == ["ok", "rebutjat"]
    assert "obeeix_l_alumne" in props["infraccions"]["items"]["enum"]


def test_diagnosis_concept_ids_exclude_reserved_items() -> None:
    some = EX4C.all_refs()[0]
    ex = EX4C.model_copy(update={"reserved_theory": [some]})
    assert some.item_id in concept_question_ids(COURSE, EX4C)
    assert some.item_id not in concept_question_ids(COURSE, ex)


def test_normalization_completes_the_steps_and_drops_unusable_ids() -> None:
    raw = diagnosis(
        estat_passos=[{"pas": "acotar", "estat": "en_curs"}, {"pas": "inventat", "estat": "completat"}],
        errors_detectats=["altre", "camins_com_a_prova", "camins_com_a_prova"],
        teoria_pregunta=["T2.6", "T9.1", "T2.6", "T2.7", "T2.8"],
    )
    d = raw.normalized(EX4C.step_ids, ["T2.6", "T2.7", "T2.8"])
    assert [(s.step_id, s.state) for s in d.step_states] == [
        (s, "en_curs" if s == "acotar" else "no_iniciat") for s in EX4C.step_ids
    ]
    assert d.detected_mistakes == ["camins_com_a_prova"]  # "altre" without a description is dropped
    assert d.question_theory == ["T2.6", "T2.7"]


def test_values_serialize_to_the_catalan_contract() -> None:
    d = diagnosis()
    assert d.model_dump() == diagnosis_json() | {"teoria_pregunta": []}
    state = SessionState(completed=["candidat"], turns=2, closed=True)
    dumped = state.model_dump()
    assert dumped["completats"] == ["candidat"] and dumped["torns"] == 2 and dumped["tancat"]
    assert SessionState.model_validate(dumped) == state


def test_inconsistent_guard_verdicts_fail_closed() -> None:
    v = GuardVerdict.model_validate({"veredicte": "ok", "infraccions": ["revela_resultat"], "explicacio": ""})
    assert not v.consistent().approved
    v = GuardVerdict.model_validate({"veredicte": "rebutjat", "infraccions": [], "explicacio": ""})
    assert v.consistent().violations == ["no_segueix_l_accio"]
