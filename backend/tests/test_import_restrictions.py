"""The dependency rule of backend/AGENTS.md, checked on every module's imports (TYPE_CHECKING blocks exempt)."""

import ast
from collections.abc import Iterator
from pathlib import Path

import pytest

from settings import BACKEND_DIR

CORE = BACKEND_DIR / "core"
SDKS = ("anthropic", "openai", "google", "httpx", "sqlmodel", "sqlalchemy", "fastapi", "yaml", "settings", "apps")


def _module(path: Path) -> str:
    return ".".join(path.relative_to(BACKEND_DIR).with_suffix("").parts)


def _imports(path: Path) -> Iterator[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    exempt: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and "TYPE_CHECKING" in ast.unparse(node.test):
            exempt |= {id(n) for n in ast.walk(node)}
    for node in ast.walk(tree):
        if id(node) in exempt:
            continue
        if isinstance(node, ast.Import):
            yield from (a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            yield node.module


def _layer_files(layer: str) -> list[Path]:
    return sorted(p for p in CORE.rglob("*.py") if f"{layer}" in p.relative_to(CORE).parts)


def _top(name: str) -> str:
    return name.split(".")[0]


@pytest.mark.parametrize("path", _layer_files("domain"), ids=_module)
def test_domain_depends_on_nothing_outward(path: Path) -> None:
    bad = [
        i
        for i in _imports(path)
        if _top(i) in SDKS
        or ".application" in i
        or ".infra" in i
        or i.startswith("core.shared.storage")
        or (i.startswith("core.shared.llm_calls") and not _module(path).startswith("core.shared.llm_calls"))
    ]
    assert not bad, f"{_module(path)} imports {bad}"


@pytest.mark.parametrize("path", _layer_files("application"), ids=_module)
def test_application_never_names_infrastructure(path: Path) -> None:
    bad = [i for i in _imports(path) if _top(i) in SDKS or ".infra" in i or i.startswith("core.shared.storage")]
    assert not bad, f"{_module(path)} imports {bad}"


@pytest.mark.parametrize("path", _layer_files("domain"), ids=_module)
def test_a_domain_depends_only_on_its_own_context_course_and_the_shared_kernel(path: Path) -> None:
    """`course` is the shared kernel of the content (every activity is about its exercises and theory)."""
    own = path.relative_to(CORE).parts[0]
    allowed = {own, "course", "shared"}
    bad = [i for i in _imports(path) if i.startswith("core.") and i.split(".")[1] not in allowed]
    assert not bad, f"{_module(path)} imports {bad}"


@pytest.mark.parametrize("path", sorted((CORE / "shared").rglob("*.py")), ids=_module)
def test_the_shared_kernel_knows_no_feature_context(path: Path) -> None:
    contexts = {p.name for p in CORE.iterdir() if p.is_dir() and p.name not in ("shared", "__pycache__")}
    bad = [i for i in _imports(path) if i.startswith("core.") and i.split(".")[1] in contexts]
    assert not bad, f"{_module(path)} imports {bad}"


@pytest.mark.parametrize("path", sorted(CORE.rglob("*.py")), ids=_module)
def test_core_never_imports_the_api(path: Path) -> None:
    assert not [i for i in _imports(path) if _top(i) == "apps"]
