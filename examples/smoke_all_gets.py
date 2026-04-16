from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from netskopesdwan import SDWANClient
from netskopesdwan.exceptions import NotFoundError, PermissionDeniedError, ValidationError
from netskopesdwan.models import DownloadResult


@dataclass(frozen=True)
class SmokeTarget:
    name: str
    label: str
    call: Any
    seed_from: str | None = None
    seed_extractor: Any | None = None
    skip_if: Any | None = None
    exception_classifier: Any | None = None
    try_multiple_seeds: bool = False
    visible: bool = True


@dataclass
class SmokeResult:
    status: str
    reason: str
    attempted: bool
    value: Any = None


def env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else value


def default_audit_range() -> tuple[str, str]:
    end = datetime.now(UTC)
    start = end - timedelta(hours=24)
    return to_iso8601_z(start), to_iso8601_z(end)


def to_iso8601_z(value: datetime) -> str:
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def summarize(value: Any) -> str:
    if value is None:
        return "ok"

    if isinstance(value, list):
        first = value[0] if value else None
        if hasattr(first, "id"):
            return (
                "ok "
                f"list(len={len(value)}, "
                f"first_id={getattr(first, 'id', None)!r}, "
                f"first_name={getattr(first, 'name', None)!r})"
            )
        if isinstance(first, dict):
            keys = list(first.keys())[:4]
            return f"ok list(len={len(value)}, first_keys={keys})"
        return f"ok list(len={len(value)})"

    if hasattr(value, "id"):
        return (
            f"ok {value.__class__.__name__}("
            f"id={getattr(value, 'id', None)!r}, "
            f"name={getattr(value, 'name', None)!r})"
        )

    if isinstance(value, DownloadResult):
        return (
            f"ok DownloadResult("
            f"size={len(value.content)} bytes, "
            f"content_type={value.content_type!r}, "
            f"filename={value.filename!r})"
        )

    if isinstance(value, dict):
        keys = list(value.keys())[:6]
        return f"ok dict(keys={keys})"

    if isinstance(value, str):
        preview = value[:80].replace("\n", "\\n")
        return f"ok str(len={len(value)}, preview={preview!r})"

    return f"ok {value!r}"


def short_error(exc: Exception) -> str:
    text = str(exc).strip() or exc.__class__.__name__
    text = text.replace("\n", " ")
    if len(text) > 140:
        return f"{exc.__class__.__name__}: {text[:137]}..."
    return f"{exc.__class__.__name__}: {text}"


def first_item(value: Any) -> Any | None:
    if isinstance(value, list) and value:
        return value[0]
    return None


def extract_first_id(value: Any) -> str | None:
    item = first_item(value)
    if item is None:
        return None
    item_id = getattr(item, "id", None)
    if isinstance(item_id, str) and item_id.strip():
        return item_id.strip()
    if isinstance(item, dict):
        raw_id = item.get("id")
        if raw_id is None:
            return None
        text = str(raw_id).strip()
        return text or None
    return None


def extract_first_name(value: Any) -> str | None:
    item = first_item(value)
    if not isinstance(item, dict):
        return None
    raw_name = item.get("name")
    if raw_name is None:
        return None
    text = str(raw_name).strip()
    return text or None


def require_site_command_output_name() -> str | None:
    if env("NETSKOPESDWAN_SITE_COMMAND_OUTPUT_NAME"):
        return None
    return "set NETSKOPESDWAN_SITE_COMMAND_OUTPUT_NAME to smoke get_output(...)"


def classify_site_command_output_exception(exc: Exception) -> SmokeResult | None:
    if isinstance(exc, NotFoundError):
        return SmokeResult(
            "SKIP",
            "output name not valid for this command result",
            attempted=True,
        )
    return None


def classify_optional_monitoring_exception(exc: Exception) -> SmokeResult | None:
    if isinstance(exc, ValidationError):
        return SmokeResult(
            "SKIP",
            "unsupported for this tenant/gateway/feature set",
            attempted=True,
        )
    return None


