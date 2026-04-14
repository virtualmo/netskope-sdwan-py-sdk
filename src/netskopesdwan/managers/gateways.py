from __future__ import annotations

from typing import Any

from ..exceptions import APIResponseError
from ..models.gateway import Gateway
from .base import BaseManager


class GatewayManager(BaseManager):
    resource_path = "/gateways"

    def list(self) -> list[Gateway]:
        payload = self._get()
        return _parse_gateway_collection(payload)

    def get(self, gateway_id: str) -> Gateway:
        payload = self._get(gateway_id)
        return _parse_gateway(payload)

def _parse_gateway_collection(payload: Any) -> list[Gateway]:
    items = _extract_items(payload)
    gateways: list[Gateway] = []
    for item in items:
        gateway = Gateway.from_dict(item)
        if gateway.id:
            gateways.append(gateway)
    return gateways


def _extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("items", "gateways", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        data = payload.get("data")
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            for key in ("items", "gateways", "results"):
                value = data.get(key)
                if isinstance(value, list):
                    return [item for item in value if isinstance(item, dict)]
    return []


def _parse_gateway(payload: Any) -> Gateway:
    gateway = Gateway.from_dict(_extract_single(payload))
    if not gateway.id:
        raise APIResponseError(
            "Gateway response did not include a recognizable gateway identifier."
        )
    return gateway


def _extract_single(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        for key in ("item", "data", "gateway"):
            value = payload.get(key)
            if isinstance(value, dict):
                return value
        return payload
    return {}
