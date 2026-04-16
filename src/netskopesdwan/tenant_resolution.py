from __future__ import annotations

from dataclasses import asdict, dataclass
from urllib.parse import urlparse

from .exceptions import ConfigurationError, ResolutionError

_INFIOT_REGIONS = {"eu", "au", "ksa", "ap"}
_GOSKOPE_SUFFIX_TO_REGION = {
    ".eu.goskope.com": ("AM2", "PROD-EU"),
    ".de.goskope.com": ("FR4", "PROD-EU"),
    ".au.goskope.com": ("MEL2", "PROD-AU"),
}
_MP_TO_REGION = {
    "SJC2": "PROD-US",
    "SV5": "PROD-US",
    "DFW3": "PROD-US",
    "SJC1": "PROD-US",
    "FRA2": "PROD-EU",
    "LON3": "PROD-EU",
    "FR4": "PROD-EU",
    "AM2": "PROD-EU",
    "ZUR2": "PROD-EU",
    "RUH1": "PROD-KSA",
    "MEL2": "PROD-AU",
    "SIN2": "PROD-AP",
    "BOM3": "PROD-AP",
}
_REGION_TO_API_SUFFIX = {
    "PROD-US": "api.infiot.net",
    "PROD-EU": "api.eu.infiot.net",
    "PROD-KSA": "api.ksa.infiot.net",
    "PROD-AU": "api.au.infiot.net",
    "PROD-AP": "api.ap.infiot.net",
}


@dataclass(slots=True)
class ResolutionResult:
    input_host: str
    input_type: str
    goskope_tenant_name: str | None
    sdwan_tenant_name: str | None
    home_mp: str | None
    sdwan_region: str | None
    api_base_url: str
    resolution_method: str
    confidence: str

    def to_metadata(self) -> dict[str, str | None]:
        return asdict(self)


def resolve_api_base_url(
    *,
    base_url: str | None,
    tenant_url: str | None,
    sdwan_tenant_name: str | None,
) -> ResolutionResult:
    if base_url and tenant_url:
        base_result = _resolve_single_input(
            raw_value=base_url,
            input_type="base_url",
            sdwan_tenant_name=sdwan_tenant_name,
        )
        tenant_result = _resolve_single_input(
            raw_value=tenant_url,
            input_type="tenant_url",
            sdwan_tenant_name=sdwan_tenant_name,
        )
        if base_result.api_base_url != tenant_result.api_base_url:
            raise ConfigurationError(
                "base_url and tenant_url resolved to different API endpoints: "
                f"{base_result.api_base_url!r} != {tenant_result.api_base_url!r}."
            )
        return base_result

    selected_value = base_url or tenant_url
    selected_type = "base_url" if base_url else "tenant_url"
    if selected_value is None:
        raise ConfigurationError("No base_url or tenant_url value was provided for resolution.")

    return _resolve_single_input(
        raw_value=selected_value,
        input_type=selected_type,
        sdwan_tenant_name=sdwan_tenant_name,
    )


def normalize_url(value: str) -> str:
    host = _extract_host(value)
    if _is_infiot_host(host):
        return f"https://{_normalize_infiot_host(host)}"
    return f"https://{host}"


def _resolve_single_input(
    *,
    raw_value: str,
    input_type: str,
    sdwan_tenant_name: str | None,
) -> ResolutionResult:
    host = _extract_host(raw_value)

    if input_type == "base_url" and _is_goskope_host(host):
        raise ConfigurationError(
            "base_url must point to a Netskope SD-WAN API host such as "
            "'https://<sdwan-tenant>.api.infiot.net'. "
            f"Received goskope tenant host {host!r}. "
            "Use tenant_url for goskope inputs instead."
        )

    if _is_infiot_host(host):
        normalized_host = _normalize_infiot_host(host)
        tenant_name = normalized_host.split(".", 1)[0]
        return ResolutionResult(
            input_host=host,
            input_type="infiot",
            goskope_tenant_name=None,
            sdwan_tenant_name=tenant_name,
            home_mp=None,
            sdwan_region=_infer_region_from_infiot_host(normalized_host),
            api_base_url=f"https://{normalized_host}",
            resolution_method=f"{input_type}:direct-infiot-normalization",
            confidence="high",
        )

    if _is_goskope_host(host):
        return _resolve_goskope_host(
            host=host,
            input_type=input_type,
            sdwan_tenant_name=sdwan_tenant_name,
        )

    raise ResolutionError(
        f"Unsupported tenant or base URL host: {host!r}. Expected a goskope.com or infiot.net host."
    )


