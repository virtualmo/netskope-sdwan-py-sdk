from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import ResolutionError


def main() -> None:
    direct_client = SDWANClient(
        base_url="https://customer.api.eu.infiot.net",
        api_token="TOKEN",
    )
    print("Direct base URL:", direct_client.resolved_base_url)
    print("Gateways:", direct_client.gateways.list())

    overridden_client = SDWANClient(
        tenant_url="customer.de.goskope.com",
        sdwan_tenant_name="legacy123",
        api_token="TOKEN",
    )
    print("Resolved from goskope URL:", overridden_client.resolved_base_url)

    # This pattern is supported, but may raise a ResolutionError when the exact SD-WAN
    # tenant hostname cannot be derived safely from the goskope tenant name alone.
    try:
        unresolved_client = SDWANClient(
            tenant_url="customer.de.goskope.com",
            api_token="TOKEN",
        )
        print(unresolved_client.gateways.list())
    except ResolutionError as exc:
        print("Resolution guidance:")
        print(exc)


if __name__ == "__main__":
    main()
