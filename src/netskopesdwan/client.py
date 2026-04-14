from __future__ import annotations

from .config import ClientSettings, load_settings
from .managers.gateways import GatewayManager
from .tenant_resolution import ResolutionResult, resolve_api_base_url
from .transport import Transport


class SDWANClient:
    def __init__(
        self,
        *,
        tenant_url: str | None = None,
        base_url: str | None = None,
        sdwan_tenant_name: str | None = None,
        api_token: str | None = None,
        timeout: float | int | None = None,
        verify_ssl: bool = True,
    ) -> None:
        self._settings: ClientSettings = load_settings(
            base_url=base_url,
            tenant_url=tenant_url,
            api_token=api_token,
            timeout=timeout,
            verify_ssl=verify_ssl,
            sdwan_tenant_name=sdwan_tenant_name,
        )
        self._resolution: ResolutionResult = resolve_api_base_url(
            base_url=self._settings.base_url,
            tenant_url=self._settings.tenant_url,
            sdwan_tenant_name=self._settings.sdwan_tenant_name,
        )

        self.resolved_base_url = self._resolution.api_base_url
        self.resolution_metadata = self._resolution.to_metadata()

        self.transport = Transport(
            base_url=self.resolved_base_url,
            api_token=self._settings.api_token,
            timeout=self._settings.timeout,
            verify_ssl=self._settings.verify_ssl,
        )

        self.gateways = GatewayManager(self.transport)
