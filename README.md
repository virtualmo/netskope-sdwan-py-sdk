# netskope-sdwan-py-sdk

`netskope-sdwan-py-sdk` is an unofficial, read-only Python SDK for Netskope SD-WAN APIs. It is designed for scripts, diagnostics, and internal tooling that need predictable GET access to the API without hiding request details behind heavy abstractions.

## Overview

This SDK is intentionally narrow and practical:

- Read-only: only `GET` endpoints are implemented
- v2-first: primary resources live directly on `SDWANClient`
- Legacy v1 support: v1-only endpoints remain isolated under `client.v1.*`
- Lightweight models: gateways use a structured `Gateway` model, while most other resources return shallow `ResourceRecord` objects
- Close to the API: filters, IDs, and response shapes stay explicit

Python 3.11 or newer is required.

## Installation

Install from PyPI:

```bash
pip install netskope-sdwan-py-sdk
```

For local development:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

To build the documentation locally:

```bash
pip install -e ".[docs]"
mkdocs serve
```

## Quick Start

```python
from netskopesdwan import SDWANClient, __version__

print(__version__)

client = SDWANClient(
    base_url="https://your-sdwan-tenant.api.eu.infiot.net",
    api_token="TOKEN",
)

gateways = client.gateways.list()
for gateway in gateways:
    print(gateway.id, gateway.name)
```

You can also load configuration from environment variables:

```bash
export NETSKOPESDWAN_BASE_URL="https://your-sdwan-tenant.api.eu.infiot.net"
export NETSKOPESDWAN_API_TOKEN="TOKEN"
```

```python
from netskopesdwan import SDWANClient

client = SDWANClient()
print(client.gateways.list())
```

## Key Features

- Read-only SDK surface for supported Netskope SD-WAN GET endpoints
- Simple authentication with constructor arguments or environment variables
- Direct API base URL support, plus supported goskope tenant URL resolution
- Structured `Gateway` objects for high-value gateway endpoints
- Binary download support through `DownloadResult`
- Legacy v1 monitoring, edge, and user helpers under `client.v1`

## Basic Usage

List gateways and fetch one by ID:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://your-sdwan-tenant.api.eu.infiot.net",
    api_token="TOKEN",
)

gateways = client.gateways.list(filter="status:up")
gateway = client.gateways.get(gateways[0].id)
telemetry = client.gateways.get_telemetry_overview(gateway.id)

print(gateway)
print(telemetry)
```

Use legacy v1 endpoints when no practical v2 equivalent exists:

```python
from netskopesdwan import SDWANClient
from netskopesdwan.enums import V1MonitoringWANMetric

client = SDWANClient(
    base_url="https://your-sdwan-tenant.api.eu.infiot.net",
    api_token="TOKEN",
)

interfaces = client.v1.monitoring.get_interfaces_latest("gw-001")
paths = client.v1.monitoring.get_paths_links(
    "gw-001",
    start_datetime="2026-04-16T11:00:00Z",
    end_datetime="2026-04-16T12:00:00Z",
    metric=V1MonitoringWANMetric.LATENCY,
)
```

## Authentication And Tenant Resolution

The client accepts either:

- `base_url`: a direct Netskope SD-WAN API hostname such as `https://your-sdwan-tenant.api.eu.infiot.net`
- `tenant_url`: a supported `goskope.com` tenant URL, optionally with `sdwan_tenant_name` when the SD-WAN tenant name differs

Environment variables:

- `NETSKOPESDWAN_BASE_URL`
- `NETSKOPESDWAN_TENANT_URL`
- `NETSKOPESDWAN_API_TOKEN`
- `NETSKOPESDWAN_TIMEOUT`

Examples:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://legacy123.api.eu.infiot.net",
    api_token="TOKEN",
)
```

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    tenant_url="customer.de.goskope.com",
    sdwan_tenant_name="legacy123",
    api_token="TOKEN",
)
```

## Behavior Notes

- `client.audit_events.list(...)` requires both `created_at_from` and `created_at_to`
- `client.site_commands.get_output(...)` returns a `DownloadResult`
- Monitoring endpoints under `client.v1.monitoring` stay close to the raw API payloads
- Placeholder hosts such as `https://customer.api.eu.infiot.net` are examples only and must be replaced with a real tenant URL

## Examples

The repository includes runnable examples:

- `python examples/basic_gateways.py`
- `python examples/basic_gateway_telemetry.py`
- `python examples/basic_monitoring.py`
- `python examples/smoke_all_gets.py`

## Local Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest -q
```

Run lint:

```bash
ruff check .
```

Run the smoke example:

```bash
python examples/smoke_all_gets.py
```

## Scope

Implemented:

- read-only v2 managers for gateways, policy, identity, software, cloud, controller, and related resources
- selected nested or special GET helpers such as address objects, controller operator status, JWKS, software downloads, and site command output
- transitional v1 managers under `client.v1.edges`, `client.v1.monitoring`, and `client.v1.users`

Not implemented:

- `POST`, `PUT`, `PATCH`, `DELETE`
- async support
- automatic DNS or CNAME discovery

## Disclaimer

This project is unofficial and is not affiliated with, endorsed by, or supported by Netskope.

The SDK is provided on an "as-is" basis without warranties of any kind. Users are responsible for validating functionality and suitability for their own use cases.
