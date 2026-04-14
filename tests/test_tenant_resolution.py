from __future__ import annotations

import pytest

from netskopesdwan.exceptions import ConfigurationError, ResolutionError
from netskopesdwan.tenant_resolution import normalize_url, resolve_api_base_url


def test_infiot_url_normalization() -> None:
    assert normalize_url("foo.infiot.net") == "https://foo.api.infiot.net"
    assert normalize_url("foo.eu.infiot.net") == "https://foo.api.eu.infiot.net"
    assert normalize_url("https://foo.eu.infiot.net") == "https://foo.api.eu.infiot.net"
    assert normalize_url("https://foo.api.au.infiot.net") == "https://foo.api.au.infiot.net"
    assert normalize_url("foo.api.eu.infiot.net") == "https://foo.api.eu.infiot.net"
    assert normalize_url("https://foo.eu.infiot.net/") == "https://foo.api.eu.infiot.net"
    assert normalize_url("HTTPS://Foo.EU.INFIOT.NET/") == "https://foo.api.eu.infiot.net"


def test_goskope_suffix_based_region_mapping_requires_exact_hostname() -> None:
    with pytest.raises(ResolutionError) as excinfo:
        resolve_api_base_url(
            base_url=None,
            tenant_url="customer.de.goskope.com",
            sdwan_tenant_name=None,
        )

    message = str(excinfo.value)
    assert "The SDK identified the SD-WAN region as: PROD-EU" in message
    assert "https://<sdwan-tenant>.api.eu.infiot.net" in message


def test_base_url_rejects_goskope_hosts() -> None:
    with pytest.raises(ConfigurationError) as excinfo:
        resolve_api_base_url(
            base_url="customer.de.goskope.com",
            tenant_url=None,
            sdwan_tenant_name=None,
        )

    assert "Use tenant_url for goskope inputs instead" in str(excinfo.value)


def test_sdwan_tenant_name_override_builds_exact_api_url() -> None:
    result = resolve_api_base_url(
        base_url=None,
        tenant_url="customer.de.goskope.com",
        sdwan_tenant_name="legacy123",
    )

    assert result.api_base_url == "https://legacy123.api.eu.infiot.net"
    assert result.sdwan_region == "PROD-EU"
    assert result.home_mp == "FR4"
    assert result.confidence == "medium"


def test_unknown_goskope_resolution_fails_clearly() -> None:
    with pytest.raises(ResolutionError) as excinfo:
        resolve_api_base_url(
            base_url=None,
            tenant_url="customer.goskope.com",
            sdwan_tenant_name=None,
        )

    assert "Could not determine the SD-WAN region" in str(excinfo.value)


def test_conflicting_base_url_and_tenant_url_raise_configuration_error() -> None:
    with pytest.raises(ConfigurationError):
        resolve_api_base_url(
            base_url="https://foo.api.infiot.net",
            tenant_url="customer.de.goskope.com",
            sdwan_tenant_name="legacy123",
        )


def test_equivalent_base_url_and_tenant_url_are_accepted() -> None:
    result = resolve_api_base_url(
        base_url="https://legacy123.api.eu.infiot.net/",
        tenant_url="customer.de.goskope.com",
        sdwan_tenant_name="legacy123",
    )

    assert result.api_base_url == "https://legacy123.api.eu.infiot.net"
