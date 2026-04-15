from __future__ import annotations

import pytest

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError
from netskopesdwan.models.resource import ResourceRecord
from tests.fixtures import (
    raw_object_fixture,
    resource_array_list_fixture,
    resource_detail_fixture,
    resource_envelope_list_fixture,
    site_command_output_fixture,
)


def test_client_wires_read_only_managers() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    assert client.audit_events.resource_path == "/auditevents"
    assert client.client_templates.resource_path == "/client-templates"
    assert client.clients.resource_path == "/clients"
    assert client.cloud_accounts.resource_path == "/cloud-accounts"
    assert client.controller_operators.resource_path == "/controller-operators"
    assert client.controllers.resource_path == "/controllers"
    assert client.device_groups.resource_path == "/device-groups"
    assert client.gateway_groups.resource_path == "/gateway-groups"
    assert client.gateway_templates.resource_path == "/gateway-templates"
    assert client.inventory_devices.resource_path == "/inventory-devices"
    assert client.ntp_configs.resource_path == "/ntp-configs"
    assert client.overlay_tags.resource_path == "/overlay-tags"
    assert client.segments.resource_path == "/segments"
    assert client.site_commands.resource_path == "/site-commands"
    assert client.software.resource_path == "/software-versions"
    assert client.tenants.resource_path == "/tenants"
    assert client.user_groups.resource_path == "/user-groups"
    assert client.users.resource_path == "/users"
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


def test_client_templates_list_parses_paginated_envelope() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_envelope_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/client-templates"
        return fixture

    client.transport.get = fake_get

    items = client.client_templates.list()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_audit_events_list_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/auditevents"
        return fixture

    client.transport.get = fake_get

    items = client.audit_events.list()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_clients_get_parses_detail_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/clients/client-001"
        return fixture

    client.transport.get = fake_get

    item = client.clients.get("client-001")

    assert item.id == "res-001"
    assert item.raw == fixture


def test_cloud_accounts_list_fails_when_payload_shape_is_invalid() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/cloud-accounts"
        return "not-json-object"

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.cloud_accounts.list()

    assert "Cloud account list response must be a top-level JSON array or object." in str(
        excinfo.value
    )


def test_controller_operators_get_parses_detail_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/controller-operators/op-001"
        return fixture

    client.transport.get = fake_get

    item = client.controller_operators.get("op-001")

    assert item.id == "res-001"
    assert item.raw == fixture


def test_controllers_get_operator_status_parses_raw_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = raw_object_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/controllers/controller-001/operator_status"
        return fixture

    client.transport.get = fake_get

    payload = client.controllers.get_operator_status("controller-001")

    assert payload == fixture


def test_controllers_get_operator_status_fails_on_non_object_payload() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/controllers/controller-001/operator_status"
        return ["invalid"]

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.controllers.get_operator_status("controller-001")

    assert "Controller operator status response must be a top-level JSON object." in str(
        excinfo.value
    )


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


def test_site_commands_get_output_returns_text() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = site_command_output_fixture()

    def fake_get_text(path: str, *, params=None):
        assert path == "/site-command/cmd-001/output/stdout"
        return fixture

    client.transport.get_text = fake_get_text

    payload = client.site_commands.get_output("cmd-001", "stdout")

    assert payload == fixture


def test_site_commands_get_parses_detail_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/site-commands/cmd-001"
        return fixture

    client.transport.get = fake_get

    item = client.site_commands.get("cmd-001")

    assert item.id == "res-001"


def test_software_list_versions_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/software-versions"
        return fixture

    client.transport.get = fake_get

    items = client.software.list_versions()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_software_list_downloads_parses_paginated_envelope() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_envelope_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/software-downloads"
        return fixture

    client.transport.get = fake_get

    items = client.software.list_downloads()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_tenants_list_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/tenants"
        return fixture

    client.transport.get = fake_get

    items = client.tenants.list()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_user_groups_get_fails_when_id_is_missing() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/user-groups/group-001"
        return {"name": "Group One"}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.user_groups.get("group-001")

    assert "User group detail response did not include the required 'id' field." in str(
        excinfo.value
    )


def test_users_list_fails_when_list_field_type_is_invalid() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/users"
        return {"data": {"id": "user-001"}}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.users.list()

    assert "User list response field 'data' must be a JSON array." in str(excinfo.value)
