from typing import Literal

from pydantic import BaseModel, Field

from core.counterexamples.domain.entities.spec import Spec
from core.counterexamples.domain.properties import PROPERTIES, CertificateKind, PropertyKind
from core.counterexamples.domain.values.submission import MAX_PATHS, Certificate, Direction, Path, Submission
from core.counterexamples.domain.values.verdict import PropertyVerdict, RevealedExample, SubmissionResult

MAX_EXPRESSION = 300  # the sympy parser's own limit


class PathRequest(BaseModel):
    x: str = Field(max_length=MAX_EXPRESSION)
    y: str = Field(max_length=MAX_EXPRESSION)


class DirectionRequest(BaseModel):
    u: str = Field(max_length=MAX_EXPRESSION)
    w: str = Field(max_length=MAX_EXPRESSION)


class CertificateRequest(BaseModel):
    camins: list[PathRequest] = Field(default_factory=list, max_length=MAX_PATHS)
    fita: str = Field(default="", max_length=MAX_EXPRESSION)
    direccio: DirectionRequest | None = None
    parcial: Literal["x", "y"] | None = None


class SubmissionRequest(BaseModel):
    funcio: str = Field(max_length=MAX_EXPRESSION)
    valor: str = Field(default="0", max_length=MAX_EXPRESSION)
    certificats: dict[PropertyKind, CertificateRequest] = Field(default_factory=dict)

    def to_domain(self) -> Submission:
        return Submission(
            function=self.funcio,
            origin_value=self.valor,
            certificates={
                kind: Certificate(
                    paths=[Path(x=p.x, y=p.y) for p in c.camins],
                    bound=c.fita,
                    direction=Direction(u=c.direccio.u, w=c.direccio.w) if c.direccio else None,
                    partial=c.parcial,
                )
                for kind, c in self.certificats.items()
            },
        )


class PropertyResponse(BaseModel):
    id: PropertyKind
    etiqueta: str
    certificat: CertificateKind
    ajuda: str

    @classmethod
    def of(cls, kind: PropertyKind) -> "PropertyResponse":
        info = PROPERTIES[kind]
        return cls(id=kind, etiqueta=info.label, certificat=info.certificate, ajuda=info.help)


class SpecSummaryResponse(BaseModel):
    id: str
    tema: int
    titol: str
    dificultat: str
    propietats: list[PropertyResponse]

    @classmethod
    def from_entity(cls, spec: Spec) -> "SpecSummaryResponse":
        return cls(
            id=spec.id,
            tema=spec.topic,
            titol=spec.title,
            dificultat=spec.difficulty,
            propietats=[PropertyResponse.of(k) for k in spec.properties],
        )


class ExampleResponse(BaseModel):
    funcio: str
    valor: str
    certificats: dict[PropertyKind, Certificate]
    explicacio: str

    @classmethod
    def from_entity(cls, example: RevealedExample) -> "ExampleResponse":
        return cls(
            funcio=example.submission.function,
            valor=example.submission.origin_value,
            certificats=dict(example.submission.certificates),
            explicacio=example.explanation,
        )


class SpecResponse(SpecSummaryResponse):
    enunciat: str
    pista: str
    exemple: ExampleResponse | None  # professors only: students see it once they pass

    @classmethod
    def build(cls, spec: Spec, with_example: bool) -> "SpecResponse":
        return cls(
            **SpecSummaryResponse.from_entity(spec).model_dump(),
            enunciat=spec.statement,
            pista=spec.hint,
            exemple=ExampleResponse.from_entity(RevealedExample(submission=spec.example, explanation=spec.explanation))
            if with_example
            else None,
        )


class SubmissionResponse(BaseModel):
    superat: bool  # every property ok or plausible
    rigoros: bool  # every property decided exactly
    veredictes: list[PropertyVerdict]
    exemple: ExampleResponse | None

    @classmethod
    def from_entity(cls, result: SubmissionResult) -> "SubmissionResponse":
        return cls(
            superat=result.passed,
            rigoros=result.rigorous,
            veredictes=result.verdicts,
            exemple=ExampleResponse.from_entity(result.example) if result.example else None,
        )
