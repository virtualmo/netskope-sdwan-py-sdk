from netskopesdwan import SDWANClient


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

    # Generic goskope hosts such as customer.goskope.com are not supported in V1
    # unless the region can be determined deterministically. Use base_url directly
    # for those tenants until DNS/CNAME-based discovery is implemented.
    #
    # unsupported_client = SDWANClient(
    #     tenant_url="customer.goskope.com",
    #     api_token="TOKEN",
    # )


if __name__ == "__main__":
    main()
