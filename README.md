# netskope-sdwan-py-sdk

`netskope-sdwan-py-sdk` is an API-first Python SDK scaffold for Netskope SD-WAN.

This first milestone focuses on:

- installable packaging
- `SDWANClient`
- centralized HTTP transport
- tenant and base URL normalization
- minimal gateway manager support
- lightweight tests with no live API dependency

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Usage

Direct API URL:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://customer.api.eu.infiot.net",
    api_token="TOKEN",
)

gateways = client.gateways.list()
```

Tenant URL with explicit SD-WAN tenant override:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    tenant_url="customer.de.goskope.com",
    sdwan_tenant_name="legacy123",
    api_token="TOKEN",
)
```

## Important Tenant Resolution Note

For goskope tenant URLs, the SDK can often determine the SD-WAN region, but it will not silently guess the final SD-WAN hostname when the SD-WAN tenant name may differ from the goskope tenant name.

Example:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://legacy123.api.eu.infiot.net",
    api_token="TOKEN",
)
```

Or, if you know the SD-WAN tenant name:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    tenant_url="customer.goskope.com",
    sdwan_tenant_name="legacy123",
    api_token="TOKEN",
)
```

## Current Scope

Implemented in this milestone:

- `client.gateways.list()`
- `client.gateways.get(gateway_id)`

Not implemented yet:

- other managers
- live DNS/CNAME discovery
- async support
- CLI or MCP integrations
