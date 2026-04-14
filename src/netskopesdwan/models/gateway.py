from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Gateway:
    id: str
    name: str | None = None
    managed: bool | None = None
    is_activated: bool | None = None
    overlay_id: str | None = None
    created_at: str | None = None
    modified_at: str | None = None
    device_config_raw: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Gateway":
        return cls(
            id=str(data.get("id") or ""),
            name=_to_optional_str(data.get("name")),
            managed=_to_optional_bool(data.get("managed")),
            is_activated=_to_optional_bool(data.get("is_activated")),
            overlay_id=_to_optional_str(data.get("overlay_id")),
            created_at=_to_optional_str(data.get("created_at")),
            modified_at=_to_optional_str(data.get("modified_at")),
            device_config_raw=_to_optional_dict(data.get("device_config_raw")),
        )


def _to_optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _to_optional_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


def _to_optional_dict(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    return None
