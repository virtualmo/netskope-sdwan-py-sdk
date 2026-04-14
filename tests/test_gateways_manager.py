from __future__ import annotations

import pytest

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError
from netskopesdwan.models.gateway import Gateway


def test_gateways_manager_list_and_get() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        if path == "/gateways":
            return {
                "items": [
                    {"id": "gw-1", "name": "Gateway One", "status": "online", "region": "eu-west"},
                    {"id": "gw-2", "name": "Gateway Two"},
                ]
            }
        if path == "/gateways/gw-1":
            return {"data": {"id": "gw-1", "name": "Gateway One", "status": "online"}}
        raise AssertionError(f"Unexpected path: {path}")

    client.transport.get = fake_get

    gateways = client.gateways.list()
    gateway = client.gateways.get("gw-1")

    assert [item.id for item in gateways] == ["gw-1", "gw-2"]
    assert gateways[0].status == "online"
    assert isinstance(gateway, Gateway)
    assert gateway.id == "gw-1"
    assert gateway.name == "Gateway One"


def test_gateways_manager_handles_nested_collection_wrappers() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/gateways"
        return {
            "data": {
                "items": [
                    {"id": "gw-1", "name": "Gateway One"},
                    {"name": "missing-id"},
                ]
            }
        }

    client.transport.get = fake_get

    gateways = client.gateways.list()

    assert [item.id for item in gateways] == ["gw-1"]


def test_gateways_manager_raises_on_unrecognized_single_gateway_shape() -> None:
    client = SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN")

    def fake_get(path: str, *, params=None):
        assert path == "/gateways/gw-1"
        return {"data": {"name": "Gateway One"}}

    client.transport.get = fake_get

    with pytest.raises(APIResponseError) as excinfo:
        client.gateways.get("gw-1")

    assert "did not include a recognizable gateway identifier" in str(excinfo.value)
