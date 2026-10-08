from abc import ABC, abstractmethod

from core.shared.llm_calls.domain.llm_call import LLMCall


class LLMCallRepository(ABC):
    @abstractmethod
    async def add(self, call: LLMCall) -> None: ...

    @abstractmethod
    async def of_session(self, session_id: str, limit: int = 500) -> list[LLMCall]:
        """Most recent first."""
