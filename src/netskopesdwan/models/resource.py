from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ResourceRecord:
    id: str
    name: str | None = None
    raw: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ResourceRecord:
        return cls(
            id=_to_required_id(data),
            name=_to_optional_str(data.get("name")),
            raw=dict(data),
        )


def _to_required_id(data: dict[str, Any]) -> str:
    value = data.get("id")
    if value is None:
        return ""
    text = str(value).strip()
    return text


def _to_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
