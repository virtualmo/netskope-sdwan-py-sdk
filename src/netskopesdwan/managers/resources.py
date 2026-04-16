from __future__ import annotations

from typing import Any

from ..exceptions import APIResponseError, ValidationError
from ..models.download import DownloadResult
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
        self._last_page_info: dict[str, Any] | None = None
        self._last_cursors: dict[str, Any] | None = None

    @property
    def last_page_info(self) -> dict[str, Any] | None:
        return self._last_page_info

    @property
    def last_cursors(self) -> dict[str, Any] | None:
        return self._last_cursors

    def list(
        self,
        *,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        params = _build_list_params(after=after, first=first, sort=sort, filter=filter)
        payload = self._get(params=params)
        items, page_info, cursors = _parse_resource_list_response(
            payload,
            resource_label=self.resource_label,
            list_field_candidates=self.list_field_candidates,
        )
        self._store_pagination_state(page_info=page_info, cursors=cursors)
        return items

    def get(self, resource_id: str) -> ResourceRecord:
        payload = self._get(resource_id)
        return _parse_resource_detail_response(payload, resource_label=self.resource_label)

    def _store_pagination_state(
        self,
        *,
        page_info: dict[str, Any] | None,
        cursors: dict[str, Any] | None,
    ) -> None:
        self._last_page_info = dict(page_info) if page_info is not None else None
        self._last_cursors = dict(cursors) if cursors is not None else None


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
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/auditevents",
            resource_label="audit event",
        )

    def list(
        self,
        *,
        created_at_from: str,
        created_at_to: str,
        type: str | None = None,
        subtype: str | None = None,
        activity: str | None = None,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        missing_filters = []
        if not created_at_from:
            missing_filters.append("created_at_from")
        if not created_at_to:
            missing_filters.append("created_at_to")
        if missing_filters:
            raise ValidationError(
                "audit_events.list(...) requires a bounded time range with "
                + ", ".join(missing_filters)
                + "."
            )

        filter_expression = _build_audit_event_filter(
            created_at_from=created_at_from,
            created_at_to=created_at_to,
            type=type,
            subtype=subtype,
            activity=activity,
            raw_filter=filter,
        )
        params = _build_list_params(
            after=after,
            first=first,
            sort=sort,
            filter=filter_expression,
        )
        payload = self._get(params=params)
        items, page_info, cursors = _parse_resource_list_response(
            payload,
            resource_label=self.resource_label,
            list_field_candidates=self.list_field_candidates,
        )
        self._store_pagination_state(page_info=page_info, cursors=cursors)
        return items

    def get(self, resource_id: str) -> ResourceRecord:
        raise AttributeError(
            "AuditEventManager does not support get(id) because the current SDK batch only "
            "includes GET /auditevents."
        )


class AddressGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/address-groups",
            resource_label="address group",
        )

    def list_address_objects(
        self,
        group_id: str,
        *,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        params = _build_list_params(after=after, first=first, sort=sort, filter=filter)
        payload = self._get(
            f"{API_V2_PREFIX}/address-groups/{group_id}/address-objects",
            params=params,
        )
        items, page_info, cursors = _parse_resource_list_response(
            payload,
            resource_label="address object",
            list_field_candidates=self.list_field_candidates,
        )
        self._store_pagination_state(page_info=page_info, cursors=cursors)
        return items


class DeviceGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/device-groups",
            resource_label="device group",
        )


class ClientTemplateManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/client-templates",
            resource_label="client template",
        )


class ClientManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/clients",
            resource_label="client",
        )


class CloudAccountManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/cloud-accounts",
            resource_label="cloud account",
        )


class ApplicationManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/custom-apps",
            resource_label="custom app",
        )

    def list_categories(
        self,
        *,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        params = _build_list_params(after=after, first=first, sort=sort, filter=filter)
        payload = self._get(f"{API_V2_PREFIX}/app-categories", params=params)
        items, page_info, cursors = _parse_resource_list_response(
            payload,
            resource_label="app category",
            list_field_candidates=self.list_field_candidates,
        )
        self._store_pagination_state(page_info=page_info, cursors=cursors)
        return items

    def list_custom_apps(
        self,
        *,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        return self.list(after=after, first=first, sort=sort, filter=filter)

    def get_custom_app(self, resource_id: str) -> ResourceRecord:
        return self.get(resource_id)

    def list_qosmos_apps(
        self,
        *,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        params = _build_list_params(after=after, first=first, sort=sort, filter=filter)
        payload = self._get(
            f"{API_V2_PREFIX}/qosmos-apps",
            params=params,
        )
        items, page_info, cursors = _parse_resource_list_response(
            payload,
            resource_label="qosmos app",
            list_field_candidates=self.list_field_candidates,
        )
        self._store_pagination_state(page_info=page_info, cursors=cursors)
        return items

    def list_webroot_categories(
        self,
        *,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        params = _build_list_params(after=after, first=first, sort=sort, filter=filter)
        payload = self._get(
            f"{API_V2_PREFIX}/webroot-categories",
            params=params,
        )
        items, page_info, cursors = _parse_resource_list_response(
            payload,
            resource_label="webroot category",
            list_field_candidates=self.list_field_candidates,
        )
        self._store_pagination_state(page_info=page_info, cursors=cursors)
        return items


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
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/controllers",
            resource_label="controller",
        )

    def get_operator_status(self, controller_id: str) -> dict[str, Any]:
        payload = self._get(f"{API_V2_PREFIX}/controllers/{controller_id}/operator_status")
        return _parse_raw_object_response(payload, resource_label="controller operator status")


class GatewayGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/gateway-groups",
            resource_label="gateway group",
        )


class GatewayTemplateManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/gateway-templates",
            resource_label="gateway template",
        )


class NTPConfigManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/ntp-configs",
            resource_label="ntp config",
        )


class OverlayTagManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/overlay-tags",
            resource_label="overlay tag",
        )


class SegmentManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/segments",
            resource_label="segment",
        )


class VPNPeerManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/vpnpeers",
            resource_label="vpn peer",
        )


class PolicyManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/policies",
            resource_label="policy",
        )


class SiteCommandManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/site-commands",
            resource_label="site command",
        )

    def get_output(self, command_id: str, name: str) -> DownloadResult:
        return self._transport.get_download(
            f"{API_V2_PREFIX}/site-command/{command_id}/output/{name}"
        )


class SoftwareManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/software-versions",
            resource_label="software version",
        )

    def list_downloads(
        self,
        *,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        params = _build_list_params(after=after, first=first, sort=sort, filter=filter)
        payload = self._get(
            f"{API_V2_PREFIX}/software-downloads",
            params=params,
        )
        items, page_info, cursors = _parse_resource_list_response(
            payload,
            resource_label="software download",
            list_field_candidates=self.list_field_candidates,
        )
        self._store_pagination_state(page_info=page_info, cursors=cursors)
        return items

    def list_versions(
        self,
        *,
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[ResourceRecord]:
        return self.list(after=after, first=first, sort=sort, filter=filter)

    def get(self, resource_id: str) -> ResourceRecord:
        raise AttributeError(
            "SoftwareManager does not support get(id) because the current SDK batch only "
            "includes GET /software-downloads and GET /software-versions."
        )


class TenantManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/tenants",
            resource_label="tenant",
        )


class UserGroupManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/user-groups",
            resource_label="user group",
        )


class UserManager(ReadOnlyResourceManager):
    def __init__(self, transport) -> None:
        super().__init__(
            transport,
            resource_path=f"{API_V2_PREFIX}/users",
            resource_label="user",
        )


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
) -> tuple[list[ResourceRecord], dict[str, Any] | None, dict[str, Any] | None]:
    return _parse_list_response(
        payload,
        resource_label=resource_label,
        list_field_candidates=list_field_candidates,
        item_adapter=_adapt_resource,
    )


def _parse_list_response(
    payload: Any,
    *,
    resource_label: str,
    list_field_candidates: tuple[str, ...],
    item_adapter,
) -> tuple[list[Any], dict[str, Any] | None, dict[str, Any] | None]:
    if isinstance(payload, list):
        items = [item_adapter(item, resource_label=resource_label) for item in payload]
        return items, None, None

    if not isinstance(payload, dict):
        raise APIResponseError(
            f"{_label(resource_label)} list response must be a top-level JSON array or object."
        )

    page_info = _parse_optional_metadata_object(
        payload,
        field_name="page_info",
        resource_label=resource_label,
    )
    cursors = _parse_optional_metadata_object(
        payload,
        field_name="cursors",
        resource_label=resource_label,
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
            f"{_label(resource_label)} list response field "
            f"'{list_field_name}' must be a JSON array."
        )

    return [item_adapter(item, resource_label=resource_label) for item in items], page_info, cursors


def _parse_resource_detail_response(payload: Any, *, resource_label: str) -> ResourceRecord:
    if not isinstance(payload, dict):
        raise APIResponseError(
            f"{_label(resource_label)} detail response must be a top-level JSON object."
        )
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
        raise APIResponseError(
            f"{_label(resource_label)} response must be a top-level JSON object."
        )
    return payload


def _build_audit_event_filter(
    *,
    created_at_from: str,
    created_at_to: str,
    type: str | None,
    subtype: str | None,
    activity: str | None,
    raw_filter: str | None,
) -> str:
    parts = [
        f'created_at>="{created_at_from}"',
        f'created_at<="{created_at_to}"',
    ]
    if type:
        parts.append(f"type: {type}")
    if subtype:
        parts.append(f"subtype: {subtype}")
    if activity:
        parts.append(f"activity: {activity}")
    if raw_filter:
        parts.append(raw_filter)
    return " AND ".join(parts)


def _build_list_params(
    *,
    after: str | None = None,
    first: int | None = None,
    sort: str | None = None,
    filter: str | None = None,
) -> dict[str, Any] | None:
    params: dict[str, Any] = {}
    if after:
        params["after"] = after
    if first is not None:
        params["first"] = first
    if sort:
        params["sort"] = sort
    if filter:
        params["filter"] = filter
    return params or None


def _parse_optional_metadata_object(
    payload: dict[str, Any],
    *,
    field_name: str,
    resource_label: str,
) -> dict[str, Any] | None:
    value = payload.get(field_name)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise APIResponseError(
            f"{_label(resource_label)} list response field '{field_name}' must be a JSON object."
        )
    return value


def _label(value: str) -> str:
    return value[:1].upper() + value[1:]
