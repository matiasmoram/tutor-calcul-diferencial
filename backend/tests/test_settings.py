"""The environment rules of `Config`: a supported provider, and what a production start (RENDER set) requires."""

import pytest

from settings import LLM_PROVIDERS, Config, api_key_variable

KEYS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY")


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("RENDER", "DATABASE_URL", "LLM_PROVIDER", "TUTOR_CLAU_PROFESSOR", "TUTOR_DEMO", *KEYS):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv("TUTOR_SYMPY_WORKER_MEMORY_MB", raising=False)


@pytest.fixture
def production(monkeypatch: pytest.MonkeyPatch) -> None:
    """Everything a production start needs; each test removes one piece."""
    monkeypatch.setenv("RENDER", "true")
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:secret@db.example:6543/postgres")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("TUTOR_CLAU_PROFESSOR", "key")


def test_the_provider_defaults_to_openai(monkeypatch: pytest.MonkeyPatch) -> None:
    assert Config().LLM_PROVIDER == "openai"
    monkeypatch.setenv("LLM_PROVIDER", "")
    assert Config().LLM_PROVIDER == "openai"
    monkeypatch.setenv("LLM_PROVIDER", "OpenRouter")
    assert Config().LLM_PROVIDER == "openrouter"


def test_an_unknown_provider_is_refused_naming_the_supported_ones(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "opneai")
    with pytest.raises(ValueError, match="LLM_PROVIDER='opneai'") as error:
        Config()
    assert all(provider in str(error.value) for provider in LLM_PROVIDERS)


@pytest.mark.parametrize("provider", LLM_PROVIDERS)
def test_each_provider_reads_its_own_key(monkeypatch: pytest.MonkeyPatch, provider: str) -> None:
    monkeypatch.setenv("LLM_PROVIDER", provider)
    assert api_key_variable(Config()) == f"{provider.upper()}_API_KEY"


def test_locally_only_a_missing_key_is_a_problem(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TUTOR_DEMO", "1")  # no DATABASE_URL, no professor key: fine on a laptop
    assert Config().startup_problems() == ["OPENAI_API_KEY is not set (LLM_PROVIDER=openai)"]
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    assert Config().startup_problems() == []


@pytest.mark.usefixtures("production")
def test_a_complete_production_configuration_has_no_problem() -> None:
    config = Config()
    assert config.PRODUCTION and config.startup_problems() == []


@pytest.mark.usefixtures("production")
@pytest.mark.parametrize(
    ("change", "problem"),
    [
        ({"OPENAI_API_KEY": None}, "OPENAI_API_KEY is not set (LLM_PROVIDER=openai)"),
        ({"LLM_PROVIDER": "openrouter"}, "OPENROUTER_API_KEY is not set (LLM_PROVIDER=openrouter)"),
        ({"DATABASE_URL": None}, "DATABASE_URL is not set"),
        ({"TUTOR_CLAU_PROFESSOR": None}, "TUTOR_CLAU_PROFESSOR is not set"),
        ({"TUTOR_DEMO": "1"}, "TUTOR_DEMO=1 is for local use only"),
    ],
)
def test_production_names_each_missing_or_unsafe_setting(
    monkeypatch: pytest.MonkeyPatch, change: dict[str, str | None], problem: str
) -> None:
    for name, value in change.items():
        if value is None:
            monkeypatch.delenv(name)
        else:
            monkeypatch.setenv(name, value)
    [found] = Config().startup_problems()
    assert found.startswith(problem)


def test_the_sympy_worker_memory_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    assert Config().SYMPY_WORKER_MEMORY_MB == 256
    monkeypatch.setenv("TUTOR_SYMPY_WORKER_MEMORY_MB", "0")
    assert Config().SYMPY_WORKER_MEMORY_MB == 0
