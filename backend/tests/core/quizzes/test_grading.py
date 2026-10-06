import pytest

from core.quizzes.domain.entities.grading import Answer, StudentCheck
from core.quizzes.domain.services.scoring import faithful
from core.shared.llm.client import Stage
from core.shared.storage.session_provider import SQLModelSessionProvider
from tests.core.quizzes.builders import answers_grader, check, grader, idea, quiz, source, transcriber
from tests.fakes.llm import ScriptedLLMClient


def answer(sid: str, verdict: str, justification: str) -> Answer:
    return Answer.model_validate({"id": sid, "veredicte": verdict, "justificacio": justification})


async def test_grading_is_decided_by_code_and_sympy(session_provider: SQLModelSessionProvider) -> None:
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GRADING: [
                grader(
                    {"id": "a1", "idees": [idea(1, "sobre $y=mx$")], "justificacio": "correcta", "feedback": "f1"},
                    # Wrong verdict: whatever the LLM says, no points.
                    {"id": "a2", "idees": [idea(1, "no")], "justificacio": "correcta", "feedback": "f2"},
                    {"id": "a3", "idees": [idea(1, "Està bé")], "justificacio": "correcta", "feedback": "f3"},
                )
            ],
            # Right verdict, "correcta", but the student's claimed limit is false: downgraded to parcial.
            Stage.QUIZ_EXTRACTION: [
                transcriber(
                    a1=[check("limit", "x*(m*x)/(x**2+(m*x)**2)", "0") | {"cita_alumne": "sobre $y=mx$ dona $0$"}]
                )
            ],
        }
    )
    answers = [
        answer("a1", "fals", "sobre $y=mx$ dona $0$"),
        answer("a2", "fals", "no"),
        answer("a3", "fals", "Està bé."),
        answer("a4", "", ""),
    ]
    r = await answers_grader(llm, session_provider).grade_answers(source(), quiz(), answers, {"a3"})
    it = {i.id: i for i in r.statements}
    assert it["a1"].justification == "parcial" and it["a1"].cas_note and it["a1"].points == 0.65
    assert it["a2"].justification == "incorrecta" and it["a2"].points == 0 and not it["a2"].correct
    assert it["a3"].justification == "correcta" and it["a3"].points == 0.85  # hint used
    assert it["a4"].points == 0 and it["a4"].answer == ""
    assert r.grade == round(100 * (0.65 + 0 + 0.85 + 0) / 4) and r.correct == 2
    graded = llm.requests[Stage.QUIZ_GRADING][0].user
    # Unanswered statements are not sent; key ideas go numbered to the grader.
    assert "[a4]" not in graded and "idees clau: (1) i" in graded
    # The transcriber never sees verdicts or solutions (nor the notes).
    extraction = llm.requests[Stage.QUIZ_EXTRACTION][0]
    assert "veredicte correcte" not in extraction.user and "resolució de referència" not in extraction.user
    assert "sobre $y=mx$ dona $0$" in extraction.user and extraction.context is None


async def test_transcribed_value_must_be_the_one_the_student_wrote(session_provider: SQLModelSessionProvider) -> None:
    # The student wrote that the limit on the parabola is 1 (it is 1/2).
    parabola = "x**2*(x**2)/(x**4+(x**2)**2)"
    llm = ScriptedLLMClient(
        {
            Stage.QUIZ_GRADING: [
                grader(
                    {"id": "a1", "idees": [idea(1, "sobre $y = x^2$")], "justificacio": "correcta", "feedback": ""},
                    {"id": "a3", "idees": [idea(1, "Sobre les rectes")], "justificacio": "correcta", "feedback": ""},
                )
            ],
            Stage.QUIZ_EXTRACTION: [
                transcriber(
                    a1=[
                        # faithful: value 1 is in the quote -> run -> false -> downgrade
                        check("limit", parabola, "1") | {"cita_alumne": "sobre $y = x^2$ el límit és $1$"},
                        # "corrected" by the transcriber: 1/2 is not what the quote says -> dropped
                        check("limit", parabola, "1/2") | {"cita_alumne": "sobre $y = x^2$ el límit és $1$"},
                    ],
                    a3=[check("limit", "x", "0") | {"cita_alumne": "sobre y=x^2 el límit és 1"}],  # not in a3's answer
                )
            ],
        }
    )
    answers = [
        answer("a1", "fals", r"$\frac{x^2y}{x^4+y^2}$: sobre $y = x^2$ el límit és $1$."),
        answer("a3", "fals", "Sobre les rectes dona 0."),
    ]
    r = await answers_grader(llm, session_provider).grade_answers(source(), quiz(), answers, set())
    it = {i.id: i for i in r.statements}
    assert [c.value for c in it["a1"].student_checks] == ["1"]
    assert it["a1"].student_checks[0].status == "falla" and it["a1"].justification == "parcial"
    assert it["a3"].justification == "correcta" and it["a3"].student_checks == []
    assert r.model_dump()["afirmacions"][0]["comprovacions_alumne"][0]["cita_alumne"].startswith("sobre")


