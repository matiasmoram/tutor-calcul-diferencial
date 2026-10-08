import re
import uuid
from typing import Any, ClassVar, Self

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class CheckedStr(str):
    """A string value object validated on construction. Pydantic validates and serializes it as a plain string."""

    PATTERN: ClassVar[re.Pattern[str]]

    def __new__(cls, value: str) -> Self:
        if not isinstance(value, str) or not cls.PATTERN.fullmatch(value):
            raise ValueError(f"invalid {cls.__name__}: {value!r}")
        return super().__new__(cls, value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls, core_schema.str_schema(), serialization=core_schema.plain_serializer_function_ser_schema(str)
        )


class HexId(CheckedStr):
    PATTERN = re.compile(r"[0-9a-f]{32}")

    @classmethod
    def generate(cls) -> Self:
        return cls(uuid.uuid4().hex)
