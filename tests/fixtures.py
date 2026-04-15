from __future__ import annotations

from typing import Any


def gateway_list_response_fixture() -> dict[str, Any]:
    return {
        "page_info": {
            "page": 1,
            "page_size": 2,
            "total": 2,
        },
        "data": [
            {
                "id": "gw-001",
                "name": "Branch Gateway 1",
                "managed": True,
                "is_activated": True,
                "overlay_id": "overlay-1",
                "created_at": "2024-01-01T00:00:00Z",
                "modified_at": "2024-01-02T00:00:00Z",
            },
            {
                "id": "gw-002",
                "name": "Branch Gateway 2",
                "managed": False,
                "is_activated": False,
                "overlay_id": "overlay-2",
                "created_at": "2024-02-01T00:00:00Z",
                "modified_at": "2024-02-02T00:00:00Z",
            },
        ],
    }


def gateway_detail_response_fixture() -> dict[str, Any]:
    return {
        "id": "gw-001",
        "name": "Branch Gateway 1",
        "managed": True,
        "is_activated": True,
        "overlay_id": "overlay-1",
        "created_at": "2024-01-01T00:00:00Z",
        "modified_at": "2024-01-02T00:00:00Z",
        "device_config_raw": {
            "hostname": "branch-gateway-1",
            "interfaces": [],
        },
    }


def error_response_fixture() -> dict[str, str]:
    return {
        "message": "Gateway lookup failed",
        "error_code": "GW_NOT_FOUND",
        "request_id": "req-sanitized-001",
    }


def resource_envelope_list_fixture() -> dict[str, Any]:
    return {
        "page_info": {"page": 1, "page_size": 2},
        "data": [
            {"id": "res-001", "name": "Resource One"},
            {"id": "res-002", "name": "Resource Two", "description": "ignored"},
        ],
    }


def resource_array_list_fixture() -> list[dict[str, Any]]:
    return [
        {"id": "res-001", "name": "Resource One"},
        {"id": "res-002", "name": "Resource Two"},
    ]


def resource_detail_fixture() -> dict[str, Any]:
    return {"id": "res-001", "name": "Resource One", "host": "redacted"}


def raw_object_fixture() -> dict[str, Any]:
    return {"status": "ok", "operator": "sanitized", "updated_at": "2024-01-01T00:00:00Z"}


def site_command_output_fixture() -> str:
    return "command output line 1\ncommand output line 2\n"


def jwks_fixture() -> dict[str, Any]:
    return {
        "keys": [
            {
                "kid": "sanitized-key-1",
                "kty": "RSA",
                "use": "sig",
            }
        ]
    }
