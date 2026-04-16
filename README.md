# netskope-sdwan-py-sdk

`netskope-sdwan-py-sdk` is a read-only Python SDK for Netskope SD-WAN APIs.

> ⚠️ Unofficial SDK – community maintained


## Design Principles

This SDK is intentionally opinionated and focused. It is designed as:

- **GET-only (initial phase)**  
  The SDK currently provides read-only access to the Netskope SD-WAN APIs.  
  This is a deliberate first stage to establish a stable, predictable foundation before introducing mutation operations (POST, PUT, PATCH, DELETE).

- **v2-first client surface**  
  All primary functionality is built around the Netskope SD-WAN v2 API.  
  New features and coverage are added to v2 managers first, making it the default and recommended interface.

- **Explicit handling of legacy v1 endpoints**  
  Endpoints that only exist in Netskope SD-WAN v1 are clearly separated under `client.v1.*`.  
  This avoids ambiguity, keeps the main client clean, and makes it obvious when legacy APIs are being used.

- **Lightweight and pragmatic data modeling**  
  The SDK avoids heavy abstractions and complex object hierarchies.  
  A structured `Gateway` model is provided for high-value resources, while most other endpoints return shallow `ResourceRecord` objects with direct access to the raw API payload.

- **Close-to-API behavior**  
  The SDK mirrors the API closely, with minimal transformation or hidden logic.  
  This makes it easier to reason about requests, debug issues, and map directly to API documentation.

- **Explicit over implicit**  
  Parameters, filters, and required fields are intentionally not hidden behind convenience layers.  
  The goal is to make API interactions transparent rather than “magic”.

- **Composable and script-friendly**  
  Designed for engineers automating workflows, building tooling, or running diagnostics — not as a full abstraction layer.

- **Small surface area, easy to extend**  
  The codebase is structured to allow incremental addition of new endpoints without introducing breaking changes or unnecessary complexity.

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
pip install -e ".[dev]"
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
- live DNS or CNAME discovery


## Disclaimer

This project is an unofficial SDK and is not affiliated with, endorsed by, or supported by Netskope.

The SDK is provided on an "as-is" basis without warranties of any kind, express or implied.  
Users are responsible for validating functionality and suitability for their own use cases.