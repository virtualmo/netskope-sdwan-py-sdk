# Getting Started

## Requirements

- Python 3.11 or newer

## Installation

Install the package:

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
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://your-sdwan-tenant.api.eu.infiot.net",
    api_token="TOKEN",
)

gateways = client.gateways.list()
for gateway in gateways:
    print(gateway.id, gateway.name)
```

## Environment-Based Configuration

You can also configure the client through environment variables:

```bash
export NETSKOPESDWAN_BASE_URL="https://your-sdwan-tenant.api.eu.infiot.net"
export NETSKOPESDWAN_API_TOKEN="TOKEN"
```

```python
from netskopesdwan import SDWANClient

client = SDWANClient()
print(client.gateways.list())
```

## Common Notes

- Placeholder hosts such as `https://customer.api.eu.infiot.net` are examples only
- `client.audit_events.list(...)` requires bounded `created_at_from` and `created_at_to` filters
- `client.site_commands.get_output(...)` returns a `DownloadResult`
