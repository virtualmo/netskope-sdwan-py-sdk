# netskope-sdwan-py-sdk

`netskope-sdwan-py-sdk` is a read-only Python SDK for Netskope SD-WAN APIs.

It is designed as:

- GET only
- v2-first for the primary client surface
- explicit about legacy v1-only GET endpoints under `client.v1.*`
- lightweight in modeling, with a structured `Gateway` model and shallow records elsewhere

## Requirements

- Python 3.11+

## Installation

```bash
pip install netskope-sdwan-py-sdk
```

For local development:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Quick Start

```python
from netskopesdwan import SDWANClient, __version__

print(__version__)

client = SDWANClient(
    base_url="https://customer.api.eu.infiot.net",
    api_token="TOKEN",
)

gateways = client.gateways.list()
gateway = client.gateways.get("gw-001")
```

## Legacy v1 Namespace

V2 is the primary surface. Transitional v1-only GET endpoints remain isolated under `client.v1`.

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://customer.api.eu.infiot.net",
    api_token="TOKEN",
)

edges = client.v1.edges.list()
interfaces = client.v1.monitoring.get_interfaces_latest("gw-001")
groups = client.v1.users.get_groups("user-001")
```

## Behavior Notes

- `client.audit_events.list(...)` requires both `created_at_from` and `created_at_to`.
- `client.site_commands.get_output(...)` returns a `DownloadResult` with bytes and response headers.
- Gateways return a structured `Gateway` model. Most other JSON resources return shallow `ResourceRecord` objects with the original payload in `.raw`.

## Tenant Resolution

Direct API URLs work as-is:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://legacy123.api.eu.infiot.net",
    api_token="TOKEN",
)
```

Supported goskope tenant URLs can also be resolved when the SD-WAN tenant name is known:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    tenant_url="customer.de.goskope.com",
    sdwan_tenant_name="legacy123",
    api_token="TOKEN",
)
```

## Local Commands

Install dev dependencies:

```bash
pip install -e .[dev]
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

- read-only v2 managers for gateways, infrastructure, policy, identity, software, controller, cloud, and certificate resources
- selected nested or special GET helpers such as address objects, controller operator status, JWKS, software downloads, and site command output
- transitional v1 managers under `client.v1.edges`, `client.v1.monitoring`, and `client.v1.users`

Not implemented:

- POST, PUT, PATCH, DELETE
- async support
- CLI or MCP integrations
- live DNS or CNAME discovery
