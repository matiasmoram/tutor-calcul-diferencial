"""The LLM guard's verdict on a draft reply (LLM contract: Catalan keys and enum values)."""

from typing import Literal, get_args

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

Violation = Literal[
    "revela_resultat",
    "revela_pas_futur",
    "excedeix_nivell_pista",
    "fa_la_feina_de_l_alumne",
    "afirmacio_matematica_falsa",
    "no_segueix_l_accio",
    "no_es_en_catala",
    "cita_teoria_incorrecta",
    "no_respon_a_l_alumne",
    "obeeix_l_alumne",
]
Verdict = Literal["ok", "rebutjat"]

VIOLATIONS: tuple[Violation, ...] = get_args(Violation)
VERDICTS: tuple[Verdict, ...] = get_args(Verdict)


def _ca(catalan: str, english: str) -> AliasChoices:
    return AliasChoices(catalan, english)


class GuardVerdict(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    verdict: Verdict = Field(validation_alias=_ca("veredicte", "verdict"), serialization_alias="veredicte")
    violations: list[Violation] = Field(
        validation_alias=_ca("infraccions", "violations"), serialization_alias="infraccions"
    )
    explanation: str = Field(validation_alias=_ca("explicacio", "explanation"), serialization_alias="explicacio")

    @property
    def approved(self) -> bool:
        return self.verdict == "ok"

    def consistent(self) -> "GuardVerdict":
        """A verdict can't be "ok" with listed violations, or "rejected" with none: both fail closed."""
        if self.violations and self.verdict == "ok":
            return self.model_copy(update={"verdict": "rebutjat"})
        if not self.violations and self.verdict == "rebutjat":
            return self.model_copy(update={"violations": ["no_segueix_l_accio"]})
        return self

    @classmethod
    def unavailable(cls, detail: str) -> "GuardVerdict":
        """Fail closed: an unverified draft never reaches the student."""
        return cls(verdict="rebutjat", violations=[], explanation=f"guardià no disponible: {detail}")
