"""Shared data of the script tests: "troba l'error" documents and reviews as the model writes them."""

from pathlib import Path

from tests.core.mistakes.builders import err, finding, terr

PROBLEM_ERRORS = [err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")]
PROBLEM_FINDINGS = [finding(2, "$x^4 \\ge x^4+y^2$"), finding(3, "demostra que el límit existeix")]
THEORY_ERRORS = [terr(1, "diferenciable en un obert $U$"), terr(4, "$D_vf(a)=Df(a)v$")]
THEORY_FINDINGS = [finding(1, "diferenciable"), finding(4, "$D_vf(a)=Df(a)v$")]


def stored(directory: Path) -> list[Path]:
    """The documents saved under `directory`, as `<source>/<difficulty>/<id>.json`."""
    return sorted(directory.glob("*/*/*.json"))
