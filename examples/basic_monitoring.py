from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pprint import pprint
from typing import Any

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError, ValidationError


@dataclass(frozen=True)
class MonitoringExample:
    name: str
    call: Any


def print_section(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def looks_like_unsupported_monitoring_error(message: str) -> bool:
    lowered = message.lower()
    return (
        "http 400" in lowered
        or "unsupported" in lowered
        or "not available" in lowered
        or "not enabled" in lowered
        or "feature" in lowered
    )


def print_payload(value: Any) -> None:
    pprint(value, sort_dicts=False)


def default_time_window() -> tuple[str, str]:
    end = datetime.now(UTC)
    start = end - timedelta(minutes=60)
    return to_iso8601_z(start), to_iso8601_z(end)


def to_iso8601_z(value: datetime) -> str:
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_example(example: MonitoringExample) -> None:
    print_section(f"Monitoring: {example.name}")

    try:
        payload = example.call()
    except ValidationError:
        print("Unsupported for this gateway/tenant/feature set")
    except APIResponseError as exc:
        message = str(exc)
        if looks_like_unsupported_monitoring_error(message):
            print("Unsupported for this gateway/tenant/feature set")
        else:
            print(f"API error: {message}")
    except Exception as exc:
        print(f"Unexpected error: {exc.__class__.__name__}: {exc}")
    else:
        print_payload(payload)


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
    gateway_name = gateway.name or "<unnamed gateway>"
    start_date, end_date = default_time_window()

    print(f"Using gateway: {gateway_name} ({gateway_id})")
    print(f"Monitoring window: {start_date} -> {end_date}")

    examples = [
        MonitoringExample(
            "get_device_flows_totals",
            lambda: client.v1.monitoring.get_device_flows_totals(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
            ),
        ),
        MonitoringExample(
            "get_devices_totals",
            lambda: client.v1.monitoring.get_devices_totals(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
            ),
        ),
        MonitoringExample(
            "get_interfaces_latest",
            lambda: client.v1.monitoring.get_interfaces_latest(gateway_id),
        ),
        MonitoringExample(
            "get_paths_latest",
            lambda: client.v1.monitoring.get_paths_latest(gateway_id),
        ),
        MonitoringExample(
            "get_routes_latest",
            lambda: client.v1.monitoring.get_routes_latest(gateway_id),
        ),
        MonitoringExample(
            "get_system_load",
            lambda: client.v1.monitoring.get_system_load(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
            ),
        ),
        MonitoringExample(
            "get_system_lte",
            lambda: client.v1.monitoring.get_system_lte(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
            ),
        ),
        MonitoringExample(
            "get_system_memory",
            lambda: client.v1.monitoring.get_system_memory(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
            ),
        ),
        MonitoringExample(
            "get_system_uptime",
            lambda: client.v1.monitoring.get_system_uptime(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
            ),
        ),
        MonitoringExample(
            "get_system_wifi",
            lambda: client.v1.monitoring.get_system_wifi(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
            ),
        ),
        MonitoringExample(
            "get_paths_links",
            lambda: client.v1.monitoring.get_paths_links(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
                metric="latency",
            ),
        ),
        MonitoringExample(
            "get_paths_links_totals",
            lambda: client.v1.monitoring.get_paths_links_totals(
                gateway_id,
                start_datetime=start_date,
                end_datetime=end_date,
            ),
        ),
    ]

    for example in examples:
        run_example(example)


if __name__ == "__main__":
    main()
