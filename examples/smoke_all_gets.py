from __future__ import annotations

import os
from typing import Any, Callable

from netskopesdwan import SDWANClient


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
            return f"list(len={len(value)}, first_id={getattr(first, 'id', None)!r}, first_name={getattr(first, 'name', None)!r})"
        return f"list(len={len(value)})"

    if hasattr(value, "id"):
        return f"{value.__class__.__name__}(id={getattr(value, 'id', None)!r}, name={getattr(value, 'name', None)!r})"

    if isinstance(value, dict):
        keys = list(value.keys())[:10]
        return f"dict(keys={keys})"

    if isinstance(value, str):
        short = value[:120].replace("\n", "\\n")
        return f"str(len={len(value)}, preview={short!r})"

    return repr(value)


def safe_call(label: str, func: Callable[[], Any]) -> Any | None:
    try:
        result = func()
        print(f"[OK]   {label}: {summarize(result)}")
        return result
    except Exception as exc:
        print(f"[FAIL] {label}: {exc.__class__.__name__}: {exc}")
        return None


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

    # Batch 1
    print_header("Infrastructure / Policy / Network")

    device_groups = safe_call("device_groups.list()", lambda: client.device_groups.list())
    if group_id := first_id(device_groups):
        safe_call(f"device_groups.get({group_id})", lambda: client.device_groups.get(group_id))

    gateway_groups = safe_call("gateway_groups.list()", lambda: client.gateway_groups.list())
    if group_id := first_id(gateway_groups):
        safe_call(f"gateway_groups.get({group_id})", lambda: client.gateway_groups.get(group_id))

    gateway_templates = safe_call("gateway_templates.list()", lambda: client.gateway_templates.list())
    if template_id := first_id(gateway_templates):
        safe_call(
            f"gateway_templates.get({template_id})",
            lambda: client.gateway_templates.get(template_id),
        )

    safe_call("inventory_devices.list()", lambda: client.inventory_devices.list())

    ntp_configs = safe_call("ntp_configs.list()", lambda: client.ntp_configs.list())
    if ntp_id := first_id(ntp_configs):
        safe_call(f"ntp_configs.get({ntp_id})", lambda: client.ntp_configs.get(ntp_id))

    overlay_tags = safe_call("overlay_tags.list()", lambda: client.overlay_tags.list())
    if tag_id := first_id(overlay_tags):
        safe_call(f"overlay_tags.get({tag_id})", lambda: client.overlay_tags.get(tag_id))

    segments = safe_call("segments.list()", lambda: client.segments.list())
    if segment_id := first_id(segments):
        safe_call(f"segments.get({segment_id})", lambda: client.segments.get(segment_id))

    vpn_peers = safe_call("vpn_peers.list()", lambda: client.vpn_peers.list())
    if peer_id := first_id(vpn_peers):
        safe_call(f"vpn_peers.get({peer_id})", lambda: client.vpn_peers.get(peer_id))

    policies = safe_call("policies.list()", lambda: client.policies.list())
    if policy_id := first_id(policies):
        safe_call(f"policies.get({policy_id})", lambda: client.policies.get(policy_id))

    radius_servers = safe_call("radius_servers.list()", lambda: client.radius_servers.list())
    if radius_id := first_id(radius_servers):
        safe_call(f"radius_servers.get({radius_id})", lambda: client.radius_servers.get(radius_id))

    # Gateways
    print_header("Gateways")

    gateways = safe_call("gateways.list()", lambda: client.gateways.list())
    if gateway_id := first_id(gateways):
        safe_call(f"gateways.get({gateway_id})", lambda: client.gateways.get(gateway_id))
        safe_call(
            f"gateways.get_localui_password({gateway_id})",
            lambda: client.gateways.get_localui_password(gateway_id),
        )
        safe_call(
            f"gateways.get_ssh_password({gateway_id})",
            lambda: client.gateways.get_ssh_password(gateway_id),
        )

    # Batch 2
    print_header("Clients / Tenants / Users / Cloud")

    client_templates = safe_call("client_templates.list()", lambda: client.client_templates.list())
    if template_id := first_id(client_templates):
        safe_call(f"client_templates.get({template_id})", lambda: client.client_templates.get(template_id))

    clients = safe_call("clients.list()", lambda: client.clients.list())
    if client_id := first_id(clients):
        safe_call(f"clients.get({client_id})", lambda: client.clients.get(client_id))

    cloud_accounts = safe_call("cloud_accounts.list()", lambda: client.cloud_accounts.list())
    if cloud_id := first_id(cloud_accounts):
        safe_call(f"cloud_accounts.get({cloud_id})", lambda: client.cloud_accounts.get(cloud_id))

    tenants = safe_call("tenants.list()", lambda: client.tenants.list())
    if tenant_id := first_id(tenants):
        safe_call(f"tenants.get({tenant_id})", lambda: client.tenants.get(tenant_id))

    user_groups = safe_call("user_groups.list()", lambda: client.user_groups.list())
    if group_id := first_id(user_groups):
        safe_call(f"user_groups.get({group_id})", lambda: client.user_groups.get(group_id))

    users = safe_call("users.list()", lambda: client.users.list())
    if user_id := first_id(users):
        safe_call(f"users.get({user_id})", lambda: client.users.get(user_id))

    # Batch 3
    print_header("Audit / Controllers / Site Commands / Software")

    audit_from = env("NETSKOPESDWAN_AUDIT_FROM")
    audit_to = env("NETSKOPESDWAN_AUDIT_TO")
    audit_type = env("NETSKOPESDWAN_AUDIT_TYPE")
    audit_subtype = env("NETSKOPESDWAN_AUDIT_SUBTYPE")
    audit_activity = env("NETSKOPESDWAN_AUDIT_ACTIVITY")

    if audit_from and audit_to:
        safe_call(
            "audit_events.list(...)",
            lambda: client.audit_events.list(
                created_at_from=audit_from,
                created_at_to=audit_to,
                type=audit_type,
                subtype=audit_subtype,
                activity=audit_activity,
            ),
        )
    else:
        print(
            "[SKIP] audit_events.list(...): set NETSKOPESDWAN_AUDIT_FROM and "
            "NETSKOPESDWAN_AUDIT_TO"
        )

    controller_operators = safe_call(
        "controller_operators.list()",
        lambda: client.controller_operators.list(),
    )
    if operator_id := first_id(controller_operators):
        safe_call(
            f"controller_operators.get({operator_id})",
            lambda: client.controller_operators.get(operator_id),
        )

    controllers = safe_call("controllers.list()", lambda: client.controllers.list())
    if controller_id := first_id(controllers):
        safe_call(f"controllers.get({controller_id})", lambda: client.controllers.get(controller_id))
        safe_call(
            f"controllers.get_operator_status({controller_id})",
            lambda: client.controllers.get_operator_status(controller_id),
        )

    site_commands = safe_call("site_commands.list()", lambda: client.site_commands.list())
    if command_id := first_id(site_commands):
        safe_call(f"site_commands.get({command_id})", lambda: client.site_commands.get(command_id))
        output_name = env("NETSKOPESDWAN_SITE_COMMAND_OUTPUT_NAME")
        if output_name:
            safe_call(
                f"site_commands.get_output({command_id}, {output_name})",
                lambda: client.site_commands.get_output(command_id, output_name),
            )
        else:
            print("[SKIP] site_commands.get_output(...): set NETSKOPESDWAN_SITE_COMMAND_OUTPUT_NAME")

    safe_call("software.list_versions()", lambda: client.software.list_versions())
    safe_call("software.list_downloads()", lambda: client.software.list_downloads())

    # Batch 4
    print_header("Addressing / Applications / Certificates / Auth")

    address_groups = safe_call("address_groups.list()", lambda: client.address_groups.list())
    if group_id := first_id(address_groups):
        safe_call(f"address_groups.get({group_id})", lambda: client.address_groups.get(group_id))
        safe_call(
            f"address_groups.list_address_objects({group_id})",
            lambda: client.address_groups.list_address_objects(group_id),
        )

    safe_call("applications.list_categories()", lambda: client.applications.list_categories())

    custom_apps = safe_call("applications.list_custom_apps()", lambda: client.applications.list_custom_apps())
    if app_id := first_id(custom_apps):
        safe_call(
            f"applications.get_custom_app({app_id})",
            lambda: client.applications.get_custom_app(app_id),
        )

    safe_call("applications.list_qosmos_apps()", lambda: client.applications.list_qosmos_apps())
    safe_call(
        "applications.list_webroot_categories()",
        lambda: client.applications.list_webroot_categories(),
    )

    ca_certs = safe_call("ca_certificates.list()", lambda: client.ca_certificates.list())
    if cert_id := first_id(ca_certs):
        safe_call(f"ca_certificates.get({cert_id})", lambda: client.ca_certificates.get(cert_id))

    safe_call("jwks.get()", lambda: client.jwks.get())


if __name__ == "__main__":
    main()
