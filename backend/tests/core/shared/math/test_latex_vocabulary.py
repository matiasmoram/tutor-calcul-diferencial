import json
from collections.abc import Iterator

import yaml

from core.quizzes.domain.services.validation import validate_draft
from core.quizzes.domain.values.drafts import StatementDraft
from core.shared.math.latex_vocabulary import unknown_commands
from settings import BACKEND_DIR


def _texts(value: object) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, v in value.items():
            if key != "fuites":  # leak regexes: "\b", "\d" are regex syntax, not LaTeX
                yield from _texts(v)
    elif isinstance(value, list):
        for v in value:
            yield from _texts(v)


def test_the_course_and_every_cached_document_use_only_known_commands() -> None:
    authored = [*(BACKEND_DIR / "teoria").glob("*.yaml"), *(BACKEND_DIR / "exercicis").glob("*.yaml")]
    texts = [t for p in authored for t in _texts(yaml.safe_load(p.read_text(encoding="utf-8")))]
    cached = (BACKEND_DIR / "generats").rglob("*.json")
    texts += [t for p in cached for t in _texts(json.loads(p.read_text(encoding="utf-8")))]
    assert len(texts) > 1000
    assert {c for t in texts for c in unknown_commands(t)} == set()


def test_invented_commands_are_caught_and_row_breaks_are_not_commands() -> None:
    # Commands that do not exist, inside math.
    garbage = r"$R_3=\frac{1}{6}\bigl(e^{\tau\fterm{0.2}}(0.2)^3\bigr)$ per a algun $\tau\blink\text{ entre }0$"
    assert unknown_commands(garbage) == {"fterm", "blink"}
    assert unknown_commands(r"$\begin{pmatrix}0&e\\e&0\end{pmatrix}$, $\det\begin{pmatrix}1\\y\end{pmatrix}$") == set()
    # A backslash escaped twice outside any environment: a row break followed by plain text.
    assert unknown_commands(r"Si $A\\subseteq\\overline{B}$") == {"\\subseteq", "\\overline"}


def test_a_statement_with_an_invented_command_is_rejected() -> None:
    draft = StatementDraft(
        statement=r"Si $f$ és contínua, $f\term{·}g$ també ho és.",
        verdict="cert",
        trap="",
        counterexample="",
        solution="El producte de contínues és continu.",
        key_ideas=["producte de funcions contínues"],
        hint="Pensa en el producte.",
        concept="Continuïtat",
        theory=[],
        checks=[],
    )
    assert any("term" in p for p in validate_draft(draft, refs=[]))
