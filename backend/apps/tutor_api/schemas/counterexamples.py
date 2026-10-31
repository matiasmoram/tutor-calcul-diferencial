from typing import Literal

from pydantic import BaseModel, Field

from apps.tutor_api.schemas.course import TheoryItemResponse
from apps.tutor_api.schemas.student_text import StudentText
from core.counterexamples.domain.entities.spec import Spec, SpecCatalog
from core.counterexamples.domain.values.properties import PROPERTIES, CertificateKind, PropertyKind
from core.counterexamples.domain.values.submission import MAX_PATHS, Certificate, Direction, Path, Submission
from core.counterexamples.domain.values.verdict import PropertyVerdict, RevealedExample, SubmissionResult
from core.course.domain.entities.course import Course
from core.shared.domain.ids import TheoryItemId
from core.shared.math.sympy_checks import MAX_LENGTH

MAX_EXPRESSION = MAX_LENGTH


class PathRequest(BaseModel):
    x: StudentText = Field(max_length=MAX_EXPRESSION)
    y: StudentText = Field(max_length=MAX_EXPRESSION)


class DirectionRequest(BaseModel):
    u: StudentText = Field(max_length=MAX_EXPRESSION)
    w: StudentText = Field(max_length=MAX_EXPRESSION)


class CertificateRequest(BaseModel):
    camins: list[PathRequest] = Field(default_factory=list, max_length=MAX_PATHS)
    fita: StudentText = Field(default="", max_length=MAX_EXPRESSION)
    direccio: DirectionRequest | None = None
    parcial: Literal["x", "y"] | None = None


class SubmissionRequest(BaseModel):
    funcio: StudentText = Field(max_length=MAX_EXPRESSION)
    valor: StudentText = Field(default="0", max_length=MAX_EXPRESSION)
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


def _items(course: Course, ids: list[TheoryItemId]) -> list[TheoryItemResponse]:
    return [TheoryItemResponse.from_entity(course.theory_item(i)) for i in ids]


class PropertyResponse(BaseModel):
    id: PropertyKind
    etiqueta: str
    certificat: CertificateKind
    ajuda: str
    teoria: list[TheoryItemResponse]  # where the notes define it ("Repassa" when it fails)

    @classmethod
    def from_entity(cls, kind: PropertyKind, catalog: SpecCatalog, course: Course) -> "PropertyResponse":
        info = PROPERTIES[kind]
        return cls(
            id=kind,
            etiqueta=info.label,
            certificat=info.certificate,
            ajuda=info.help,
            teoria=_items(course, list(catalog.property_theory.get(kind, []))),
        )


class SpecSummaryResponse(BaseModel):
    id: str
    tema: int
    titol: str
    dificultat: str
    propietats: list[PropertyResponse]

    @classmethod
    def from_entity(cls, spec: Spec, catalog: SpecCatalog, course: Course) -> "SpecSummaryResponse":
        return cls(
            id=spec.id,
            tema=spec.topic,
            titol=spec.title,
            dificultat=spec.difficulty,
            propietats=[PropertyResponse.from_entity(k, catalog, course) for k in spec.properties],
        )


class ExampleResponse(BaseModel):
    funcio: str
    valor: str
    certificats: dict[PropertyKind, Certificate]
    explicacio: str
    teoria_reservada: list[TheoryItemResponse]  # where the notes show a counterexample like this one

    @classmethod
    def from_entity(cls, example: RevealedExample, course: Course) -> "ExampleResponse":
        return cls(
            funcio=example.submission.function,
            valor=example.submission.origin_value,
            certificats=dict(example.submission.certificates),
            explicacio=example.explanation,
            teoria_reservada=_items(course, example.reserved_theory),
        )


class SpecResponse(SpecSummaryResponse):
    enunciat: str
    pista: str
    teoria: list[TheoryItemResponse]  # the definitions and results the challenge is about, shown from the start
    exemple: ExampleResponse | None  # professors only: students see it once they pass

    @classmethod
    def from_entity(
        cls, spec: Spec, catalog: SpecCatalog, course: Course, *, with_example: bool = False
    ) -> "SpecResponse":
        example = RevealedExample(
            submission=spec.example, explanation=spec.explanation, reserved_theory=spec.reserved_theory
        )
        return cls(
            **SpecSummaryResponse.from_entity(spec, catalog, course).model_dump(),
            enunciat=spec.statement,
            pista=spec.hint,
            teoria=_items(course, spec.theory),
            exemple=ExampleResponse.from_entity(example, course) if with_example else None,
        )


class SubmissionResponse(BaseModel):
    superat: bool  # every property ok or plausible
    rigoros: bool  # every property decided exactly
    veredictes: list[PropertyVerdict]
    exemple: ExampleResponse | None

    @classmethod
    def from_entity(cls, result: SubmissionResult, course: Course) -> "SubmissionResponse":
        return cls(
            superat=result.passed,
            rigoros=result.rigorous,
            veredictes=result.verdicts,
            exemple=ExampleResponse.from_entity(result.example, course) if result.example else None,
        )
