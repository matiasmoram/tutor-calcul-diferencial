"""The authored counterexample challenges, loaded once per test run (read-only)."""

from functools import cache

from core.counterexamples.domain.entities.spec import SpecCatalog
from core.counterexamples.infra.yaml_spec_source import YamlSpecSource
from settings import BACKEND_DIR


@cache
def authored_challenges() -> SpecCatalog:
    return YamlSpecSource(BACKEND_DIR / "contraexemples" / "reptes.yaml").load()
