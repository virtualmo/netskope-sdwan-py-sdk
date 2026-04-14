from __future__ import annotations

from typing import Any

import requests

from .exceptions import (
    APIResponseError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ValidationError,
)


class Transport:
    def __init__(
        self,
        *,
        base_url: str,
        api_token: str,
        timeout: float | int | None,
        verify_ssl: bool,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"Bearer {api_token}",
            }
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        response = self.session.request(
            method=method.upper(),
            url=f"{self.base_url}/{path.lstrip('/')}",
            params=params,
            json=json_body,
            timeout=self.timeout,
            verify=self.verify_ssl,
        )
        self._raise_for_status(response)

        if response.status_code == 204 or not response.content:
            return None

        try:
            return response.json()
        except ValueError as exc:
            raise APIResponseError("The API returned a non-JSON response.") from exc

    def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self.request("GET", path, params=params)

    def _raise_for_status(self, response: requests.Response) -> None:
        status = response.status_code
        if 200 <= status < 300:
            return

        message = _build_error_message(response)
        if status == 401:
            raise AuthenticationError(message)
        if status == 403:
            raise PermissionDeniedError(message)
        if status == 404:
            raise NotFoundError(message)
        if status == 400:
            raise ValidationError(message)
        if status == 422:
            raise ValidationError(message)
        if status == 429:
            raise RateLimitError(message)
        raise APIResponseError(message)


def _build_error_message(response: requests.Response) -> str:
    default_message = f"API request failed with status {response.status_code}."
    error_code: str | None = None
    request_id: str | None = None
    try:
        payload = response.json()
    except ValueError:
        text = response.text.strip()
        detail = text or default_message
    else:
        detail = default_message
        if isinstance(payload, dict):
            message = payload.get("message")
            if isinstance(message, str) and message.strip():
                detail = message.strip()
            else:
                for key in ("error", "detail"):
                    value = payload.get(key)
                    if isinstance(value, str) and value.strip():
                        detail = value.strip()
                        break
            error_code_value = payload.get("error_code")
            if isinstance(error_code_value, str) and error_code_value.strip():
                error_code = error_code_value.strip()
            request_id_value = payload.get("request_id")
            if isinstance(request_id_value, str) and request_id_value.strip():
                request_id = request_id_value.strip()

    request = response.request
    method = request.method if request is not None else "UNKNOWN"
    url = request.url if request is not None else "unknown URL"
    extras: list[str] = []
    if error_code:
        extras.append(f"error_code={error_code}")
    if request_id:
        extras.append(f"request_id={request_id}")
    suffix = f" ({', '.join(extras)})" if extras else ""
    return f"{method} {url} returned HTTP {response.status_code}: {detail}{suffix}"
