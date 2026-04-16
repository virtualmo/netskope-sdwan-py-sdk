from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import APIResponseError, ValidationError
from netskopesdwan.models.download import DownloadResult


@dataclass(frozen=True)
class MonitoringExample:
    name: str
    call: Any


def print_section(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def summarize(value: Any) -> str:
    if isinstance(value, list):
        return f"ok list(len={len(value)})"
    if isinstance(value, dict):
        keys = list(value.keys())[:6]
        return f"ok dict(keys={keys})"
    if isinstance(value, DownloadResult):
        return f"ok DownloadResult(size={len(value.content)} bytes)"
    return "ok"


def looks_like_environment_skip(exc: Exception) -> bool:
    if isinstance(exc, ValidationError):
        return True

    message = str(exc).lower()
    return (
        "http 400" in message
        or "unsupported" in message
        or "not available" in message
        or "not enabled" in message
        or "feature" in message
    )


def print_result(name: str, status: str, detail: str) -> None:
    print(f"{name:<32} {status:<4} {detail}")


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

    print(f"Using gateway: {gateway_name} ({gateway_id})")

    examples = [
        MonitoringExample(
            "get_device_flows_totals",
            lambda: client.v1.monitoring.get_device_flows_totals(gateway_id),
        ),
        MonitoringExample(
            "get_devices_totals",
            lambda: client.v1.monitoring.get_devices_totals(gateway_id),
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
            lambda: client.v1.monitoring.get_system_load(gateway_id),
        ),
        MonitoringExample(
            "get_system_lte",
            lambda: client.v1.monitoring.get_system_lte(gateway_id),
        ),
        MonitoringExample(
            "get_system_memory",
            lambda: client.v1.monitoring.get_system_memory(gateway_id),
        ),
        MonitoringExample(
            "get_system_uptime",
            lambda: client.v1.monitoring.get_system_uptime(gateway_id),
        ),
        MonitoringExample(
            "get_system_wifi",
            lambda: client.v1.monitoring.get_system_wifi(gateway_id),
        ),
        MonitoringExample(
            "get_paths_links",
            lambda: client.v1.monitoring.get_paths_links(gateway_id),
        ),
        MonitoringExample(
            "get_paths_links_totals",
            lambda: client.v1.monitoring.get_paths_links_totals(gateway_id),
        ),
    ]

    passed = 0
    skipped = 0
    failed = 0

    print_section("Monitoring")

    for example in examples:
        try:
            payload = example.call()
        except APIResponseError as exc:
            print_result(example.name, "FAIL", str(exc))
            failed += 1
        except Exception as exc:
            if looks_like_environment_skip(exc):
                print_result(
                    example.name,
                    "SKIP",
                    "unsupported for this gateway/tenant/feature set",
                )
                skipped += 1
            else:
                print_result(
                    example.name,
                    "FAIL",
                    f"{exc.__class__.__name__}: {exc}",
                )
                failed += 1
        else:
            print_result(example.name, "PASS", summarize(payload))
            passed += 1

    print_section("Totals")
    print(f"passed:  {passed}")
    print(f"skipped: {skipped}")
    print(f"failed:  {failed}")


if __name__ == "__main__":
    main()
