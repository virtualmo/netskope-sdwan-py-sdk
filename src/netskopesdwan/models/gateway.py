from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Gateway:
    id: str
    name: str | None = None
    status: str | None = None
    region: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Gateway":
        return cls(
            id=str(data.get("id") or data.get("_id") or ""),
            name=_to_optional_str(data.get("name")),
            status=_to_optional_str(data.get("status")),
            region=_to_optional_str(data.get("region")),
        )


def _to_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
