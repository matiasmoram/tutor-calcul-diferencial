"""Shared data of the script tests: "troba l'error" documents and reviews as the model writes them."""

import json
from pathlib import Path

from core.shared.llm.client import JsonObject
from tests.core.mistakes.builders import (
    PART2_ERROR,
    PART3_ERROR,
    corruption,
    edit,
    err,
    finding,
    part_checked,
    terr,
    theory_written,
    written,
)

PROBLEM_ERRORS = [err(2, "$x^4 \\ge x^4+y^2$"), err(3, "demostra que el límit existeix")]
PROBLEM_FINDINGS = [finding(2, "$x^4 \\ge x^4+y^2$"), finding(3, "demostra que el límit existeix")]
THEORY_ERRORS = [terr(1, "diferenciable en un obert $U$"), terr(4, "$D_vf(a)=Df(a)v$")]
THEORY_FINDINGS = [finding(1, "diferenciable"), finding(4, "$D_vf(a)=Df(a)v$")]

# "Pas a pas": the correct resolutions (tests.core.mistakes.builders.PARTS / THEORY_PARTS) as a writer puts them in a
# <batch>.net.json, the errors put into them, and the blind checks that find exactly those errors.
NET_PROBLEM: JsonObject = {"font": "problema", "id": "t2-4c"} | written()
NET_THEORY: JsonObject = {"font": "teoria", "id": "T3.21"} | theory_written()
PART_ERRORS: dict[int, JsonObject] = {
    2: PART2_ERROR | {"explicacio": "EXPLICACIO-2", "correccio": "CORRECCIO-2", "pista": "PISTA-2"},
    3: PART3_ERROR | {"explicacio": "EXPLICACIO-3", "correccio": "CORRECCIO-3", "pista": "PISTA-3"},
}
PART_FOUND: dict[int, JsonObject] = {2: part_checked(finding(1, "x^4 \\ge")), 3: part_checked(finding(2, "és $1$"))}
THEORY_PART_ERRORS: dict[int, JsonObject] = {
    1: corruption([edit(1, "de classe $\\mathcal{C}^1$", "diferenciable")], "diferenciable", tipus="hipotesi"),
    3: corruption([edit(1, "és diferenciable", "és contínua")], "$f$ és contínua", tipus="conclusio"),
}
THEORY_PART_FOUND: dict[int, JsonObject] = {
    1: part_checked(finding(1, "diferenciable")),
    3: part_checked(finding(1, "és contínua")),
}


def stored(directory: Path) -> list[Path]:
    """The documents saved under `directory`, as `<source>/<difficulty>/<id>.json`."""
    return sorted(directory.glob("*/*/*.json"))


def write_json(path: Path, data: object) -> Path:
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path