@pytest.mark.parametrize(
    ("value", "quote", "ok"),
    [
        ("1", "el límit és $1$", True),
        ("1/2", "el límit és $1$", False),
        ("1/2", r"val $\frac{1}{2}$", True),
        ("m/(1+m**2)", r"dona $\frac{m}{1+m^2}$, que depèn de m", True),
        ("0", "sobre y=mx dona 0", True),
        ("0", "sobre y=mx dona zero", False),
    ],
)
def test_fidelity_of_transcribed_values(value: str, quote: str, ok: bool) -> None:
    claim = StudentCheck.model_validate(check("limit", "x", value) | {"cita_alumne": quote})
    assert faithful(claim) is ok


async def test_rubric_needs_real_evidence_for_each_idea(session_provider: SQLModelSessionProvider) -> None:
    q = quiz()
    q.statements[1].key_ideas = ["contrarecíproc", "els dos iterats valdrien L", "contradicció"]
    text = "Per la proposició 12."
    llm = ScriptedLLMClient(
        {
            # A lenient grader credits all three ideas, but with one quote (and one made-up quote).
            Stage.QUIZ_GRADING: [
                grader(
                    {
                        "id": "a2",
                        "idees": [
                            idea(1, "Per la proposició 12"),
                            idea(2, "Per la proposició 12"),
                            idea(3, "per tant contradicció"),
                        ],
                        "justificacio": "correcta",
                        "feedback": "",
                    }
                )
            ],
            Stage.QUIZ_EXTRACTION: [transcriber(a2=[])],
        }
    )
    r = await answers_grader(llm, session_provider).grade_answers(source(), q, [answer("a2", "cert", text)], set())
    a2 = next(i for i in r.statements if i.id == "a2")
    assert a2.ideas_present == [1] and a2.justification == "parcial" and a2.points == 0.65


async def test_grading_without_answers_makes_no_call(session_provider: SQLModelSessionProvider) -> None:
    r = await answers_grader(ScriptedLLMClient({}), session_provider).grade_answers(source(), quiz(), [], set())
    assert r.grade == 0 and r.call is None
    assert r.statements[0].feedback == "No has contestat aquesta afirmació."


async def test_the_grading_serializes_to_the_keys_the_frontend_reads(
    session_provider: SQLModelSessionProvider,
) -> None:
    r = await answers_grader(ScriptedLLMClient({}), session_provider).grade_answers(source(), quiz(), [], {"a1"})
    doc = r.model_dump(mode="json")
    assert set(doc) == {"nota", "encerts", "total", "afirmacions", "resum", "crida"}
    assert set(doc["afirmacions"][0]) == {
        "id", "resposta", "veredicte", "encert", "justificacio", "feedback", "nota_cas", "comprovacions_alumne",
        "idees_presents", "pista_usada", "punts", "solucio",
    }  # fmt: skip
    assert set(doc["afirmacions"][0]["solucio"]) == {
        "contraexemple",
        "resolucio",
        "idees_clau",
        "teoria",
        "comprovacions",
    }
    assert doc["afirmacions"][0]["pista_usada"] is True
