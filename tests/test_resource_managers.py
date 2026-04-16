from __future__ import annotations

import pytest

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError, ValidationError
from netskopesdwan.models.download import DownloadResult
from netskopesdwan.models.resource import ResourceRecord
from tests.fixtures import (
    jwks_fixture,
    raw_object_fixture,
    resource_array_list_fixture,
    resource_detail_fixture,
    resource_envelope_list_fixture,
    site_command_output_fixture,
)


def test_client_wires_read_only_managers() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    assert client.address_groups.resource_path == "/v2/address-groups"
    assert client.audit_events.resource_path == "/v2/auditevents"
    assert client.applications.resource_path == "/v2/custom-apps"
    assert client.ca_certificates.resource_path == "/v2/ca-certificates"
    assert client.client_templates.resource_path == "/v2/client-templates"
    assert client.clients.resource_path == "/v2/clients"
    assert client.cloud_accounts.resource_path == "/v2/cloud-accounts"
    assert client.controller_operators.resource_path == "/v2/controller-operators"
    assert client.controllers.resource_path == "/v2/controllers"
    assert client.device_groups.resource_path == "/v2/device-groups"
    assert client.gateway_groups.resource_path == "/v2/gateway-groups"
    assert client.gateway_templates.resource_path == "/v2/gateway-templates"
    assert client.inventory_devices.resource_path == "/v2/inventory-devices"
    assert client.jwks.resource_path == "/v2/jwks.json"
    assert client.ntp_configs.resource_path == "/v2/ntp-configs"
    assert client.overlay_tags.resource_path == "/v2/overlay-tags"
    assert client.segments.resource_path == "/v2/segments"
    assert client.site_commands.resource_path == "/v2/site-commands"
    assert client.software.resource_path == "/v2/software-versions"
    assert client.tenants.resource_path == "/v2/tenants"
    assert client.user_groups.resource_path == "/v2/user-groups"
    assert client.users.resource_path == "/v2/users"
    assert client.vpn_peers.resource_path == "/v2/vpnpeers"
    assert client.policies.resource_path == "/v2/policies"
    assert client.radius_servers.resource_path == "/v2/radius-servers"


def test_device_groups_list_parses_paginated_envelope() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_envelope_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/device-groups"
        assert params is None
        return fixture

    client.transport.get = fake_get

    items = client.device_groups.list()

    assert [item.id for item in items] == ["res-001", "res-002"]
    assert items[0].name == "Resource One"
    assert items[1].raw == fixture["data"][1]
    assert client.device_groups.last_page_info == fixture["page_info"]
    assert client.device_groups.last_cursors is None


def test_address_groups_list_and_get_parse_resource_payloads() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    list_fixture = resource_array_list_fixture()
    detail_fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        if path == "/v2/address-groups":
            return list_fixture
        if path == "/v2/address-groups/ag-001":
            return detail_fixture
        raise AssertionError(f"Unexpected path: {path}")

    client.transport.get = fake_get

    items = client.address_groups.list()
    item = client.address_groups.get("ag-001")

    assert [entry.id for entry in items] == ["res-001", "res-002"]
    assert item.id == "res-001"


def test_address_groups_list_address_objects_parses_nested_resource_list() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_envelope_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/address-groups/ag-001/address-objects"
        return fixture

    client.transport.get = fake_get

    items = client.address_groups.list_address_objects("ag-001")

    assert [entry.id for entry in items] == ["res-001", "res-002"]


def test_address_groups_list_address_objects_forwards_query_params() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_envelope_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/address-groups/ag-001/address-objects"
        assert params == {
            "after": "cursor-1",
            "first": 25,
            "sort": "name",
            "filter": "name: Branch",
        }
        return fixture

    client.transport.get = fake_get

    items = client.address_groups.list_address_objects(
        "ag-001",
        after="cursor-1",
        first=25,
        sort="name",
        filter="name: Branch",
    )

    assert [entry.id for entry in items] == ["res-001", "res-002"]
    assert client.address_groups.last_page_info == fixture["page_info"]


