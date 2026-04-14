from __future__ import annotations

import pytest

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError
from netskopesdwan.managers.gateways import GATEWAYS_PATH, GATEWAY_BY_ID_PATH
from netskopesdwan.models.gateway import Gateway
from tests.fixtures import gateway_detail_response_fixture, gateway_list_response_fixture


def test_gateways_manager_list_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = gateway_list_response_fixture()

    def fake_get(path: str, *, params=None):
        assert path == GATEWAYS_PATH
        return fixture

    client.transport.get = fake_get

    gateways = client.gateways.list()

    assert [item.id for item in gateways] == ["gw-001", "gw-002"]
    assert gateways[0].managed is True
    assert gateways[1].is_activated is False


def test_gateways_manager_list_fails_on_non_array_payload() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == GATEWAYS_PATH
        return {"id": "gw-001"}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.gateways.list()

    assert "top-level JSON array" in str(excinfo.value)


def test_gateways_manager_get_parses_top_level_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = gateway_detail_response_fixture()

    def fake_get(path: str, *, params=None):
        assert path == GATEWAY_BY_ID_PATH.format(id="gw-001")
        return fixture

    client.transport.get = fake_get
    gateway = client.gateways.get("gw-001")

    assert isinstance(gateway, Gateway)
    assert gateway.id == "gw-001"
    assert gateway.overlay_id == "overlay-1"
    assert gateway.created_at == "2024-01-01T00:00:00Z"
    assert gateway.modified_at == "2024-01-02T00:00:00Z"
    assert isinstance(gateway.created_at, str)
    assert isinstance(gateway.modified_at, str)
    assert gateway.device_config_raw == fixture["device_config_raw"]


def test_gateways_manager_get_fails_when_id_missing() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == GATEWAY_BY_ID_PATH.format(id="gw-001")
        return {"name": "Branch Gateway 1"}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.gateways.get("gw-001")

    assert "required 'id' field" in str(excinfo.value)


def test_gateway_adapter_ignores_legacy_device_config_field() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == GATEWAY_BY_ID_PATH.format(id="gw-001")
        return {
            "id": "gw-001",
            "name": "Branch Gateway 1",
            "device_config": {"hostname": "legacy-shape"},
        }

    client.transport.get = fake_get
    gateway = client.gateways.get("gw-001")

    assert gateway.device_config_raw is None