def build_targets(
    *,
    audit_from: str,
    audit_to: str,
    site_command_output_name: str | None,
) -> list[SmokeTarget]:
    # Add new GET endpoints here. Seeded targets reuse prior list results through the cache.
    return [
        SmokeTarget(
            "address_groups.list",
            "address_groups.list()",
            lambda c, _: c.address_groups.list(),
        ),
        SmokeTarget(
            "address_groups.get",
            "address_groups.get(id)",
            lambda c, seed: c.address_groups.get(seed),
            seed_from="address_groups.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "address_groups.list_address_objects",
            "address_groups.list_address_objects(group_id)",
            lambda c, seed: c.address_groups.list_address_objects(seed),
            seed_from="address_groups.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "audit_events.list",
            "audit_events.list(...)",
            lambda c, _: c.audit_events.list(
                created_at_from=audit_from,
                created_at_to=audit_to,
            ),
        ),
        SmokeTarget(
            "applications.list_categories",
            "applications.list_categories()",
            lambda c, _: c.applications.list_categories(),
        ),
        SmokeTarget(
            "applications.list_custom_apps",
            "applications.list_custom_apps()",
            lambda c, _: c.applications.list_custom_apps(),
        ),
        SmokeTarget(
            "applications.get_custom_app",
            "applications.get_custom_app(id)",
            lambda c, seed: c.applications.get_custom_app(seed),
            seed_from="applications.list_custom_apps",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "applications.list_qosmos_apps",
            "applications.list_qosmos_apps()",
            lambda c, _: c.applications.list_qosmos_apps(),
        ),
        SmokeTarget(
            "applications.list_webroot_categories",
            "applications.list_webroot_categories()",
            lambda c, _: c.applications.list_webroot_categories(),
        ),
        SmokeTarget(
            "ca_certificates.list",
            "ca_certificates.list()",
            lambda c, _: c.ca_certificates.list(),
        ),
        SmokeTarget(
            "ca_certificates.get",
            "ca_certificates.get(id)",
            lambda c, seed: c.ca_certificates.get(seed),
            seed_from="ca_certificates.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "client_templates.list",
            "client_templates.list()",
            lambda c, _: c.client_templates.list(),
        ),
        SmokeTarget(
            "client_templates.get",
            "client_templates.get(id)",
            lambda c, seed: c.client_templates.get(seed),
            seed_from="client_templates.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget("clients.list", "clients.list()", lambda c, _: c.clients.list()),
        SmokeTarget(
            "clients.get",
            "clients.get(id)",
            lambda c, seed: c.clients.get(seed),
            seed_from="clients.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "cloud_accounts.list",
            "cloud_accounts.list()",
            lambda c, _: c.cloud_accounts.list(),
        ),
        SmokeTarget(
            "cloud_accounts.get",
            "cloud_accounts.get(id)",
            lambda c, seed: c.cloud_accounts.get(seed),
            seed_from="cloud_accounts.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "controller_operators.list",
            "controller_operators.list()",
            lambda c, _: c.controller_operators.list(),
        ),
        SmokeTarget(
            "controller_operators.get",
            "controller_operators.get(id)",
            lambda c, seed: c.controller_operators.get(seed),
            seed_from="controller_operators.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "controllers.list",
            "controllers.list()",
            lambda c, _: c.controllers.list(),
        ),
        SmokeTarget(
            "controllers.get",
            "controllers.get(id)",
            lambda c, seed: c.controllers.get(seed),
            seed_from="controllers.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "controllers.get_operator_status",
            "controllers.get_operator_status(id)",
            lambda c, seed: c.controllers.get_operator_status(seed),
            seed_from="controllers.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "device_groups.list",
            "device_groups.list()",
            lambda c, _: c.device_groups.list(),
        ),
        SmokeTarget(
            "device_groups.get",
            "device_groups.get(id)",
            lambda c, seed: c.device_groups.get(seed),
            seed_from="device_groups.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "gateway_groups.list",
            "gateway_groups.list()",
            lambda c, _: c.gateway_groups.list(),
        ),
        SmokeTarget(
            "gateway_groups.get",
            "gateway_groups.get(id)",
            lambda c, seed: c.gateway_groups.get(seed),
            seed_from="gateway_groups.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget("gateways.list", "gateways.list()", lambda c, _: c.gateways.list()),
        SmokeTarget(
            "gateways.list_prefer_up_for_monitoring",
            "gateways.list(filter=status:up) for monitoring",
            lambda c, _: preferred_gateway_candidates(c),
            visible=False,
        ),
        SmokeTarget(
            "gateways.get",
            "gateways.get(id)",
            lambda c, seed: c.gateways.get(seed),
            seed_from="gateways.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "gateways.get_localui_password",
            "gateways.get_localui_password(id)",
            lambda c, seed: c.gateways.get_localui_password(seed),
            seed_from="gateways.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "gateways.get_ssh_password",
            "gateways.get_ssh_password(id)",
            lambda c, seed: c.gateways.get_ssh_password(seed),
            seed_from="gateways.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "gateway_templates.list",
            "gateway_templates.list()",
            lambda c, _: c.gateway_templates.list(),
        ),
        SmokeTarget(
            "gateway_templates.get",
            "gateway_templates.get(id)",
            lambda c, seed: c.gateway_templates.get(seed),
            seed_from="gateway_templates.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "inventory_devices.list",
            "inventory_devices.list()",
            lambda c, _: c.inventory_devices.list(),
        ),
        SmokeTarget("jwks.get", "jwks.get()", lambda c, _: c.jwks.get()),
        SmokeTarget(
            "ntp_configs.list",
            "ntp_configs.list()",
            lambda c, _: c.ntp_configs.list(),
        ),
        SmokeTarget(
            "ntp_configs.get",
            "ntp_configs.get(id)",
            lambda c, seed: c.ntp_configs.get(seed),
            seed_from="ntp_configs.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "overlay_tags.list",
            "overlay_tags.list()",
            lambda c, _: c.overlay_tags.list(),
        ),
        SmokeTarget(
            "overlay_tags.get",
            "overlay_tags.get(id)",
            lambda c, seed: c.overlay_tags.get(seed),
            seed_from="overlay_tags.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget("policies.list", "policies.list()", lambda c, _: c.policies.list()),
        SmokeTarget(
            "policies.get",
            "policies.get(id)",
            lambda c, seed: c.policies.get(seed),
            seed_from="policies.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "radius_servers.list",
            "radius_servers.list()",
            lambda c, _: c.radius_servers.list(),
        ),
        SmokeTarget(
            "radius_servers.get",
            "radius_servers.get(id)",
            lambda c, seed: c.radius_servers.get(seed),
            seed_from="radius_servers.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget("segments.list", "segments.list()", lambda c, _: c.segments.list()),
        SmokeTarget(
            "segments.get",
            "segments.get(id)",
            lambda c, seed: c.segments.get(seed),
            seed_from="segments.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "site_commands.list",
            "site_commands.list()",
            lambda c, _: c.site_commands.list(),
        ),
        SmokeTarget(
            "site_commands.get",
            "site_commands.get(id)",
            lambda c, seed: c.site_commands.get(seed),
            seed_from="site_commands.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "site_commands.get_output",
            "site_commands.get_output(id, name)",
            lambda c, seed: c.site_commands.get_output(seed, site_command_output_name),
            seed_from="site_commands.list",
            seed_extractor=extract_first_id,
            skip_if=require_site_command_output_name,
            exception_classifier=classify_site_command_output_exception,
        ),
        SmokeTarget(
            "software.list_versions",
            "software.list_versions()",
            lambda c, _: c.software.list_versions(),
        ),
        SmokeTarget(
            "software.list_downloads",
            "software.list_downloads()",
            lambda c, _: c.software.list_downloads(),
        ),
        SmokeTarget("tenants.list", "tenants.list()", lambda c, _: c.tenants.list()),
        SmokeTarget(
            "tenants.get",
            "tenants.get(id)",
            lambda c, seed: c.tenants.get(seed),
            seed_from="tenants.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "user_groups.list",
            "user_groups.list()",
            lambda c, _: c.user_groups.list(),
        ),
        SmokeTarget(
            "user_groups.get",
            "user_groups.get(id)",
            lambda c, seed: c.user_groups.get(seed),
            seed_from="user_groups.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget("users.list", "users.list()", lambda c, _: c.users.list()),
        SmokeTarget(
            "users.get",
            "users.get(id)",
            lambda c, seed: c.users.get(seed),
            seed_from="users.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "vpn_peers.list",
            "vpn_peers.list()",
            lambda c, _: c.vpn_peers.list(),
        ),
        SmokeTarget(
            "vpn_peers.get",
            "vpn_peers.get(id)",
            lambda c, seed: c.vpn_peers.get(seed),
            seed_from="vpn_peers.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "v1.edges.list",
            "v1.edges.list()",
            lambda c, _: c.v1.edges.list(),
        ),
        SmokeTarget(
            "v1.edges.get",
            "v1.edges.get(id)",
            lambda c, seed: c.v1.edges.get(seed),
            seed_from="v1.edges.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "v1.edges.list_interfaces",
            "v1.edges.list_interfaces(edge_id)",
            lambda c, seed: c.v1.edges.list_interfaces(seed),
            seed_from="v1.edges.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "v1.edges.get_interface",
            "v1.edges.get_interface(edge_id, interface_name)",
            lambda c, seed: c.v1.edges.get_interface(seed["edge_id"], seed["interface_name"]),
            seed_from="v1.edges.list_interfaces",
            seed_extractor=lambda value: build_named_seed(
                value,
                source_target="v1.edges.list_interfaces",
                upstream_id_target="v1.edges.list",
            ),
        ),
        SmokeTarget(
            "v1.edges.list_gateway_interfaces",
            "v1.edges.list_gateway_interfaces(edge_id)",
            lambda c, seed: c.v1.edges.list_gateway_interfaces(seed),
            seed_from="v1.edges.list",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "v1.edges.get_gateway_interface",
            "v1.edges.get_gateway_interface(edge_id, interface_name)",
            lambda c, seed: c.v1.edges.get_gateway_interface(
                seed["edge_id"],
                seed["interface_name"],
            ),
            seed_from="v1.edges.list_gateway_interfaces",
            seed_extractor=lambda value: build_named_seed(
                value,
                source_target="v1.edges.list_gateway_interfaces",
                upstream_id_target="v1.edges.list",
            ),
        ),
        SmokeTarget(
            "v1.monitoring.get_device_flows_totals",
            "v1.monitoring.get_device_flows_totals(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_device_flows_totals(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.monitoring.get_devices_totals",
            "v1.monitoring.get_devices_totals(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_devices_totals(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.monitoring.get_interfaces_latest",
            "v1.monitoring.get_interfaces_latest(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_interfaces_latest(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "v1.monitoring.get_paths_latest",
            "v1.monitoring.get_paths_latest(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_paths_latest(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "v1.monitoring.get_routes_latest",
            "v1.monitoring.get_routes_latest(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_routes_latest(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_first_id,
        ),
        SmokeTarget(
            "v1.monitoring.get_system_load",
            "v1.monitoring.get_system_load(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_system_load(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.monitoring.get_system_lte",
            "v1.monitoring.get_system_lte(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_system_lte(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.monitoring.get_system_memory",
            "v1.monitoring.get_system_memory(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_system_memory(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.monitoring.get_system_uptime",
            "v1.monitoring.get_system_uptime(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_system_uptime(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.monitoring.get_system_wifi",
            "v1.monitoring.get_system_wifi(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_system_wifi(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.monitoring.get_paths_links",
            "v1.monitoring.get_paths_links(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_paths_links(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.monitoring.get_paths_links_totals",
            "v1.monitoring.get_paths_links_totals(gateway_id)",
            lambda c, seed: c.v1.monitoring.get_paths_links_totals(seed),
            seed_from="gateways.list_prefer_up_for_monitoring",
            seed_extractor=extract_gateway_candidate_ids,
            exception_classifier=classify_optional_monitoring_exception,
            try_multiple_seeds=True,
        ),
        SmokeTarget(
            "v1.users.get_groups",
            "v1.users.get_groups(user_id)",
            lambda c, seed: c.v1.users.get_groups(seed),
            seed_from="users.list",
            seed_extractor=extract_first_id,
        ),
    ]


def build_named_seed(
    value: Any,
    *,
    source_target: str,
    upstream_id_target: str,
) -> dict[str, str] | None:
    interface_name = extract_first_name(value)
    if not interface_name:
        return None

    upstream_value = DEPENDENCY_VALUES.get(upstream_id_target)
    edge_id = extract_first_id(upstream_value)
    if not edge_id:
        return None

    return {"edge_id": edge_id, "interface_name": interface_name}


DEPENDENCY_VALUES: dict[str, Any] = {}
DEFAULT_GATEWAY_CANDIDATE_LIMIT = 3


def extract_gateway_candidate_ids(
    value: Any,
    *,
    limit: int = DEFAULT_GATEWAY_CANDIDATE_LIMIT,
) -> list[str]:
    if not isinstance(value, list):
        return []

    candidates: list[str] = []
    for item in value:
        item_id = getattr(item, "id", None)
        if not isinstance(item_id, str):
            continue
        gateway_id = item_id.strip()
        if not gateway_id or gateway_id in candidates:
            continue
        candidates.append(gateway_id)
        if len(candidates) >= limit:
            break
    return candidates


def run_target(
    client: SDWANClient,
    target: SmokeTarget,
    registry: dict[str, SmokeTarget],
    results: dict[str, SmokeResult],
) -> SmokeResult:
    cached = results.get(target.name)
    if cached is not None:
        return cached

    if target.skip_if is not None:
        skip_reason = target.skip_if()
        if skip_reason:
            result = SmokeResult("SKIP", skip_reason, attempted=False)
            results[target.name] = result
            return result

    seed = None
    if target.seed_from is not None:
        dependency = run_target(client, registry[target.seed_from], registry, results)
        if dependency.status == "FAIL":
            result = SmokeResult(
                "SKIP",
                f"dependency failed: {registry[target.seed_from].label}",
                attempted=False,
            )
            results[target.name] = result
            return result
        if dependency.status == "SKIP":
            result = SmokeResult(
                "SKIP",
                f"dependency unavailable: {registry[target.seed_from].label}",
                attempted=False,
            )
            results[target.name] = result
            return result

        extractor = target.seed_extractor or extract_first_id
        seed = extractor(dependency.value)
        if seed is None:
            result = SmokeResult(
                "SKIP",
                f"no seed available from {registry[target.seed_from].label}",
                attempted=False,
            )
            results[target.name] = result
            return result

    if target.try_multiple_seeds:
        result = run_target_with_multiple_seeds(client, target, seed)
    else:
        result = execute_target_call(client, target, seed)

    results[target.name] = result
    return result


def preferred_gateway_candidates(client: SDWANClient) -> Any:
    up_gateways = client.gateways.list(filter="status:up")
    if up_gateways:
        return up_gateways
    return client.gateways.list()


def execute_target_call(
    client: SDWANClient,
    target: SmokeTarget,
    seed: Any,
) -> SmokeResult:
    try:
        value = target.call(client, seed)
    except PermissionDeniedError as exc:
        return SmokeResult("SKIP", short_error(exc), attempted=True)
    except Exception as exc:
        if target.exception_classifier is not None:
            classified = target.exception_classifier(exc)
            if classified is not None:
                return classified
        return SmokeResult("FAIL", short_error(exc), attempted=True)

    DEPENDENCY_VALUES[target.name] = value
    return SmokeResult("PASS", summarize(value), attempted=True, value=value)


def run_target_with_multiple_seeds(
    client: SDWANClient,
    target: SmokeTarget,
    seeds: Any,
) -> SmokeResult:
    if not isinstance(seeds, list) or not seeds:
        return SmokeResult("SKIP", "no gateway candidates available", attempted=False)

    skip_reason: str | None = None
    attempted_candidates = 0

    for seed in seeds:
        attempted_candidates += 1
        result = execute_target_call(client, target, seed)
        if result.status == "PASS":
            return result
        if result.status == "FAIL":
            return result
        skip_reason = result.reason

    if skip_reason is None:
        skip_reason = "unsupported for this tenant/gateway/feature set"
    return SmokeResult(
        "SKIP",
        f"{skip_reason} after {attempted_candidates} gateway candidates",
        attempted=True,
    )


def print_connection(client: SDWANClient) -> None:
    print("Connection")
    print(f"  base_url: {client.resolved_base_url}")
    print(f"  metadata: {client.resolution_metadata}")
    print()


def print_result(label: str, result: SmokeResult) -> None:
    print(f"{result.status:<5} {label:<48} {result.reason}")


def main() -> None:
    base_url = env("NETSKOPESDWAN_BASE_URL")
    tenant_url = env("NETSKOPESDWAN_TENANT_URL")
    api_token = env("NETSKOPESDWAN_API_TOKEN")
    sdwan_tenant_name = env("NETSKOPESDWAN_SDWAN_TENANT_NAME")
    site_command_output_name = env("NETSKOPESDWAN_SITE_COMMAND_OUTPUT_NAME")

    if not api_token:
        raise SystemExit("Missing NETSKOPESDWAN_API_TOKEN")

    if not base_url and not tenant_url:
        raise SystemExit("Set NETSKOPESDWAN_BASE_URL or NETSKOPESDWAN_TENANT_URL")

    audit_from = env("NETSKOPESDWAN_AUDIT_FROM")
    audit_to = env("NETSKOPESDWAN_AUDIT_TO")
    if not audit_from or not audit_to:
        audit_from, audit_to = default_audit_range()

    client = SDWANClient(
        base_url=base_url,
        tenant_url=tenant_url,
        sdwan_tenant_name=sdwan_tenant_name,
        api_token=api_token,
    )

    print_connection(client)
    print(f"Audit window: {audit_from} -> {audit_to}")
    print()

    DEPENDENCY_VALUES.clear()
    targets = build_targets(
        audit_from=audit_from,
        audit_to=audit_to,
        site_command_output_name=site_command_output_name,
    )
    registry = {target.name: target for target in targets}
    results: dict[str, SmokeResult] = {}

    for target in targets:
        if not target.visible:
            continue
        result = run_target(client, target, registry, results)
        print_result(target.label, result)

    visible_target_names = {target.name for target in targets if target.visible}
    passed = sum(
        1
        for name, result in results.items()
        if name in visible_target_names and result.status == "PASS"
    )
    skipped = sum(
        1
        for name, result in results.items()
        if name in visible_target_names and result.status == "SKIP"
    )
    failed = sum(
        1
        for name, result in results.items()
        if name in visible_target_names and result.status == "FAIL"
    )

    print()
    print("Totals")
    print(f"  passed:  {passed}")
    print(f"  skipped: {skipped}")
    print(f"  failed:  {failed}")

    raise SystemExit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
