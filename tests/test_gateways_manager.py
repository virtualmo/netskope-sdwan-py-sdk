from __future__ import annotations

import pytest

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError
from netskopesdwan.managers.gateways import (
    GATEWAYS_PATH,
    GATEWAY_BY_ID_PATH,
    GATEWAY_LOCALUI_PASSWORD_PATH,
    GATEWAY_SSH_PASSWORD_PATH,
)
from netskopesdwan.models.gateway import Gateway
from tests.fixtures import (
    gateway_detail_response_fixture,
    gateway_list_response_fixture,
    gateway_password_fixture,
)


def test_gateways_manager_list_parses_paginated_envelope() -> None:
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
    assert client.gateways._last_page_info == fixture["page_info"]
    assert client.gateways.last_page_info == fixture["page_info"]
    assert client.gateways.last_cursors is None


def test_gateways_manager_list_forwards_standard_query_params() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = gateway_list_response_fixture()

    def fake_get(path: str, *, params=None):
        assert path == GATEWAYS_PATH
        assert params == {
            "after": "cursor-1",
            "first": 50,
            "sort": "name",
            "filter": "name: Branch",
        }
        return fixture

    client.transport.get = fake_get

    gateways = client.gateways.list(
        after="cursor-1",
        first=50,
        sort="name",
        filter="name: Branch",
    )

    assert [item.id for item in gateways] == ["gw-001", "gw-002"]


def test_gateways_manager_list_fails_when_list_field_is_missing() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == GATEWAYS_PATH
        return {"page_info": {"page": 1}, "request_id": "req-123"}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.gateways.list()

    message = str(excinfo.value)
    assert "Expected 'data' or 'items'" in message
    assert "Top-level keys: page_info, request_id" in message


def test_gateways_manager_list_fails_when_list_field_type_is_malformed() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == GATEWAYS_PATH
        return {"page_info": {"page": 1}, "data": {"id": "gw-001"}}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.gateways.list()

    assert "field 'data' must be a JSON array" in str(excinfo.value)


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


def test_gateways_manager_password_helper_methods_are_available() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    assert callable(client.gateways.get_localui_password)
    assert callable(client.gateways.get_ssh_password)


def test_gateways_manager_get_localui_password_parses_top_level_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = gateway_password_fixture()

    def fake_get(path: str, *, params=None):
        assert path == GATEWAY_LOCALUI_PASSWORD_PATH.format(id="gw-001")
        return fixture

    client.transport.get = fake_get

    payload = client.gateways.get_localui_password("gw-001")

    assert payload == fixture


def test_gateways_manager_get_ssh_password_parses_top_level_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = gateway_password_fixture()

    def fake_get(path: str, *, params=None):
        assert path == GATEWAY_SSH_PASSWORD_PATH.format(id="gw-001")
        return fixture

    client.transport.get = fake_get

    payload = client.gateways.get_ssh_password("gw-001")

    assert payload == fixture


def test_gateways_manager_password_helpers_fail_on_non_object_payload() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == GATEWAY_LOCALUI_PASSWORD_PATH.format(id="gw-001")
        return ["invalid"]

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.gateways.get_localui_password("gw-001")

    assert "Gateway local UI password response must be a top-level JSON object." in str(
        excinfo.value
    )
