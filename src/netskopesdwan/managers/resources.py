from __future__ import annotations

from typing import Any

from ..exceptions import APIResponseError
from ..models.resource import ResourceRecord
from .base import BaseManager

API_V2_PREFIX = "/v2"


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
            resource_path=f"{API_V2_PREFIX}/inventory-devices",
            resource_label="inventory device",
        )

    def get(self, resource_id: str) -> ResourceRecord:
        raise AttributeError(
            "InventoryDeviceManager does not support get(id) because the current SDK batch only "
            "includes GET /inventory-devices."
        )


class AuditEventManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/auditevents", resource_label="audit event")

    def get(self, resource_id: str) -> ResourceRecord:
        raise AttributeError(
            "AuditEventManager does not support get(id) because the current SDK batch only "
            "includes GET /auditevents."
        )


class AddressGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/address-groups", resource_label="address group")

    def list_address_objects(self, group_id: str) -> list[ResourceRecord]:
        payload = self._get(f"{API_V2_PREFIX}/address-groups/{group_id}/address-objects")
        return _parse_resource_list_response(
            payload,
            resource_label="address object",
            list_field_candidates=self.list_field_candidates,
        )


class DeviceGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/device-groups", resource_label="device group")


class ClientTemplateManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/client-templates",
            resource_label="client template",
        )


class ClientManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/clients", resource_label="client")


class CloudAccountManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/cloud-accounts", resource_label="cloud account")


class ApplicationManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/custom-apps", resource_label="custom app")

    def list_categories(self) -> list[ResourceRecord]:
        payload = self._get(f"{API_V2_PREFIX}/app-categories")
        return _parse_resource_list_response(
            payload,
            resource_label="app category",
            list_field_candidates=self.list_field_candidates,
        )

    def list_custom_apps(self) -> list[ResourceRecord]:
        return self.list()

    def get_custom_app(self, resource_id: str) -> ResourceRecord:
        return self.get(resource_id)

    def list_qosmos_apps(self) -> list[ResourceRecord]:
        payload = self._get(f"{API_V2_PREFIX}/qosmos-apps")
        return _parse_resource_list_response(
            payload,
            resource_label="qosmos app",
            list_field_candidates=self.list_field_candidates,
        )

    def list_webroot_categories(self) -> list[ResourceRecord]:
        payload = self._get(f"{API_V2_PREFIX}/webroot-categories")
        return _parse_resource_list_response(
            payload,
            resource_label="webroot category",
            list_field_candidates=self.list_field_candidates,
        )


class CACertificateManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/ca-certificates",
            resource_label="ca certificate",
        )


class ControllerOperatorManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/controller-operators",
            resource_label="controller operator",
        )


class ControllerManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/controllers", resource_label="controller")

    def get_operator_status(self, controller_id: str) -> dict[str, Any]:
        payload = self._get(f"{API_V2_PREFIX}/controllers/{controller_id}/operator_status")
        return _parse_raw_object_response(payload, resource_label="controller operator status")


class GatewayGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/gateway-groups", resource_label="gateway group")


class GatewayTemplateManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/gateway-templates",
            resource_label="gateway template",
        )


class NTPConfigManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/ntp-configs", resource_label="ntp config")


class OverlayTagManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/overlay-tags", resource_label="overlay tag")


class SegmentManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/segments", resource_label="segment")


class VPNPeerManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/vpnpeers", resource_label="vpn peer")


class PolicyManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/policies", resource_label="policy")


class SiteCommandManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/site-commands", resource_label="site command")

    def get_output(self, command_id: str, name: str) -> str:
        return self._transport.get_text(f"{API_V2_PREFIX}/site-command/{command_id}/output/{name}")


class SoftwareManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/software-versions",
            resource_label="software version",
        )

    def list_downloads(self) -> list[ResourceRecord]:
        payload = self._get(f"{API_V2_PREFIX}/software-downloads")
        return _parse_resource_list_response(
            payload,
            resource_label="software download",
            list_field_candidates=self.list_field_candidates,
        )

    def list_versions(self) -> list[ResourceRecord]:
        return self.list()

    def get(self, resource_id: str) -> ResourceRecord:
        raise AttributeError(
            "SoftwareManager does not support get(id) because the current SDK batch only "
            "includes GET /software-downloads and GET /software-versions."
        )


class TenantManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/tenants", resource_label="tenant")


class UserGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/user-groups", resource_label="user group")


class UserManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(transport, resource_path=f"{API_V2_PREFIX}/users", resource_label="user")


class RadiusServerManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/radius-servers",
            resource_label="radius server",
        )


class JWKSManager(BaseManager):
    resource_path = f"{API_V2_PREFIX}/jwks.json"

    def get(self) -> dict[str, Any]:
        payload = self._get(f"{API_V2_PREFIX}/jwks.json")
        return _parse_raw_object_response(payload, resource_label="jwks")


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


def _parse_raw_object_response(payload: Any, *, resource_label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise APIResponseError(f"{_label(resource_label)} response must be a top-level JSON object.")
    return payload


def _label(value: str) -> str:
    return value[:1].upper() + value[1:]
