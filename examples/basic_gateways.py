import os

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError


def env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else value


def config_source(*, base_url: str | None, tenant_url: str | None) -> str:
    if os.getenv("NETSKOPESDWAN_BASE_URL"):
        return "environment direct base URL"
    if os.getenv("NETSKOPESDWAN_TENANT_URL"):
        return "environment tenant URL"
    if base_url:
        return "embedded example base URL placeholder"
    if tenant_url:
        return "embedded example tenant URL placeholder"
    return "unknown configuration"


def looks_like_invalid_tenant_error(message: str) -> bool:
    lowered = message.lower()
    return "lookup tenant" in lowered or "tenant not found" in lowered


def main() -> None:
    # This hardcoded base URL is only an example. Replace it with a real tenant
    # URL, or set NETSKOPESDWAN_BASE_URL / NETSKOPESDWAN_TENANT_URL.
    base_url = env("NETSKOPESDWAN_BASE_URL", "https://customer.api.eu.infiot.net")
    tenant_url = env("NETSKOPESDWAN_TENANT_URL")
    sdwan_tenant_name = env("NETSKOPESDWAN_SDWAN_TENANT_NAME")
    api_token = env("NETSKOPESDWAN_API_TOKEN", "TOKEN")

    client = SDWANClient(
        base_url=base_url,
        tenant_url=tenant_url,
        sdwan_tenant_name=sdwan_tenant_name,
        api_token=api_token,
    )

    print(f"Using {config_source(base_url=base_url, tenant_url=tenant_url)}")
    print("Resolved base URL:", client.resolved_base_url)

    try:
        gateways = client.gateways.list()
    except APIResponseError as exc:
        message = str(exc)
        if looks_like_invalid_tenant_error(message):
            print()
            print("Could not list gateways because the tenant URL/base URL is not valid.")
            print(
                "Values like https://customer.api.eu.infiot.net are placeholders for documentation "
                "and examples, not real tenants."
            )
            print(
                "Set a real tenant with NETSKOPESDWAN_BASE_URL or NETSKOPESDWAN_TENANT_URL, "
                "and provide a valid NETSKOPESDWAN_API_TOKEN."
            )
            return

        print()
        print(f"Gateway list failed: {message}")
        return
    except Exception as exc:
        print()
        print(f"Unexpected error while listing gateways: {exc.__class__.__name__}: {exc}")
        return

    print("Gateways:", gateways)


if __name__ == "__main__":
    main()
