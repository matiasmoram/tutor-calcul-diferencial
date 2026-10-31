import pytest

from core.shared.llm.infra.factory import make_llm_client
from settings import Config


def test_openrouter_uses_its_own_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-openai")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-openrouter")
    sdk = make_llm_client(Config())._client  # type: ignore[attr-defined]
    assert sdk.api_key == "sk-openrouter"


def test_openrouter_without_its_key_never_sends_the_openai_one(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-openai")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY is not set"):
        make_llm_client(Config())
