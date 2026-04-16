from __future__ import annotations

import pytest

from netskopesdwan import SDWANClient, V1MonitoringWANMetric
from netskopesdwan.exceptions import APIResponseError
from netskopesdwan.models.resource import ResourceRecord


def test_client_wires_v1_namespace() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    assert client.v1.edges.resource_path == "/edges"
    assert hasattr(client.v1, "monitoring")
    assert hasattr(client.v1, "users")


def test_v1_edges_list_and_get_parse_resource_records() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        if path == "/edges":
            assert params == {
                "afterCursor": "cursor-a",
                "beforeCursor": "cursor-b",
                "maxItems": 10,
                "childTenantId": "tenant-123",
                "getTemplates": True,
            }
            return {
                "data": [{"id": "edge-001", "name": "Edge One"}],
                "startCursor": "cursor-a",
                "endCursor": "cursor-b",
                "firstPage": True,
                "lastPage": False,
            }
        if path == "/edges/edge-001":
            assert params == {"childTenantId": "tenant-123"}
            return {"id": "edge-001", "name": "Edge One"}
        raise AssertionError(f"Unexpected path: {path}")

    client.transport.get = fake_get

    items = client.v1.edges.list(
        after_cursor="cursor-a",
        before_cursor="cursor-b",
        max_items=10,
        child_tenant_id="tenant-123",
        get_templates=True,
    )
    item = client.v1.edges.get("edge-001", child_tenant_id="tenant-123")

    assert isinstance(items[0], ResourceRecord)
    assert items[0].id == "edge-001"
    assert item.id == "edge-001"
    assert client.v1.edges.last_cursors == {
        "startCursor": "cursor-a",
        "endCursor": "cursor-b",
        "firstPage": True,
        "lastPage": False,
    }


def test_v1_edges_interface_helpers_parse_raw_payloads() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        if path == "/edges/edge-001/interfaces":
            assert params == {"childTenantId": "tenant-123"}
            return [{"name": "wan0"}]
        if path == "/edges/edge-001/interfaces/wan0":
            assert params == {"childTenantId": "tenant-123"}
            return {"name": "wan0"}
        if path == "/gateways/edge-001/interfaces":
            assert params == {"childTenantId": "tenant-123"}
            return [{"name": "lan0"}]
        if path == "/gateways/edge-001/interfaces/lan0":
            assert params == {"childTenantId": "tenant-123"}
            return {"name": "lan0"}
        raise AssertionError(f"Unexpected path: {path}")

    client.transport.get = fake_get

    assert client.v1.edges.list_interfaces(
        "edge-001",
        child_tenant_id="tenant-123",
    ) == [{"name": "wan0"}]
    assert client.v1.edges.get_interface(
        "edge-001",
        "wan0",
        child_tenant_id="tenant-123",
    ) == {"name": "wan0"}
    assert client.v1.edges.list_gateway_interfaces(
        "edge-001",
        child_tenant_id="tenant-123",
    ) == [{"name": "lan0"}]
    assert client.v1.edges.get_gateway_interface(
        "edge-001",
        "lan0",
        child_tenant_id="tenant-123",
    ) == {"name": "lan0"}


def test_v1_monitoring_helpers_parse_raw_payloads() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        if path.endswith("/device_flows_totals"):
            assert params == {
                "childTenantId": "tenant-123",
                "startDatetime": "2024-01-01T00:00:00Z",
                "endDatetime": "2024-01-02T00:00:00Z",
                "ip": "10.0.0.1",
            }
            return {"total": 1}
        if path.endswith("/interfaces_latest"):
            assert params == {"childTenantId": "tenant-123"}
            return [{"name": "wan0"}]
        if path.endswith("/system/load"):
            assert params == {
                "childTenantId": "tenant-123",
                "startDatetime": "2024-01-01T00:00:00Z",
                "endDatetime": "2024-01-02T00:00:00Z",
                "timeSlots": 24,
            }
            return {"cpu": 10}
        raise AssertionError(f"Unexpected path: {path}")

    client.transport.get = fake_get

    assert client.v1.monitoring.get_device_flows_totals(
        "gw-001",
        child_tenant_id="tenant-123",
        start_datetime="2024-01-01T00:00:00Z",
        end_datetime="2024-01-02T00:00:00Z",
        ip="10.0.0.1",
    ) == {"total": 1}
    assert client.v1.monitoring.get_interfaces_latest("gw-001", child_tenant_id="tenant-123") == [
        {"name": "wan0"}
    ]
    assert client.v1.monitoring.get_system_load(
        "gw-001",
        child_tenant_id="tenant-123",
        start_datetime="2024-01-01T00:00:00Z",
        end_datetime="2024-01-02T00:00:00Z",
        time_slots=24,
    ) == {"cpu": 10}


def test_v1_monitoring_get_paths_links_accepts_metric_enum() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/monitoring/gateways/gw-001/wan/paths_links"
        assert params == {
            "startDatetime": "2024-01-01T00:00:00Z",
            "endDatetime": "2024-01-02T00:00:00Z",
            "metric": "latency",
        }
        return [{"metric": "latency"}]

    client.transport.get = fake_get

    payload = client.v1.monitoring.get_paths_links(
        "gw-001",
        start_datetime="2024-01-01T00:00:00Z",
        end_datetime="2024-01-02T00:00:00Z",
        metric=V1MonitoringWANMetric.LATENCY,
    )

    assert payload == [{"metric": "latency"}]


def test_v1_monitoring_get_paths_links_accepts_metric_string() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/monitoring/gateways/gw-001/wan/paths_links"
        assert params == {
            "startDatetime": "2024-01-01T00:00:00Z",
            "endDatetime": "2024-01-02T00:00:00Z",
            "metric": "latency",
        }
        return [{"metric": "latency"}]

    client.transport.get = fake_get

    payload = client.v1.monitoring.get_paths_links(
        "gw-001",
        start_datetime="2024-01-01T00:00:00Z",
        end_datetime="2024-01-02T00:00:00Z",
        metric="latency",
    )

    assert payload == [{"metric": "latency"}]


def test_v1_users_get_groups_parses_resource_records() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/users/user-001/groups"
        assert params == {
            "afterCursor": "cursor-a",
            "beforeCursor": "cursor-b",
            "maxItems": 20,
        }
        return {
            "data": [{"id": "group-001", "name": "Group One"}],
            "startCursor": "cursor-a",
            "endCursor": "cursor-b",
            "firstPage": True,
            "lastPage": True,
        }

    client.transport.get = fake_get

    items = client.v1.users.get_groups(
        "user-001",
        after_cursor="cursor-a",
        before_cursor="cursor-b",
        max_items=20,
    )

    assert isinstance(items[0], ResourceRecord)
    assert items[0].id == "group-001"


def test_v1_edges_list_fails_on_malformed_payload() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/edges"
        return {"id": "edge-001"}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.v1.edges.list()

    assert "Expected one of ('data', 'items')" in str(excinfo.value)
