from itertools import pairwise

from pydantic import BaseModel, ConfigDict, Field

from core.shared.domain.contract import catalan_alias
from core.shared.domain.ids import ExerciseId, SessionId
from core.tutoring.domain.entities.tutor_session import TutorSession
from core.tutoring.domain.entities.tutor_turn import TutorTurn

# Repeating these is expected (an off-topic student, a closed exercise), not a loop of the tutor.
_NOT_LOOPS = ("despres_de_tancar", "redirigir")


class SessionSummary(BaseModel):
    """One session in the professor's review list, with the flags worth a look."""

    model_config = ConfigDict(serialize_by_alias=True, frozen=True)

    id: SessionId
    exercise_id: ExerciseId = Field(
        validation_alias=catalan_alias("exercici", "exercise_id"), serialization_alias="exercici"
    )
    started_at: float = Field(validation_alias=catalan_alias("inici", "started_at"), serialization_alias="inici")
    last_activity_at: float = Field(
        validation_alias=catalan_alias("darrer", "last_activity_at"), serialization_alias="darrer"
    )
    turns: int = Field(validation_alias=catalan_alias("torns", "turns"), serialization_alias="torns")
    closed: bool = Field(validation_alias=catalan_alias("tancat", "closed"), serialization_alias="tancat")
    fallbacks: int
    guard_rejections: int = Field(
        validation_alias=catalan_alias("rebutjos_guardia", "guard_rejections"), serialization_alias="rebutjos_guardia"
    )
    loops: int = Field(validation_alias=catalan_alias("bucles", "loops"), serialization_alias="bucles")
    steps_shown: int = Field(
        validation_alias=catalan_alias("mostrar_pas", "steps_shown"), serialization_alias="mostrar_pas"
    )
    frustration: int = Field(
        validation_alias=catalan_alias("frustracio", "frustration"), serialization_alias="frustracio"
    )

    @classmethod
    def of(cls, session: TutorSession, turns: list[TutorTurn]) -> "SessionSummary":
        plans = [(t.trace.plan.action, t.trace.plan.target_step, t.trace.plan.hint_level) for t in turns]
        return cls(
            id=session.id,
            exercise_id=session.exercise_id,
            started_at=session.created_at,
            last_activity_at=session.updated_at,
            turns=len(turns),
            closed=any(p[0] in ("tancar", "mostrar_conclusio") for p in plans),
            fallbacks=sum(1 for t in turns if t.trace.fallback),
            guard_rejections=sum(max(0, len(t.trace.attempts) - 1) for t in turns),
            loops=sum(1 for a, b in pairwise(plans) if a == b and a[0] not in _NOT_LOOPS),
            steps_shown=sum(1 for p in plans if p[0] == "mostrar_pas"),
            frustration=sum(1 for t in turns if t.trace.diagnosis.intent == "frustracio"),
        )
