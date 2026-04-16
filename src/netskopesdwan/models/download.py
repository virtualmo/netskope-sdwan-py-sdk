from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DownloadResult:
    """Binary download payload plus selected response metadata."""

    content: bytes
    content_type: str | None = None
    content_disposition: str | None = None
    filename: str | None = None
