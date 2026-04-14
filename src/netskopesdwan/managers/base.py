from __future__ import annotations

from typing import Any

from ..transport import Transport


class BaseManager:
    resource_path: str = ""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def _get(self, path: str = "", *, params: dict[str, Any] | None = None) -> Any:
        if path.startswith("/"):
            return self._transport.get(path, params=params)
        resource = self.resource_path.rstrip("/")
        suffix = f"/{path.lstrip('/')}" if path else ""
        return self._transport.get(f"{resource}{suffix}", params=params)
