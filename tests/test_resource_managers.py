from __future__ import annotations

import pytest

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError
from netskopesdwan.models.resource import ResourceRecord
from tests.fixtures import (
    resource_array_list_fixture,
    resource_detail_fixture,
    resource_envelope_list_fixture,
)


def test_client_wires_read_only_managers() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    assert client.device_groups.resource_path == "/device-groups"
    assert client.gateway_groups.resource_path == "/gateway-groups"
    assert client.gateway_templates.resource_path == "/gateway-templates"
    assert client.inventory_devices.resource_path == "/inventory-devices"
    assert client.ntp_configs.resource_path == "/ntp-configs"
    assert client.overlay_tags.resource_path == "/overlay-tags"
    assert client.segments.resource_path == "/segments"
    assert client.vpn_peers.resource_path == "/vpnpeers"
    assert client.policies.resource_path == "/policies"
    assert client.radius_servers.resource_path == "/radius-servers"


def test_device_groups_list_parses_paginated_envelope() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_envelope_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/device-groups"
        return fixture

    client.transport.get = fake_get

    items = client.device_groups.list()

    assert [item.id for item in items] == ["res-001", "res-002"]
    assert items[0].name == "Resource One"
    assert items[1].raw == fixture["data"][1]


def test_policies_list_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/policies"
        return fixture

    client.transport.get = fake_get

    items = client.policies.list()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_radius_server_get_parses_detail_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/radius-servers/rad-001"
        return fixture

    client.transport.get = fake_get

    item = client.radius_servers.get("rad-001")

    assert isinstance(item, ResourceRecord)
    assert item.id == "res-001"
    assert item.name == "Resource One"
    assert item.raw == fixture


def test_segments_list_fails_when_envelope_list_field_is_missing() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/segments"
        return {"page_info": {"page": 1}, "request_id": "req-001"}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.segments.list()

    message = str(excinfo.value)
    assert "Segment list response did not include a valid list field" in message
    assert "Top-level keys: page_info, request_id" in message


def test_vpn_peers_list_fails_when_list_field_type_is_invalid() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/vpnpeers"
        return {"data": {"id": "vpn-001"}}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.vpn_peers.list()

    assert "field 'data' must be a JSON array" in str(excinfo.value)


def test_gateway_templates_get_fails_when_id_is_missing() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/gateway-templates/template-001"
        return {"name": "Template One"}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.gateway_templates.get("template-001")

    assert "required 'id' field" in str(excinfo.value)
