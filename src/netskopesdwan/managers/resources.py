from __future__ import annotations

from typing import Any

from ..exceptions import APIResponseError
from ..models.resource import ResourceRecord
from .base import BaseManager


class ReadOnlyResourceManager(BaseManager):
    resource_label = "resource"
    list_field_candidates = ("data", "items")

    def __init__(self, transport, *, resource_path: str, resource_label: str) -> None:
        super().__init__(transport)
        self.resource_path = resource_path
        self.resource_label = resource_label

    def list(self) -> list[ResourceRecord]:
        payload = self._get()
        return _parse_resource_list_response(
            payload,
            resource_label=self.resource_label,
            list_field_candidates=self.list_field_candidates,
        )

    def get(self, resource_id: str) -> ResourceRecord:
        payload = self._get(resource_id)
        return _parse_resource_detail_response(payload, resource_label=self.resource_label)


class InventoryDeviceManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path="/inventory-devices",
            resource_label="inventory device",
        )

    def get(self, resource_id: str) -> ResourceRecord:
        raise AttributeError(
            "InventoryDeviceManager does not support get(id) because the current SDK batch only "
            "includes GET /inventory-devices."
        )


class DeviceGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path="/device-groups", resource_label="device group")


class GatewayGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path="/gateway-groups", resource_label="gateway group")


class GatewayTemplateManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path="/gateway-templates",
            resource_label="gateway template",
        )


class NTPConfigManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path="/ntp-configs", resource_label="ntp config")


class OverlayTagManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path="/overlay-tags", resource_label="overlay tag")


class SegmentManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path="/segments", resource_label="segment")


class VPNPeerManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path="/vpnpeers", resource_label="vpn peer")


class PolicyManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path="/policies", resource_label="policy")


class RadiusServerManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path="/radius-servers",
            resource_label="radius server",
        )


def _parse_resource_list_response(
    payload: Any,
    *,
    resource_label: str,
    list_field_candidates: tuple[str, ...],
) -> list[ResourceRecord]:
    if isinstance(payload, list):
        return [_adapt_resource(item, resource_label=resource_label) for item in payload]

    if not isinstance(payload, dict):
        raise APIResponseError(
            f"{_label(resource_label)} list response must be a top-level JSON array or object."
        )

    list_field_name = next((name for name in list_field_candidates if name in payload), None)
    if list_field_name is None:
        keys = ", ".join(sorted(payload.keys())) or "<none>"
        raise APIResponseError(
            f"{_label(resource_label)} list response did not include a valid list field. "
            f"Expected one of {list_field_candidates}. Top-level keys: {keys}."
        )

    items = payload[list_field_name]
    if not isinstance(items, list):
        raise APIResponseError(
            f"{_label(resource_label)} list response field '{list_field_name}' must be a JSON array."
        )

    return [_adapt_resource(item, resource_label=resource_label) for item in items]


def _parse_resource_detail_response(payload: Any, *, resource_label: str) -> ResourceRecord:
    if not isinstance(payload, dict):
        raise APIResponseError(f"{_label(resource_label)} detail response must be a top-level JSON object.")
    resource = _adapt_resource(payload, resource_label=resource_label)
    if not resource.id:
        raise APIResponseError(
            f"{_label(resource_label)} detail response did not include the required 'id' field."
        )
    return resource


def _adapt_resource(payload: Any, *, resource_label: str) -> ResourceRecord:
    if not isinstance(payload, dict):
        raise APIResponseError(f"{_label(resource_label)} payload items must be JSON objects.")
    return ResourceRecord.from_dict(payload)


def _label(value: str) -> str:
    return value[:1].upper() + value[1:]
