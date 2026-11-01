from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from apps.tutor_api.server import create_app
from tests.fakes.llm import ScriptedLLMClient


@pytest.fixture
def scripted_llm() -> ScriptedLLMClient:
    return ScriptedLLMClient({})


@pytest.fixture
def api(tmp_path, monkeypatch: pytest.MonkeyPatch, scripted_llm: ScriptedLLMClient) -> Iterator[TestClient]:
    """The real app on a throwaway SQLite database, with the scripted model."""
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{(tmp_path / 'api.db').as_posix()}")
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.delenv("TUTOR_CLAU_PROFESSOR", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    monkeypatch.setenv("TUTOR_DEMO", "1")  # tests see solutions unless they set a professor key
    with TestClient(create_app(llm=scripted_llm)) as client:
        yield client
