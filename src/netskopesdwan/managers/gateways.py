from __future__ import annotations

from typing import Any

from ..exceptions import APIResponseError
from ..models.gateway import Gateway
from .base import BaseManager

GATEWAYS_PATH = "/v2/gateways"
GATEWAY_BY_ID_PATH = "/v2/gateways/{id}"


class GatewayManager(BaseManager):
    resource_path = GATEWAYS_PATH

    def __init__(self, transport) -> None:
        super().__init__(transport)
        self._last_page_info: dict[str, Any] | None = None

    def list(self) -> list[Gateway]:
        payload = self._get()
        gateways, page_info = _parse_gateway_list_response(payload)
        self._last_page_info = page_info
        return gateways

    def get(self, gateway_id: str) -> Gateway:
        payload = self._get(GATEWAY_BY_ID_PATH.format(id=gateway_id))
        return _parse_gateway_object_response(payload)


def _parse_gateway_list_response(payload: Any) -> tuple[list[Gateway], dict[str, Any] | None]:
    if not isinstance(payload, dict):
        raise APIResponseError(
            "Gateway list response must be a top-level JSON object."
        )

    page_info = payload.get("page_info")
    if page_info is not None and not isinstance(page_info, dict):
        raise APIResponseError("Gateway list response field 'page_info' must be a JSON object.")

    list_field_name = "data" if "data" in payload else "items" if "items" in payload else None
    if list_field_name is None:
        keys = ", ".join(sorted(payload.keys())) or "<none>"
        raise APIResponseError(
            "Gateway list response did not include a valid list field. "
            f"Expected 'data' or 'items'. Top-level keys: {keys}."
        )

    items = payload[list_field_name]
    if not isinstance(items, list):
        raise APIResponseError(
            f"Gateway list response field '{list_field_name}' must be a JSON array."
        )

    return ([_adapt_gateway(item) for item in items], page_info)


def _parse_gateway_object_response(payload: Any) -> Gateway:
    if not isinstance(payload, dict):
        raise APIResponseError(
            "Gateway detail response must be a top-level JSON object."
        )
    gateway = _adapt_gateway(payload)
    if not gateway.id:
        raise APIResponseError(
            "Gateway detail response did not include the required 'id' field."
        )
    return gateway


def _adapt_gateway(payload: Any) -> Gateway:
    if not isinstance(payload, dict):
        raise APIResponseError("Gateway payload items must be JSON objects.")
    return Gateway.from_dict(payload)
