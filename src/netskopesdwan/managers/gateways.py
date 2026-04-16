from __future__ import annotations

from typing import Any

from ..exceptions import APIResponseError
from ..models.gateway import Gateway
from .base import BaseManager
from .resources import _parse_list_response

GATEWAYS_PATH = "/v2/gateways"
GATEWAY_BY_ID_PATH = "/v2/gateways/{id}"
GATEWAY_LOCALUI_PASSWORD_PATH = "/v2/gateways/{id}/localui-password"
GATEWAY_SSH_PASSWORD_PATH = "/v2/gateways/{id}/ssh-password"
GATEWAY_TELEMETRY_OVERVIEW_PATH = "/v2/gateways/{id}/telemetry/overview"


class GatewayManager(BaseManager):
    resource_path = GATEWAYS_PATH

    def __init__(self, transport) -> None:
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
        after: str | None = None,
        first: int | None = None,
        sort: str | None = None,
        filter: str | None = None,
    ) -> list[Gateway]:
        params = _build_list_params(after=after, first=first, sort=sort, filter=filter)
        payload = self._get(params=params)
        gateways, page_info, cursors = _parse_gateway_list_response(payload)
        self._last_page_info = dict(page_info) if page_info is not None else None
        self._last_cursors = dict(cursors) if cursors is not None else None
        return gateways

    def get(self, gateway_id: str) -> Gateway:
        payload = self._get(GATEWAY_BY_ID_PATH.format(id=gateway_id))
        return _parse_gateway_object_response(payload)

    def get_localui_password(self, gateway_id: str) -> dict[str, Any]:
        payload = self._get(GATEWAY_LOCALUI_PASSWORD_PATH.format(id=gateway_id))
        return _parse_gateway_password_response(payload, password_type="local UI password")

    def get_ssh_password(self, gateway_id: str) -> dict[str, Any]:
        payload = self._get(GATEWAY_SSH_PASSWORD_PATH.format(id=gateway_id))
        return _parse_gateway_password_response(payload, password_type="SSH password")

    def get_telemetry_overview(self, gateway_id: str) -> dict[str, Any]:
        payload = self._get(GATEWAY_TELEMETRY_OVERVIEW_PATH.format(id=gateway_id))
        return _parse_gateway_telemetry_response(payload)


def _parse_gateway_list_response(
    payload: Any,
) -> tuple[list[Gateway], dict[str, Any] | None, dict[str, Any] | None]:
    return _parse_list_response(
        payload,
        resource_label="gateway",
        list_field_candidates=("data", "items"),
        item_adapter=_adapt_gateway,
    )


def _parse_gateway_object_response(payload: Any) -> Gateway:
    if not isinstance(payload, dict):
        raise APIResponseError("Gateway detail response must be a top-level JSON object.")
    gateway = _adapt_gateway(payload)
    if not gateway.id:
        raise APIResponseError("Gateway detail response did not include the required 'id' field.")
    return gateway


def _adapt_gateway(payload: Any, *, resource_label: str = "gateway") -> Gateway:
    if not isinstance(payload, dict):
        raise APIResponseError(
            f"{resource_label[:1].upper() + resource_label[1:]} payload items must be JSON objects."
        )
    return Gateway.from_dict(payload)


def _parse_gateway_password_response(payload: Any, *, password_type: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise APIResponseError(f"Gateway {password_type} response must be a top-level JSON object.")
    return payload


def _parse_gateway_telemetry_response(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise APIResponseError(
            "Gateway telemetry overview response must be a top-level JSON object."
        )
    return payload


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