def _resolve_goskope_host(
    *,
    host: str,
    input_type: str,
    sdwan_tenant_name: str | None,
) -> ResolutionResult:
    goskope_tenant_name = host.split(".", 1)[0]
    home_mp, region, method = _resolve_goskope_region(host)

    if region is None:
        raise ResolutionError(
            "Could not determine the SD-WAN region from tenant URL: "
            f"{host}\n\n"
            "This SDK currently supports deterministic suffix-based goskope mapping and "
            "keeps DNS/CNAME discovery as a future enhancement.\n\n"
            "Please provide the exact SD-WAN API URL directly, for example:\n\n"
            '    SDWANClient(base_url="https://<sdwan-tenant>.api.infiot.net", api_token="TOKEN")'
        )

    if not sdwan_tenant_name:
        raise ResolutionError(_build_hostname_resolution_error(host, region))

    api_base_url = _build_api_base_url(sdwan_tenant_name, region)
    return ResolutionResult(
        input_host=host,
        input_type="goskope",
        goskope_tenant_name=goskope_tenant_name,
        sdwan_tenant_name=sdwan_tenant_name,
        home_mp=home_mp,
        sdwan_region=region,
        api_base_url=api_base_url,
        resolution_method=f"{input_type}:{method}+sdwan-tenant-override",
        confidence="medium",
    )


def _build_hostname_resolution_error(host: str, region: str) -> str:
    expected_pattern = _build_api_pattern(region)
    return (
        f"Could not determine the exact SD-WAN API URL from tenant URL: {host}\n\n"
        f"The SDK identified the SD-WAN region as: {region}\n"
        "Expected API pattern for this region:\n"
        f"    {expected_pattern}\n\n"
        "However, some tenants, especially older tenants, use an SD-WAN tenant name that "
        "does not match the goskope tenant name.\n\n"
        "Please obtain the SD-WAN API URL from the SD-WAN UI and pass it directly:\n\n"
        f'    SDWANClient(base_url="{expected_pattern}", api_token="TOKEN")\n\n'
        "If you already know the SD-WAN tenant name, you may instead use:\n"
        f'    SDWANClient(tenant_url="{host}", sdwan_tenant_name="<sdwan-tenant>", '
        'api_token="TOKEN")'
    )


def _resolve_goskope_region(host: str) -> tuple[str | None, str | None, str]:
    for suffix, (home_mp, region) in _GOSKOPE_SUFFIX_TO_REGION.items():
        if host.endswith(suffix):
            return home_mp, region, "suffix-mapping"

    parsed_mp = _extract_home_mp_from_host(host)
    if parsed_mp:
        return parsed_mp, _MP_TO_REGION.get(parsed_mp), "hostname-mp-parsing"

    if host.endswith(".goskope.com"):
        return None, None, "unresolved-goskope"

    return None, None, "unsupported-goskope"


def _extract_home_mp_from_host(host: str) -> str | None:
    labels = host.split(".")
    for label in labels:
        parts = label.split("-")
        for part in parts:
            upper = part.upper()
            if upper in _MP_TO_REGION:
                return upper
    return None


def _build_api_pattern(region: str) -> str:
    return f"https://<sdwan-tenant>.{_REGION_TO_API_SUFFIX[region]}"


def _build_api_base_url(sdwan_tenant_name: str, region: str) -> str:
    return f"https://{sdwan_tenant_name}.{_REGION_TO_API_SUFFIX[region]}"


def _extract_host(value: str) -> str:
    candidate = value.strip()
    if not candidate:
        raise ConfigurationError("Tenant or base URL value cannot be empty.")

    parsed = urlparse(candidate if "://" in candidate else f"https://{candidate}")
    if not parsed.hostname:
        raise ConfigurationError(f"Could not parse a valid hostname from {value!r}.")
    return parsed.hostname.lower()


def _is_goskope_host(host: str) -> bool:
    return host.endswith(".goskope.com")


def _is_infiot_host(host: str) -> bool:
    return host.endswith(".infiot.net")


def _normalize_infiot_host(host: str) -> str:
    labels = host.split(".")
    if len(labels) < 3:
        raise ResolutionError(f"Unsupported infiot host format: {host!r}.")

    tenant = labels[0]
    remainder = labels[1:]

    if remainder[0] == "api":
        return host

    if remainder == ["infiot", "net"]:
        return f"{tenant}.api.infiot.net"

    if (
        len(remainder) == 3
        and remainder[1:] == ["infiot", "net"]
        and remainder[0] in _INFIOT_REGIONS
    ):
        return f"{tenant}.api.{remainder[0]}.infiot.net"

    raise ResolutionError(f"Unsupported infiot host format: {host!r}.")


def _infer_region_from_infiot_host(host: str) -> str:
    labels = host.split(".")
    if labels[1] != "api":
        raise ResolutionError(f"Expected normalized infiot host, got {host!r}.")
    if labels[2:] == ["infiot", "net"]:
        return "PROD-US"
    region = labels[2].upper()
    try:
        return {
            "EU": "PROD-EU",
            "AU": "PROD-AU",
            "KSA": "PROD-KSA",
            "AP": "PROD-AP",
        }[region]
    except KeyError as exc:
        raise ResolutionError(f"Unsupported normalized infiot host region in {host!r}.") from exc
