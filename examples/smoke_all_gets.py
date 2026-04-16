from __future__ import annotations

import os
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Any

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import PermissionDeniedError
from netskopesdwan.models import DownloadResult


def env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else value


def print_header(title: str) -> None:
    print(f"\n{'=' * 80}")
    print(title)
    print(f"{'=' * 80}")


def summarize(value: Any) -> str:
    if value is None:
        return "None"

    if isinstance(value, list):
        first = value[0] if value else None
        if hasattr(first, "id"):
            return (
                "list("
                f"len={len(value)}, "
                f"first_id={getattr(first, 'id', None)!r}, "
                f"first_name={getattr(first, 'name', None)!r})"
            )
        return f"list(len={len(value)})"

    if hasattr(value, "id"):
        return (
            f"{value.__class__.__name__}("
            f"id={getattr(value, 'id', None)!r}, "
            f"name={getattr(value, 'name', None)!r})"
        )

    if isinstance(value, dict):
        keys = list(value.keys())[:10]
        return f"dict(keys={keys})"

    if isinstance(value, DownloadResult):
        return (
            f"DownloadResult(size={len(value.content)} bytes, "
            f"content_type={value.content_type!r}, "
            f"filename={value.filename!r})"
        )

    if isinstance(value, str):
        short = value[:120].replace("\n", "\\n")
        return f"str(len={len(value)}, preview={short!r})"

    if isinstance(value, bytes):
        return f"bytes(len={len(value)})"

    return repr(value)


def default_audit_range() -> tuple[str, str]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=24)
    return to_iso8601_z(start), to_iso8601_z(end)


def to_iso8601_z(value: datetime) -> str:
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_call(
    results: dict[str, list[str]],
    label: str,
    func: Callable[[], Any],
) -> Any | None:
    try:
        result = func()
    except PermissionDeniedError as exc:
        print(f"[PERM] {label}: {exc}")
        results["permission"].append(label)
        return None
    except Exception as exc:
        print(f"[FAIL] {label}: {exc.__class__.__name__}: {exc}")
        results["failure"].append(label)
        return None

    print(f"[OK]   {label}: {summarize(result)}")
    results["success"].append(label)
    return result


def skip(results: dict[str, list[str]], label: str, reason: str) -> None:
    print(f"[SKIP] {label}: {reason}")
    results["skip"].append(label)


def first_id(records: Any) -> str | None:
    if not isinstance(records, list) or not records:
        return None
    first = records[0]
    return getattr(first, "id", None)


