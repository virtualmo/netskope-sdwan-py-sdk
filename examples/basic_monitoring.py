from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError


def print_section(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def main() -> None:
    try:
        client = SDWANClient()
    except Exception as exc:
        print(f"Could not initialize client from environment: {exc.__class__.__name__}: {exc}")
        return

    print_section("Gateway Selection")

    try:
        gateways = client.gateways.list(filter="status:up")
        if not gateways:
            gateways = client.gateways.list()
    except APIResponseError as exc:
        print(f"Could not list gateways: {exc}")
        return
    except Exception as exc:
        print(f"Unexpected error while listing gateways: {exc.__class__.__name__}: {exc}")
        return

    if not gateways:
        print("No gateways were returned by the tenant.")
        return

    gateway = gateways[0]
    gateway_id = gateway.id

    print(f"Using gateway: {gateway_id} ({gateway.name})")

    print_section("Interfaces Latest")
    try:
        payload = client.v1.monitoring.get_interfaces_latest(gateway_id)
        print(payload)
    except APIResponseError as exc:
        print(f"Monitoring call failed: {exc}")
    except Exception as exc:
        print(f"Unexpected error: {exc.__class__.__name__}: {exc}")

    print_section("Paths Latest")
    try:
        payload = client.v1.monitoring.get_paths_latest(gateway_id)
        print(payload)
    except APIResponseError as exc:
        print(f"Monitoring call failed: {exc}")
    except Exception as exc:
        print(f"Unexpected error: {exc.__class__.__name__}: {exc}")

    print_section("Routes Latest")
    try:
        payload = client.v1.monitoring.get_routes_latest(gateway_id)
        print(payload)
    except APIResponseError as exc:
        print(f"Monitoring call failed: {exc}")
    except Exception as exc:
        print(f"Unexpected error: {exc.__class__.__name__}: {exc}")


if __name__ == "__main__":
    main()