def test_policies_list_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/policies"
        return fixture

    client.transport.get = fake_get

    items = client.policies.list()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_radius_server_get_parses_detail_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/radius-servers/rad-001"
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
        assert path == "/v2/client-templates"
        return fixture

    client.transport.get = fake_get

    items = client.client_templates.list()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_applications_helpers_parse_supported_endpoints() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    envelope_fixture = resource_envelope_list_fixture()
    array_fixture = resource_array_list_fixture()
    detail_fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        if path == "/v2/app-categories":
            return array_fixture
        if path == "/v2/custom-apps":
            return envelope_fixture
        if path == "/v2/custom-apps/app-001":
            return detail_fixture
        if path == "/v2/qosmos-apps":
            return array_fixture
        if path == "/v2/webroot-categories":
            return array_fixture
        raise AssertionError(f"Unexpected path: {path}")

    client.transport.get = fake_get

    assert [item.id for item in client.applications.list_categories()] == ["res-001", "res-002"]
    assert [item.id for item in client.applications.list_custom_apps()] == ["res-001", "res-002"]
    assert client.applications.get_custom_app("app-001").id == "res-001"
    assert [item.id for item in client.applications.list_qosmos_apps()] == ["res-001", "res-002"]
    assert [item.id for item in client.applications.list_webroot_categories()] == [
        "res-001",
        "res-002",
    ]


def test_audit_events_list_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/auditevents"
        assert params == {
            "filter": 'created_at>="2024-12-01T00:00:00-04:00" AND '
            'created_at<="2025-01-10T23:59:59-05:00"'
        }
        return fixture

    client.transport.get = fake_get

    items = client.audit_events.list(
        created_at_from="2024-12-01T00:00:00-04:00",
        created_at_to="2025-01-10T23:59:59-05:00",
    )

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_audit_events_list_includes_optional_filters() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/auditevents"
        assert params == {
            "filter": 'created_at>="2024-12-01T00:00:00-04:00" AND '
            'created_at<="2025-01-10T23:59:59-05:00" AND '
            "type: AUDIT AND subtype: AUDIT_TENANT AND activity: LOGIN"
        }
        return fixture

    client.transport.get = fake_get

    items = client.audit_events.list(
        created_at_from="2024-12-01T00:00:00-04:00",
        created_at_to="2025-01-10T23:59:59-05:00",
        type="AUDIT",
        subtype="AUDIT_TENANT",
        activity="LOGIN",
    )

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_audit_events_list_supports_standard_list_query_params() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_envelope_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/auditevents"
        assert params == {
            "after": "cursor-2",
            "first": 10,
            "sort": "-created_at",
            "filter": 'created_at>="2024-12-01T00:00:00Z" AND '
            'created_at<="2024-12-02T00:00:00Z" AND tenant_id: tenant-001',
        }
        return fixture

    client.transport.get = fake_get

    items = client.audit_events.list(
        created_at_from="2024-12-01T00:00:00Z",
        created_at_to="2024-12-02T00:00:00Z",
        after="cursor-2",
        first=10,
        sort="-created_at",
        filter="tenant_id: tenant-001",
    )

    assert [item.id for item in items] == ["res-001", "res-002"]
    assert client.audit_events.last_page_info == fixture["page_info"]


def test_audit_events_list_requires_created_at_from() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    with pytest.raises(ValidationError) as excinfo:
        client.audit_events.list(
            created_at_from="",
            created_at_to="2025-01-10T23:59:59-05:00",
        )

    assert "requires a bounded time range" in str(excinfo.value)
    assert "created_at_from" in str(excinfo.value)


def test_audit_events_list_requires_created_at_to() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    with pytest.raises(ValidationError) as excinfo:
        client.audit_events.list(
            created_at_from="2024-12-01T00:00:00-04:00",
            created_at_to="",
        )

    assert "requires a bounded time range" in str(excinfo.value)
    assert "created_at_to" in str(excinfo.value)


def test_audit_events_list_fails_on_malformed_payload() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/v2/auditevents"
        return {"data": {"id": "evt-001"}}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.audit_events.list(
            created_at_from="2024-12-01T00:00:00-04:00",
            created_at_to="2025-01-10T23:59:59-05:00",
        )

    assert "Audit event list response field 'data' must be a JSON array." in str(excinfo.value)


def test_clients_get_parses_detail_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/clients/client-001"
        return fixture

    client.transport.get = fake_get

    item = client.clients.get("client-001")

    assert item.id == "res-001"
    assert item.raw == fixture


