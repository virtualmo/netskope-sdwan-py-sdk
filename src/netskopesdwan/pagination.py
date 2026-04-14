from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Page(Generic[T]):
    """Minimal pagination container for future expansion."""

    items: list[T]
    next_token: str | None = None
