from __future__ import annotations

import json

import pytest
import requests

from netskopesdwan.exceptions import (
    APIResponseError,
    AuthenticationError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ValidationError,
)
from netskopesdwan.transport import Transport


@pytest.mark.parametrize(
    ("status_code", "expected_exception"),
    [
        (400, ValidationError),
        (401, AuthenticationError),
        (403, PermissionDeniedError),
        (404, NotFoundError),
        (422, ValidationError),
        (429, RateLimitError),
        (500, APIResponseError),
    ],
)
def test_transport_maps_http_statuses(status_code: int, expected_exception: type[Exception]) -> None:
    transport = Transport(
        base_url="https://tenant.api.infiot.net",
        api_token="TOKEN",
        timeout=30,
        verify_ssl=True,
    )

    response = _build_response(
        status_code=status_code,
        body={"message": "problem details"},
        url="https://tenant.api.infiot.net/gateways",
        method="GET",
    )

    with pytest.raises(expected_exception) as excinfo:
        transport._raise_for_status(response)

    message = str(excinfo.value)
    assert "GET https://tenant.api.infiot.net/gateways returned HTTP" in message
    assert "problem details" in message


def test_transport_uses_text_body_when_json_is_unavailable() -> None:
    transport = Transport(
        base_url="https://tenant.api.infiot.net",
        api_token="TOKEN",
        timeout=30,
        verify_ssl=True,
    )
    response = _build_response(
        status_code=500,
        body="plain failure body",
        url="https://tenant.api.infiot.net/gateways",
        method="POST",
        content_type="text/plain",
    )

    with pytest.raises(APIResponseError) as excinfo:
        transport._raise_for_status(response)

    message = str(excinfo.value)
    assert "POST https://tenant.api.infiot.net/gateways returned HTTP 500" in message
    assert "plain failure body" in message


def _build_response(
    *,
    status_code: int,
    body: dict[str, str] | str,
    url: str,
    method: str,
    content_type: str = "application/json",
) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response.url = url
    response.request = requests.Request(method=method, url=url).prepare()
    response.headers["Content-Type"] = content_type
    if isinstance(body, dict):
        response._content = json.dumps(body).encode("utf-8")
    else:
        response._content = body.encode("utf-8")
    return response
