# netskope-sdwan-py-sdk

`netskope-sdwan-py-sdk` is a read-only Python SDK for Netskope SD-WAN.

Current design:

- GET only
- v2-first client surface
- legacy v1 endpoints isolated under `client.v1.*`
- lightweight models by default

## Requirements

- Python 3.11+

## Install

```bash
git clone https://github.com/ns-melamin/netskope-sdwan-py-sdk.git
cd netskope-sdwan-py-sdk
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Run Tests

```bash
pytest -q
```

## Examples

```bash
python examples/basic_gateways.py
python examples/smoke_all_gets.py
```

## Basic v2 Usage

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://customer.api.eu.infiot.net",
    api_token="TOKEN",
)

gateways = client.gateways.list()
gateway = client.gateways.get("gw-001")
```

## Legacy v1 Usage

V2 is the primary surface. Transitional v1-only GET endpoints remain available under `client.v1`.

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
- `client.site_commands.get_output(...)` returns a `DownloadResult` with bytes and download headers.
- Gateways use a structured `Gateway` model. Most other JSON resources use shallow `ResourceRecord` wrappers with the original payload preserved in `.raw`.

## Tenant Resolution

Direct API URLs work as-is:

```python
client = SDWANClient(
    base_url="https://legacy123.api.eu.infiot.net",
    api_token="TOKEN",
)
```

Supported goskope tenant URLs can also be resolved when you provide the SD-WAN tenant name:

```python
client = SDWANClient(
    tenant_url="customer.de.goskope.com",
    sdwan_tenant_name="legacy123",
    api_token="TOKEN",
)
```

## Current Scope

Implemented:

- read-only v2 managers for gateways, infrastructure, policy, identity, software, controller, cloud, and certificate resources
- read-only helper methods for nested or special GETs such as address objects, controller operator status, JWKS, software downloads, and site command output
- transitional v1 managers under `client.v1.edges`, `client.v1.monitoring`, and `client.v1.users`

Not implemented:

- POST, PUT, PATCH, DELETE
- async support
- CLI or MCP integrations
- live DNS or CNAME discovery