def main() -> None:
    base_url = env("NETSKOPESDWAN_BASE_URL")
    tenant_url = env("NETSKOPESDWAN_TENANT_URL")
    api_token = env("NETSKOPESDWAN_API_TOKEN")
    sdwan_tenant_name = env("NETSKOPESDWAN_SDWAN_TENANT_NAME")
    results = {"success": [], "permission": [], "failure": [], "skip": []}

    if not api_token:
        raise SystemExit("Missing NETSKOPESDWAN_API_TOKEN")

    if not base_url and not tenant_url:
        raise SystemExit("Set NETSKOPESDWAN_BASE_URL or NETSKOPESDWAN_TENANT_URL")

    client = SDWANClient(
        base_url=base_url,
        tenant_url=tenant_url,
        sdwan_tenant_name=sdwan_tenant_name,
        api_token=api_token,
    )

    print_header("Connection")
    print("Resolved base URL:", client.resolved_base_url)
    print("Resolution metadata:", client.resolution_metadata)

    print_header("Infrastructure / Policy / Network")

    device_groups = safe_call(
        results,
        "device_groups.list()",
        lambda: client.device_groups.list(),
    )
    if group_id := first_id(device_groups):
        safe_call(
            results,
            f"device_groups.get({group_id})",
            lambda: client.device_groups.get(group_id),
        )

    gateway_groups = safe_call(
        results,
        "gateway_groups.list()",
        lambda: client.gateway_groups.list(),
    )
    if group_id := first_id(gateway_groups):
        safe_call(
            results,
            f"gateway_groups.get({group_id})",
            lambda: client.gateway_groups.get(group_id),
        )

    gateway_templates = safe_call(
        results,
        "gateway_templates.list()",
        lambda: client.gateway_templates.list(),
    )
    if template_id := first_id(gateway_templates):
        safe_call(
            results,
            f"gateway_templates.get({template_id})",
            lambda: client.gateway_templates.get(template_id),
        )

    safe_call(results, "inventory_devices.list()", lambda: client.inventory_devices.list())

    ntp_configs = safe_call(results, "ntp_configs.list()", lambda: client.ntp_configs.list())
    if ntp_id := first_id(ntp_configs):
        safe_call(results, f"ntp_configs.get({ntp_id})", lambda: client.ntp_configs.get(ntp_id))

    overlay_tags = safe_call(results, "overlay_tags.list()", lambda: client.overlay_tags.list())
    if tag_id := first_id(overlay_tags):
        safe_call(results, f"overlay_tags.get({tag_id})", lambda: client.overlay_tags.get(tag_id))

    segments = safe_call(results, "segments.list()", lambda: client.segments.list())
    if segment_id := first_id(segments):
        safe_call(results, f"segments.get({segment_id})", lambda: client.segments.get(segment_id))

    vpn_peers = safe_call(results, "vpn_peers.list()", lambda: client.vpn_peers.list())
    if peer_id := first_id(vpn_peers):
        safe_call(results, f"vpn_peers.get({peer_id})", lambda: client.vpn_peers.get(peer_id))

    policies = safe_call(results, "policies.list()", lambda: client.policies.list())
    if policy_id := first_id(policies):
        safe_call(results, f"policies.get({policy_id})", lambda: client.policies.get(policy_id))

    radius_servers = safe_call(
        results,
        "radius_servers.list()",
        lambda: client.radius_servers.list(),
    )
    if radius_id := first_id(radius_servers):
        safe_call(
            results,
            f"radius_servers.get({radius_id})",
            lambda: client.radius_servers.get(radius_id),
        )

    print_header("Gateways")

    gateways = safe_call(results, "gateways.list()", lambda: client.gateways.list())
    if gateway_id := first_id(gateways):
        safe_call(results, f"gateways.get({gateway_id})", lambda: client.gateways.get(gateway_id))
        safe_call(
            results,
            f"gateways.get_localui_password({gateway_id})",
            lambda: client.gateways.get_localui_password(gateway_id),
        )
        safe_call(
            results,
            f"gateways.get_ssh_password({gateway_id})",
            lambda: client.gateways.get_ssh_password(gateway_id),
        )

    print_header("Clients / Tenants / Users / Cloud")

    client_templates = safe_call(
        results,
        "client_templates.list()",
        lambda: client.client_templates.list(),
    )
    if template_id := first_id(client_templates):
        safe_call(
            results,
            f"client_templates.get({template_id})",
            lambda: client.client_templates.get(template_id),
        )

    clients = safe_call(results, "clients.list()", lambda: client.clients.list())
    if client_id := first_id(clients):
        safe_call(results, f"clients.get({client_id})", lambda: client.clients.get(client_id))

    cloud_accounts = safe_call(
        results,
        "cloud_accounts.list()",
        lambda: client.cloud_accounts.list(),
    )
    if cloud_id := first_id(cloud_accounts):
        safe_call(
            results,
            f"cloud_accounts.get({cloud_id})",
            lambda: client.cloud_accounts.get(cloud_id),
        )

    tenants = safe_call(results, "tenants.list()", lambda: client.tenants.list())
    if tenant_id := first_id(tenants):
        safe_call(results, f"tenants.get({tenant_id})", lambda: client.tenants.get(tenant_id))

    user_groups = safe_call(results, "user_groups.list()", lambda: client.user_groups.list())
    if group_id := first_id(user_groups):
        safe_call(results, f"user_groups.get({group_id})", lambda: client.user_groups.get(group_id))

    users = safe_call(results, "users.list()", lambda: client.users.list())
    if user_id := first_id(users):
        safe_call(results, f"users.get({user_id})", lambda: client.users.get(user_id))

    print_header("Audit / Controllers / Site Commands / Software")

    audit_from = env("NETSKOPESDWAN_AUDIT_FROM")
    audit_to = env("NETSKOPESDWAN_AUDIT_TO")
    audit_type = env("NETSKOPESDWAN_AUDIT_TYPE")
    audit_subtype = env("NETSKOPESDWAN_AUDIT_SUBTYPE")
    audit_activity = env("NETSKOPESDWAN_AUDIT_ACTIVITY")
    if not audit_from or not audit_to:
        audit_from, audit_to = default_audit_range()
        print(f"Using default audit window: {audit_from} -> {audit_to}")

    safe_call(
        results,
        "audit_events.list(...)",
        lambda: client.audit_events.list(
            created_at_from=audit_from,
            created_at_to=audit_to,
            type=audit_type,
            subtype=audit_subtype,
            activity=audit_activity,
        ),
    )

    controller_operators = safe_call(
        results,
        "controller_operators.list()",
        lambda: client.controller_operators.list(),
    )
    if operator_id := first_id(controller_operators):
        safe_call(
            results,
            f"controller_operators.get({operator_id})",
            lambda: client.controller_operators.get(operator_id),
        )

    controllers = safe_call(
        results,
        "controllers.list()",
        lambda: client.controllers.list(),
    )
    if controller_id := first_id(controllers):
        safe_call(
            results,
            f"controllers.get({controller_id})",
            lambda: client.controllers.get(controller_id),
        )
        safe_call(
            results,
            f"controllers.get_operator_status({controller_id})",
            lambda: client.controllers.get_operator_status(controller_id),
        )

    site_commands = safe_call(
        results,
        "site_commands.list()",
        lambda: client.site_commands.list(),
    )
    if command_id := first_id(site_commands):
        safe_call(
            results,
            f"site_commands.get({command_id})",
            lambda: client.site_commands.get(command_id),
        )
        output_name = env("NETSKOPESDWAN_SITE_COMMAND_OUTPUT_NAME")
        if output_name:
            safe_call(
                results,
                f"site_commands.get_output({command_id}, {output_name})",
                lambda: client.site_commands.get_output(command_id, output_name),
            )
        else:
            skip(
                results,
                "site_commands.get_output(...)",
                "set NETSKOPESDWAN_SITE_COMMAND_OUTPUT_NAME",
            )

    safe_call(results, "software.list_versions()", lambda: client.software.list_versions())
    safe_call(results, "software.list_downloads()", lambda: client.software.list_downloads())

    print_header("Addressing / Applications / Certificates / Auth")

    address_groups = safe_call(
        results,
        "address_groups.list()",
        lambda: client.address_groups.list(),
    )
    if group_id := first_id(address_groups):
        safe_call(
            results,
            f"address_groups.get({group_id})",
            lambda: client.address_groups.get(group_id),
        )
        safe_call(
            results,
            f"address_groups.list_address_objects({group_id})",
            lambda: client.address_groups.list_address_objects(group_id),
        )

    safe_call(
        results,
        "applications.list_categories()",
        lambda: client.applications.list_categories(),
    )

    custom_apps = safe_call(
        results,
        "applications.list_custom_apps()",
        lambda: client.applications.list_custom_apps(),
    )
    if app_id := first_id(custom_apps):
        safe_call(
            results,
            f"applications.get_custom_app({app_id})",
            lambda: client.applications.get_custom_app(app_id),
        )

    safe_call(
        results,
        "applications.list_qosmos_apps()",
        lambda: client.applications.list_qosmos_apps(),
    )
    safe_call(
        results,
        "applications.list_webroot_categories()",
        lambda: client.applications.list_webroot_categories(),
    )

    ca_certs = safe_call(
        results,
        "ca_certificates.list()",
        lambda: client.ca_certificates.list(),
    )
    if cert_id := first_id(ca_certs):
        safe_call(
            results,
            f"ca_certificates.get({cert_id})",
            lambda: client.ca_certificates.get(cert_id),
        )

    safe_call(results, "jwks.get()", lambda: client.jwks.get())

    print_header("Summary")
    print(f"Successes:   {len(results['success'])}")
    print(f"Permissions: {len(results['permission'])}")
    print(f"Failures:    {len(results['failure'])}")
    print(f"Skipped:     {len(results['skip'])}")

    if results["permission"]:
        print("Permission-limited calls:", ", ".join(results["permission"]))
    if results["failure"]:
        print("Failures:", ", ".join(results["failure"]))


if __name__ == "__main__":
    main()
