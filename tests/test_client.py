from __future__ import annotations

import pytest

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import ConfigurationError
from netskopesdwan.managers.gateways import GatewayManager


def test_client_initialization_with_base_url() -> None:
    client = SDWANClient(
        base_url="customer.eu.infiot.net",
        api_token="TOKEN",
        timeout=15,
        verify_ssl=False,
    )

    assert client.resolved_base_url == "https://customer.api.eu.infiot.net"
    assert client.transport.base_url == "https://customer.api.eu.infiot.net"
    assert client.transport.timeout == 15
    assert client.transport.verify_ssl is False
    assert isinstance(client.gateways, GatewayManager)


def test_client_loads_environment(monkeypatch) -> None:
    monkeypatch.setenv("NETSKOPESDWAN_BASE_URL", "tenant.api.infiot.net")
    monkeypatch.setenv("NETSKOPESDWAN_API_TOKEN", "ENV_TOKEN")
    monkeypatch.setenv("NETSKOPESDWAN_TIMEOUT", "12")

    client = SDWANClient()

    assert client.resolved_base_url == "https://tenant.api.infiot.net"
    assert client.transport.timeout == 12
    assert client.transport.session.headers["Authorization"] == "Bearer ENV_TOKEN"


def test_client_loads_tenant_url_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("NETSKOPESDWAN_TENANT_URL", "customer.de.goskope.com")
    monkeypatch.setenv("NETSKOPESDWAN_API_TOKEN", "ENV_TOKEN")

    client = SDWANClient(sdwan_tenant_name="legacy123")

    assert client.resolved_base_url == "https://legacy123.api.eu.infiot.net"
    assert client.resolution_metadata["input_host"] == "customer.de.goskope.com"


def test_client_initialization_with_tenant_url_only() -> None:
    client = SDWANClient(
        tenant_url="customer.de.goskope.com",
        sdwan_tenant_name="legacy123",
        api_token="TOKEN",
    )

    assert client.resolved_base_url == "https://legacy123.api.eu.infiot.net"
    assert client.resolution_metadata["sdwan_region"] == "PROD-EU"


def test_client_accepts_equivalent_base_url_and_tenant_url() -> None:
    client = SDWANClient(
        base_url="https://legacy123.api.eu.infiot.net/",
        tenant_url="customer.de.goskope.com",
        sdwan_tenant_name="legacy123",
        api_token="TOKEN",
    )

    assert client.resolved_base_url == "https://legacy123.api.eu.infiot.net"


def test_client_rejects_conflicting_base_url_and_tenant_url() -> None:
    with pytest.raises(ConfigurationError) as excinfo:
        SDWANClient(
            base_url="https://other.api.eu.infiot.net",
            tenant_url="customer.de.goskope.com",
            sdwan_tenant_name="legacy123",
            api_token="TOKEN",
        )

    assert "resolved to different API endpoints" in str(excinfo.value)


def test_client_requires_base_url_or_tenant_url() -> None:
    with pytest.raises(ConfigurationError) as excinfo:
        SDWANClient(api_token="TOKEN")

    assert "Either base_url or tenant_url must be provided" in str(excinfo.value)


def test_client_rejects_goskope_value_in_base_url() -> None:
    with pytest.raises(ConfigurationError) as excinfo:
        SDWANClient(
            base_url="customer.de.goskope.com",
            api_token="TOKEN",
        )

    assert "base_url must point to a Netskope SD-WAN API host" in str(excinfo.value)


def test_client_rejects_non_positive_timeout() -> None:
    with pytest.raises(ConfigurationError) as excinfo:
        SDWANClient(base_url="tenant.api.infiot.net", api_token="TOKEN", timeout=0)

    assert "timeout must be greater than 0" in str(excinfo.value)


def test_client_requires_token() -> None:
    try:
        SDWANClient(base_url="tenant.api.infiot.net")
    except ConfigurationError as exc:
        assert "api_token is required" in str(exc)
    else:
        raise AssertionError("Expected ConfigurationError to be raised.")
