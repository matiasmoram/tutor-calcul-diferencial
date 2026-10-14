import re
from collections.abc import Sequence

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

TOO_LARGE = "La petició és massa gran."


class BodySizeLimit:
    """Rejects a request body over the limit of its path with a 413, before the app parses it.

    A declared Content-Length over the limit is refused at once; a body without one (chunked) is counted as it
    arrives, and the read that crosses the limit raises the 413 (FastAPI lets an HTTPException from the body read
    through as is)."""

    def __init__(self, app: ASGIApp, default: int, by_path: Sequence[tuple[str, int]] = ()) -> None:
        self._app = app
        self._default = default
        self._by_path = [(re.compile(pattern), limit) for pattern, limit in by_path]

    def limit_for(self, path: str) -> int:
        return next((limit for pattern, limit in self._by_path if pattern.fullmatch(path)), self._default)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return
        limit = self.limit_for(scope["path"])
        declared = dict(scope["headers"]).get(b"content-length")
        if declared is not None and (not declared.isdigit() or int(declared) > limit):
            await JSONResponse({"detail": TOO_LARGE}, status_code=413)(scope, receive, send)
            return
        received = 0

        async def counted() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > limit:
                    raise HTTPException(413, TOO_LARGE)
            return message

        await self._app(scope, counted, send)
