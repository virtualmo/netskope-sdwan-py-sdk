from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DownloadResult:
    content: bytes
    content_type: str | None = None
    content_disposition: str | None = None
    filename: str | None = None