def test_cloud_accounts_list_fails_when_payload_shape_is_invalid() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/v2/cloud-accounts"
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
        assert path == "/v2/controller-operators/op-001"
        return fixture

    client.transport.get = fake_get

    item = client.controller_operators.get("op-001")

    assert item.id == "res-001"
    assert item.raw == fixture


def test_controllers_get_operator_status_parses_raw_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = raw_object_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/controllers/controller-001/operator_status"
        return fixture

    client.transport.get = fake_get

    payload = client.controllers.get_operator_status("controller-001")

    assert payload == fixture


def test_controllers_get_operator_status_fails_on_non_object_payload() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/v2/controllers/controller-001/operator_status"
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
        assert path == "/v2/segments"
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
        assert path == "/v2/vpnpeers"
        return {"data": {"id": "vpn-001"}}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.vpn_peers.list()

    assert "field 'data' must be a JSON array" in str(excinfo.value)


def test_gateway_templates_get_fails_when_id_is_missing() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/v2/gateway-templates/template-001"
        return {"name": "Template One"}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.gateway_templates.get("template-001")

    assert "required 'id' field" in str(excinfo.value)


def test_ca_certificates_list_and_get_parse_resource_payloads() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    list_fixture = resource_envelope_list_fixture()
    detail_fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        if path == "/v2/ca-certificates":
            return list_fixture
        if path == "/v2/ca-certificates/ca-001":
            return detail_fixture
        raise AssertionError(f"Unexpected path: {path}")

    client.transport.get = fake_get

    items = client.ca_certificates.list()
    item = client.ca_certificates.get("ca-001")

    assert [entry.id for entry in items] == ["res-001", "res-002"]
    assert item.id == "res-001"


def test_site_commands_get_output_returns_text() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = site_command_output_fixture()

    def fake_get_download(path: str, *, params=None):
        assert path == "/v2/site-command/cmd-001/output/stdout"
        return DownloadResult(
            content=fixture,
            content_type="application/octet-stream",
            content_disposition='attachment; filename="stdout.txt"',
            filename="stdout.txt",
        )

    client.transport.get_download = fake_get_download

    payload = client.site_commands.get_output("cmd-001", "stdout")

    assert isinstance(payload, DownloadResult)
    assert payload.content == fixture
    assert payload.filename == "stdout.txt"


def test_site_commands_get_parses_detail_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_detail_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/site-commands/cmd-001"
        return fixture

    client.transport.get = fake_get

    item = client.site_commands.get("cmd-001")

    assert item.id == "res-001"


def test_software_list_versions_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/software-versions"
        return fixture

    client.transport.get = fake_get

    items = client.software.list_versions()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_software_list_downloads_parses_paginated_envelope() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_envelope_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/software-downloads"
        return fixture

    client.transport.get = fake_get

    items = client.software.list_downloads()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_jwks_get_parses_raw_object() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = jwks_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/jwks.json"
        return fixture

    client.transport.get = fake_get

    payload = client.jwks.get()

    assert payload == fixture


def test_jwks_get_fails_on_non_object_payload() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/v2/jwks.json"
        return ["invalid"]

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.jwks.get()

    assert "Jwks response must be a top-level JSON object." in str(excinfo.value)


@pytest.mark.parametrize(
    ("manager_attr", "call_args"),
    [
        ("audit_events", ("evt-001",)),
        ("inventory_devices", ("inv-001",)),
        ("software", ("ver-001",)),
    ],
)
def test_list_only_managers_raise_clear_attribute_error(
    manager_attr: str, call_args: tuple[str, ...]
) -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    manager = getattr(client, manager_attr)

    with pytest.raises(AttributeError) as excinfo:
        manager.get(*call_args)

    assert "does not support get(id)" in str(excinfo.value)


def test_tenants_list_parses_top_level_array() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")
    fixture = resource_array_list_fixture()

    def fake_get(path: str, *, params=None):
        assert path == "/v2/tenants"
        return fixture

    client.transport.get = fake_get

    items = client.tenants.list()

    assert [item.id for item in items] == ["res-001", "res-002"]


def test_user_groups_get_fails_when_id_is_missing() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/v2/user-groups/group-001"
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
        assert path == "/v2/users"
        return {"data": {"id": "user-001"}}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.users.list()

    assert "User list response field 'data' must be a JSON array." in str(excinfo.value)
