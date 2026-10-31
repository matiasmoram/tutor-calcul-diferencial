"""The dependency rules of backend/AGENTS.md, checked on every module's imports (TYPE_CHECKING blocks exempt)."""

import ast
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

from settings import BACKEND_DIR

CORE = BACKEND_DIR / "core"
SDKS = ("anthropic", "openai", "google", "httpx", "sqlmodel", "sqlalchemy", "fastapi", "yaml", "settings", "apps")
# Third-party packages a domain may use besides the standard library: pydantic for its models, and sympy because in
# this course the maths is the domain.
DOMAIN_LIBRARIES = frozenset({"pydantic", "pydantic_core", "sympy"})
# From the LLM port, application code may name the call scope and the failures it reacts to, nothing else.
APPLICATION_LLM_NAMES = {
    "core.shared.llm": frozenset({"call_scope"}),
    "core.shared.llm.call_scope": None,  # any name
    "core.shared.llm.client": frozenset({"LLMError", "LLMProviderError", "TruncatedOutputError"}),
}

type Import = tuple[str, tuple[str, ...]]  # (module, names of a `from` import); a relative module starts with "."


def _module(path: Path) -> str:
    return ".".join(path.relative_to(BACKEND_DIR).with_suffix("").parts)


def _imports(path: Path) -> Iterator[Import]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    exempt: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and "TYPE_CHECKING" in ast.unparse(node.test):
            exempt |= {id(n) for n in ast.walk(node)}
    for node in ast.walk(tree):
        if id(node) in exempt:
            continue
        if isinstance(node, ast.Import):
            yield from ((a.name, ()) for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            yield "." * node.level + (node.module or ""), tuple(a.name for a in node.names)


def _modules(path: Path) -> list[str]:
    return [m for m, _ in _imports(path)]


def _layer_files(layer: str) -> list[Path]:
    return sorted(p for p in CORE.rglob("*.py") if layer in p.relative_to(CORE).parts)


def _top(name: str) -> str:
    return name.split(".")[0]


def _under(name: str, package: str) -> bool:
    return name == package or name.startswith(package + ".")


def _package_through(name: str, part: str) -> str:
    """`core.x.infra.y` -> `core.x.infra` for part "infra"."""
    parts = name.split(".")
    return ".".join(parts[: parts.index(part) + 1])


@pytest.mark.parametrize(
    "path", sorted(p for d in ("core", "apps", "settings") for p in (BACKEND_DIR / d).rglob("*.py")), ids=_module
)
def test_no_relative_imports(path: Path) -> None:
    assert not [m for m in _modules(path) if m.startswith(".")], f"{_module(path)} uses a relative import"


@pytest.mark.parametrize("path", _layer_files("domain"), ids=_module)
def test_a_domain_imports_only_the_allowed_packages(path: Path) -> None:
    """The standard library, `DOMAIN_LIBRARIES`, its own domain, the course domain (the content every activity is
    about) and the shared kernel's `domain` and `math` (outside `math.infra`)."""
    own = _package_through(_module(path), "domain")
    allowed = (own, "core.course.domain", "core.shared.domain", "core.shared.math")
    bad = [
        m
        for m in _modules(path)
        if not (
            _top(m) in sys.stdlib_module_names
            or _top(m) in DOMAIN_LIBRARIES
            or (any(_under(m, p) for p in allowed) and not _under(m, "core.shared.math.infra"))
        )
    ]
    assert not bad, f"{_module(path)} imports {bad}"


@pytest.mark.parametrize("path", _layer_files("application"), ids=_module)
def test_application_never_names_infrastructure(path: Path) -> None:
    bad = [m for m in _modules(path) if _top(m) in SDKS or "infra" in m.split(".") or _under(m, "core.shared.storage")]
    assert not bad, f"{_module(path)} imports {bad}"


@pytest.mark.parametrize("path", _layer_files("application"), ids=_module)
def test_application_takes_only_the_call_scope_and_the_errors_from_the_llm_port(path: Path) -> None:
    bad = []
    for module, names in _imports(path):
        if not _under(module, "core.shared.llm"):
            continue
        allowed = APPLICATION_LLM_NAMES.get(module, frozenset())
        if allowed is not None and not (names and set(names) <= allowed):
            bad.append(f"{module}: {', '.join(names) or '*'}")
    assert not bad, f"{_module(path)} imports {bad}"


def _shared_outside_infra() -> list[Path]:
    """`storage/` is the persistence kernel itself (SQLModel), infrastructure by nature."""
    return sorted(
        p
        for p in (CORE / "shared").rglob("*.py")
        if not {"infra", "storage"} & set(p.relative_to(CORE / "shared").parts)
    )


@pytest.mark.parametrize("path", _shared_outside_infra(), ids=_module)
def test_the_shared_kernel_outside_infra_imports_no_sdk(path: Path) -> None:
    bad = [m for m in _modules(path) if _top(m) in SDKS]
    assert not bad, f"{_module(path)} imports {bad}"


@pytest.mark.parametrize("path", sorted(CORE.rglob("*.py")), ids=_module)
def test_infrastructure_is_imported_only_by_infrastructure(path: Path) -> None:
    """A context's `infra` is private to it; the shared kernel's `infra` and `storage` serve every context's `infra`.
    Composition roots (apps, scripts, test fixtures) build them all."""
    module = _module(path)
    in_infra = "infra" in module.split(".")
    bad = []
    for m in _modules(path):
        if _under(m, "core.shared.storage"):
            ok = in_infra or _under(module, "core.shared.storage")
        elif "infra" in m.split(".") and _under(m, "core.shared"):
            ok = in_infra
        elif "infra" in m.split("."):
            ok = _under(module, _package_through(m, "infra"))
        else:
            continue
        if not ok:
            bad.append(m)
    assert not bad, f"{module} imports {bad}"


@pytest.mark.parametrize("path", sorted((CORE / "shared").rglob("*.py")), ids=_module)
def test_the_shared_kernel_knows_no_feature_context(path: Path) -> None:
    contexts = {p.name for p in CORE.iterdir() if p.is_dir() and p.name not in ("shared", "__pycache__")}
    bad = [m for m in _modules(path) if m.startswith("core.") and m.split(".")[1] in contexts]
    assert not bad, f"{_module(path)} imports {bad}"


@pytest.mark.parametrize("path", sorted(CORE.rglob("*.py")), ids=_module)
def test_core_never_imports_the_api(path: Path) -> None:
    assert not [m for m in _modules(path) if _top(m) == "apps"]
