from __future__ import annotations

import os
from dataclasses import dataclass

from .exceptions import ConfigurationError


ENV_BASE_URL = "NETSKOPESDWAN_BASE_URL"
ENV_TENANT_URL = "NETSKOPESDWAN_TENANT_URL"
ENV_API_TOKEN = "NETSKOPESDWAN_API_TOKEN"
ENV_TIMEOUT = "NETSKOPESDWAN_TIMEOUT"


@dataclass(slots=True)
class ClientSettings:
    base_url: str | None
    tenant_url: str | None
    api_token: str
    timeout: float | int | None
    verify_ssl: bool
    sdwan_tenant_name: str | None


def load_settings(
    *,
    base_url: str | None,
    tenant_url: str | None,
    api_token: str | None,
    timeout: float | int | None,
    verify_ssl: bool,
    sdwan_tenant_name: str | None,
) -> ClientSettings:
    resolved_base_url = base_url or _read_env(ENV_BASE_URL)
    resolved_tenant_url = tenant_url or _read_env(ENV_TENANT_URL)
    resolved_api_token = api_token or _read_env(ENV_API_TOKEN)
    resolved_timeout = timeout if timeout is not None else _read_timeout()

    if not resolved_base_url and not resolved_tenant_url:
        raise ConfigurationError(
            "Either base_url or tenant_url must be provided, either directly or via environment "
            f"variables {ENV_BASE_URL} / {ENV_TENANT_URL}."
        )

    if not resolved_api_token:
        raise ConfigurationError(
            "api_token is required, either via the constructor or the "
            f"{ENV_API_TOKEN} environment variable."
        )

    if resolved_timeout is not None and resolved_timeout <= 0:
        raise ConfigurationError("timeout must be greater than 0 when provided.")

    return ClientSettings(
        base_url=resolved_base_url,
        tenant_url=resolved_tenant_url,
        api_token=resolved_api_token,
        timeout=resolved_timeout,
        verify_ssl=verify_ssl,
        sdwan_tenant_name=sdwan_tenant_name,
    )


def _read_env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _read_timeout() -> float | int | None:
    raw_timeout = _read_env(ENV_TIMEOUT)
    if raw_timeout is None:
        return None

    try:
        value = float(raw_timeout)
    except ValueError as exc:
        raise ConfigurationError(
            f"{ENV_TIMEOUT} must be a valid integer or float, got {raw_timeout!r}."
        ) from exc

    return int(value) if value.is_integer() else value
