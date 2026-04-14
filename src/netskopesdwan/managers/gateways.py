from __future__ import annotations

from typing import Any

from ..exceptions import APIResponseError
from ..models.gateway import Gateway
from .base import BaseManager

GATEWAYS_PATH = "/v2/gateways"
GATEWAY_BY_ID_PATH = "/v2/gateways/{id}"


class GatewayManager(BaseManager):
    resource_path = GATEWAYS_PATH

    def list(self) -> list[Gateway]:
        payload = self._get()
        return _parse_gateway_list_response(payload)

    def get(self, gateway_id: str) -> Gateway:
        payload = self._get(GATEWAY_BY_ID_PATH.format(id=gateway_id))
        return _parse_gateway_object_response(payload)


def _parse_gateway_list_response(payload: Any) -> list[Gateway]:
    if not isinstance(payload, list):
        raise APIResponseError(
            "Gateway list response must be a top-level JSON array."
        )
    return [_adapt_gateway(item) for item in payload]


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
