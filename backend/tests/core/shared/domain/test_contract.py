from pydantic import BaseModel, ConfigDict, Field

from core.shared.domain.contract import catalan_alias, omit_none


class _Statement(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    text: str = Field(validation_alias=catalan_alias("enunciat", "text"), serialization_alias="enunciat")
    hint: str | None = Field(
        default=None, validation_alias=catalan_alias("pista", "hint"), serialization_alias="pista", exclude_if=omit_none
    )


def test_a_field_reads_either_spelling_and_writes_the_catalan_key() -> None:
    from_contract = _Statement.model_validate({"enunciat": "f és contínua", "pista": "T3.12"})
    from_code = _Statement.model_validate({"text": "f és contínua", "hint": "T3.12"})

    assert from_contract == from_code
    assert from_contract.model_dump(mode="json") == {"enunciat": "f és contínua", "pista": "T3.12"}
    assert _Statement.model_validate_json(from_contract.model_dump_json()) == from_contract


def test_an_unset_optional_field_is_left_out_of_the_json() -> None:
    assert _Statement.model_validate({"enunciat": "x"}).model_dump(mode="json") == {"enunciat": "x"}


def test_omit_none_drops_only_none() -> None:
    assert omit_none(None)
    assert not any(omit_none(v) for v in (0, 0.0, False, "", [], {}))
