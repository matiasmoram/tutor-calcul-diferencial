from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from core.counterexamples.domain.values.properties import PropertyKind
from core.counterexamples.domain.values.submission import Submission
from core.shared.domain.contract import catalan_alias
from core.shared.domain.ids import TheoryItemId

# "ok": decided exactly (one-variable limits, an equality sympy simplifies). "plausible": rests on sampling (a radial
# bound checked on a grid, directional derivatives in a generic direction plus a few fixed ones). "falla": the
# certificate or the function does not have the property. "indeterminat": sympy could not decide, or no certificate.
VerdictStatus = Literal["ok", "plausible", "falla", "indeterminat"]
PASSING: frozenset[VerdictStatus] = frozenset({"ok", "plausible"})


class PropertyVerdict(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    kind: PropertyKind = Field(validation_alias=catalan_alias("propietat", "kind"), serialization_alias="propietat")
    status: VerdictStatus = Field(validation_alias=catalan_alias("estat", "status"), serialization_alias="estat")
    detail: str = Field(default="", validation_alias=catalan_alias("detall", "detail"), serialization_alias="detall")
    # The computations behind the verdict, as LaTeX lines the student can read ("\partial_x f(0,0) = 0").
    computations: list[str] = Field(
        default_factory=list, validation_alias=catalan_alias("calculs", "computations"), serialization_alias="calculs"
    )


class RevealedExample(BaseModel):
    """The challenge's authored solution and why it works."""

    submission: Submission
    explanation: str
    reserved_theory: list[TheoryItemId] = Field(default_factory=list)  # where the notes show such an example


class SubmissionResult(BaseModel):
    verdicts: list[PropertyVerdict]
    # Given only once the student has passed (or to a professor): comparing comes after building your own.
    example: RevealedExample | None = None

    @property
    def passed(self) -> bool:
        return all(v.status in PASSING for v in self.verdicts)

    @property
    def rigorous(self) -> bool:
        """Every property decided exactly, none only plausible."""
        return all(v.status == "ok" for v in self.verdicts)
