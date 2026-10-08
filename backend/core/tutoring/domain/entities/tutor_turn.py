from pydantic import BaseModel

from core.shared.domain.ids import SessionId
from core.tutoring.domain.values.chat_message import TurnOrigin
from core.tutoring.domain.values.turn_trace import TurnTrace


class TutorTurn(BaseModel):
    """One exchange of a session as it is kept for review: the student's text, the reply, and the full trace."""

    session_id: SessionId
    number: int
    created_at: float
    origin: TurnOrigin = "text"
    student_text: str
    tutor_text: str
    trace: TurnTrace
