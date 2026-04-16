from pprint import pprint

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError


def main() -> None:
    try:
        client = SDWANClient()
    except Exception as exc:
        print(f"Could not initialize client from environment: {exc.__class__.__name__}: {exc}")
        return

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
    gateway_name = gateway.name or "<unnamed gateway>"

    print(f"Using gateway: {gateway_name} ({gateway_id})")
    print("\nTelemetry overview")
    print("------------------")

    try:
        payload = client.gateways.get_telemetry_overview(gateway_id)
    except APIResponseError as exc:
        print(f"Telemetry request failed: {exc}")
        return
    except Exception as exc:
        print(f"Unexpected error while fetching telemetry: {exc.__class__.__name__}: {exc}")
        return

    pprint(payload, sort_dicts=False)


if __name__ == "__main__":
    main()
