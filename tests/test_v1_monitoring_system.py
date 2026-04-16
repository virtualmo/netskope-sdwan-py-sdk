from __future__ import annotations

from netskopesdwan import SDWANClient


def assert_system_endpoint(
    method_name: str,
    expected_path: str,
    fixture: dict[str, object],
) -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == expected_path
        assert params is None
        return fixture

    client.transport.get = fake_get

    method = getattr(client.v1.monitoring, method_name)
    payload = method("gw-123")

    assert payload == fixture


def test_get_system_load() -> None:
    assert_system_endpoint(
        "get_system_load",
        "/monitoring/gateways/gw-123/system/load",
        {"load": 0.5},
    )


def test_get_system_lte() -> None:
    assert_system_endpoint(
        "get_system_lte",
        "/monitoring/gateways/gw-123/system/lte",
        {"signal": -80},
    )


def test_get_system_memory() -> None:
    assert_system_endpoint(
        "get_system_memory",
        "/monitoring/gateways/gw-123/system/memory",
        {"used_percent": 42},
    )


def test_get_system_uptime() -> None:
    assert_system_endpoint(
        "get_system_uptime",
        "/monitoring/gateways/gw-123/system/uptime",
        {"uptime_seconds": 12345},
    )


def test_get_system_wifi() -> None:
    assert_system_endpoint(
        "get_system_wifi",
        "/monitoring/gateways/gw-123/system/wifi",
        {"radios": []},
    )
