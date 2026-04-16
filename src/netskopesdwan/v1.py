from __future__ import annotations

from enum import Enum
from typing import Any

from .enums import V1MonitoringWANMetric
from .exceptions import APIResponseError
from .managers.base import BaseManager
from .models.resource import ResourceRecord
from .transport import Transport


class LegacyV1Namespace:
    """Legacy v1-only GET endpoints without current practical v2 equivalents."""

    def __init__(self, transport: Transport) -> None:
        self.edges = V1EdgeManager(transport)
        self.monitoring = V1MonitoringManager(transport)
        self.users = V1UserManager(transport)


class V1EdgeManager(BaseManager):
    resource_path = "/edges"

    def __init__(self, transport: Transport) -> None:
        super().__init__(transport)
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
        after_cursor: str | None = None,
        before_cursor: str | None = None,
        max_items: int | None = None,
        child_tenant_id: str | None = None,
        get_templates: bool | None = None,
    ) -> list[ResourceRecord]:
        params = _build_v1_params(
            after_cursor=after_cursor,
            before_cursor=before_cursor,
            max_items=max_items,
            child_tenant_id=child_tenant_id,
            get_templates=get_templates,
        )
        payload = self._get(params=params)
        self._last_page_info = None
        self._last_cursors = _extract_v1_cursors(payload)
        return _parse_v1_resource_list(payload, resource_label="v1 edge")

    def get(
        self,
        edge_id: str,
        *,
        child_tenant_id: str | None = None,
    ) -> ResourceRecord:
        payload = self._get(
            edge_id,
            params=_build_v1_params(child_tenant_id=child_tenant_id),
        )
        return _parse_v1_resource_detail(payload, resource_label="v1 edge")

    def list_interfaces(
        self,
        edge_id: str,
        *,
        child_tenant_id: str | None = None,
    ) -> list[dict[str, Any]]:
        payload = self._get(
            f"/edges/{edge_id}/interfaces",
            params=_build_v1_params(child_tenant_id=child_tenant_id),
        )
        return _parse_v1_raw_list(payload, resource_label="v1 edge interface")

    def get_interface(
        self,
        edge_id: str,
        interface_name: str,
        *,
        child_tenant_id: str | None = None,
    ) -> dict[str, Any]:
        payload = self._get(
            f"/edges/{edge_id}/interfaces/{interface_name}",
            params=_build_v1_params(child_tenant_id=child_tenant_id),
        )
        return _parse_v1_raw_object(payload, resource_label="v1 edge interface")

    def list_gateway_interfaces(
        self,
        edge_id: str,
        *,
        child_tenant_id: str | None = None,
    ) -> list[dict[str, Any]]:
        payload = self._get(
            f"/gateways/{edge_id}/interfaces",
            params=_build_v1_params(child_tenant_id=child_tenant_id),
        )
        return _parse_v1_raw_list(payload, resource_label="v1 gateway interface")

    def get_gateway_interface(
        self,
        edge_id: str,
        interface_name: str,
        *,
        child_tenant_id: str | None = None,
    ) -> dict[str, Any]:
        payload = self._get(
            f"/gateways/{edge_id}/interfaces/{interface_name}",
            params=_build_v1_params(child_tenant_id=child_tenant_id),
        )
        return _parse_v1_raw_object(payload, resource_label="v1 gateway interface")


