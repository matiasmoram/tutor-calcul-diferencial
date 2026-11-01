"""Contract keys (LLM JSON schemas, the HTTP JSON the frontend reads, stored documents) keep their Catalan spelling
while attributes are English: a field reads either spelling and writes the Catalan one."""

from pydantic import AliasChoices


def catalan_alias(catalan: str, english: str) -> AliasChoices:
    """The ``validation_alias`` of a field whose contract key is ``catalan``; pair it with
    ``serialization_alias=catalan``."""
    return AliasChoices(catalan, english)


def omit_none(value: object) -> bool:
    """The ``exclude_if`` of an optional field left out of the JSON while it is None."""
    return value is None