class V1MonitoringManager(BaseManager):
    def get_device_flows_totals(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        ip: str | None = None,
    ) -> dict[str, Any]:
        return self._get_raw_object(
            f"/monitoring/gateways/{gateway_id}/devices/device_flows_totals",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                ip=ip,
            ),
        )

    def get_devices_totals(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
    ) -> dict[str, Any]:
        return self._get_raw_object(
            f"/monitoring/gateways/{gateway_id}/devices/devices_totals",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            ),
        )

    def get_interfaces_latest(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        return self._get_raw_payload(
            f"/monitoring/gateways/{gateway_id}/overview/interfaces_latest",
            params=_build_v1_params(child_tenant_id=child_tenant_id),
        )

    def get_paths_latest(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        return self._get_raw_payload(
            f"/monitoring/gateways/{gateway_id}/overview/paths_latest",
            params=_build_v1_params(child_tenant_id=child_tenant_id),
        )

    def get_routes_latest(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        return self._get_raw_payload(
            f"/monitoring/gateways/{gateway_id}/overview/routes_latest",
            params=_build_v1_params(child_tenant_id=child_tenant_id),
        )

    def get_system_load(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        time_slots: int | None = None,
    ) -> dict[str, Any]:
        return self._get_raw_object(
            f"/monitoring/gateways/{gateway_id}/system/load",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                time_slots=time_slots,
            ),
        )

    def get_system_lte(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        time_slots: int | None = None,
    ) -> dict[str, Any]:
        return self._get_raw_object(
            f"/monitoring/gateways/{gateway_id}/system/lte",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                time_slots=time_slots,
            ),
        )

    def get_system_memory(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        time_slots: int | None = None,
    ) -> dict[str, Any]:
        return self._get_raw_object(
            f"/monitoring/gateways/{gateway_id}/system/memory",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                time_slots=time_slots,
            ),
        )

    def get_system_uptime(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        time_slots: int | None = None,
    ) -> dict[str, Any]:
        return self._get_raw_object(
            f"/monitoring/gateways/{gateway_id}/system/uptime",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                time_slots=time_slots,
            ),
        )

    def get_system_wifi(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        time_slots: int | None = None,
    ) -> dict[str, Any]:
        return self._get_raw_object(
            f"/monitoring/gateways/{gateway_id}/system/wifi",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                time_slots=time_slots,
            ),
        )

    def get_paths_links(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
        metric: V1MonitoringWANMetric | str | None = None,
        time_slots: int | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        return self._get_raw_payload(
            f"/monitoring/gateways/{gateway_id}/wan/paths_links",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                metric=_enum_value(metric),
                time_slots=time_slots,
            ),
        )

    def get_paths_links_totals(
        self,
        gateway_id: str,
        *,
        child_tenant_id: str | None = None,
        start_datetime: str | None = None,
        end_datetime: str | None = None,
    ) -> dict[str, Any]:
        return self._get_raw_object(
            f"/monitoring/gateways/{gateway_id}/wan/paths_links_totals",
            params=_build_v1_params(
                child_tenant_id=child_tenant_id,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            ),
        )

    def _get_raw_object(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = self._get(path, params=params)
        return _parse_v1_raw_object(payload, resource_label="v1 monitoring response")

    def _get_raw_payload(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        payload = self._get(path, params=params)
        return _parse_v1_raw_payload(payload, resource_label="v1 monitoring response")


class V1UserManager(BaseManager):
    def get_groups(
        self,
        user_id: str,
        *,
        after_cursor: str | None = None,
        before_cursor: str | None = None,
        max_items: int | None = None,
    ) -> list[ResourceRecord]:
        payload = self._get(
            f"/users/{user_id}/groups",
            params=_build_v1_params(
                after_cursor=after_cursor,
                before_cursor=before_cursor,
                max_items=max_items,
            ),
        )
        return _parse_v1_resource_list(payload, resource_label="v1 user group")


def _parse_v1_resource_list(payload: Any, *, resource_label: str) -> list[ResourceRecord]:
    items = _parse_v1_enveloped_list(payload, resource_label=resource_label)
    return [ResourceRecord.from_dict(item) for item in items]


def _enum_value(value: str | Enum | None) -> str | None:
    if isinstance(value, Enum):
        return str(value.value)
    return value


def _parse_v1_resource_detail(payload: Any, *, resource_label: str) -> ResourceRecord:
    data = _parse_v1_raw_object(payload, resource_label=resource_label)
    resource = ResourceRecord.from_dict(data)
    if not resource.id:
        raise APIResponseError(
            f"{resource_label} detail response did not include the required 'id' field."
        )
    return resource


def _parse_v1_raw_payload(
    payload: Any,
    *,
    resource_label: str,
) -> list[dict[str, Any]] | dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
        return payload
    raise APIResponseError(
        f"{resource_label} response must be a top-level JSON object or array of objects."
    )


def _parse_v1_raw_list(payload: Any, *, resource_label: str) -> list[dict[str, Any]]:
    if isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
        return payload
    raise APIResponseError(f"{resource_label} response must be a top-level JSON array of objects.")


def _parse_v1_raw_object(payload: Any, *, resource_label: str) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    raise APIResponseError(f"{resource_label} response must be a top-level JSON object.")


def _parse_v1_enveloped_list(payload: Any, *, resource_label: str) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return _parse_v1_raw_list(payload, resource_label=resource_label)
    if not isinstance(payload, dict):
        raise APIResponseError(
            f"{resource_label} response must be a top-level JSON array or object."
        )
    for field_name in ("data", "items"):
        if field_name not in payload:
            continue
        items = payload[field_name]
        if isinstance(items, list) and all(isinstance(item, dict) for item in items):
            return items
        raise APIResponseError(
            f"{resource_label} response field '{field_name}' must be a JSON array of objects."
        )
    keys = ", ".join(sorted(payload.keys())) or "<none>"
    raise APIResponseError(
        f"{resource_label} response did not include a valid list field. "
        f"Expected one of ('data', 'items'). Top-level keys: {keys}."
    )


def _build_v1_params(
    *,
    after_cursor: str | None = None,
    before_cursor: str | None = None,
    max_items: int | None = None,
    child_tenant_id: str | None = None,
    get_templates: bool | None = None,
    start_datetime: str | None = None,
    end_datetime: str | None = None,
    ip: str | None = None,
    metric: str | None = None,
    time_slots: int | None = None,
) -> dict[str, Any] | None:
    params: dict[str, Any] = {}
    if after_cursor:
        params["afterCursor"] = after_cursor
    if before_cursor:
        params["beforeCursor"] = before_cursor
    if max_items is not None:
        params["maxItems"] = max_items
    if child_tenant_id:
        params["childTenantId"] = child_tenant_id
    if get_templates is not None:
        params["getTemplates"] = get_templates
    if start_datetime:
        params["startDatetime"] = start_datetime
    if end_datetime:
        params["endDatetime"] = end_datetime
    if ip:
        params["ip"] = ip
    if metric:
        params["metric"] = metric
    if time_slots is not None:
        params["timeSlots"] = time_slots
    return params or None


def _extract_v1_cursors(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    cursor_fields = ("startCursor", "endCursor", "firstPage", "lastPage")
    cursors = {name: payload[name] for name in cursor_fields if name in payload}
    return cursors or None
