# Authentication

## API Token

The SDK uses bearer token authentication. Provide the token directly:

```python
from netskopesdwan import SDWANClient

client = SDWANClient(
    base_url="https://your-sdwan-tenant.api.eu.infiot.net",
    api_token="TOKEN",
)
```

Or through the environment:

```bash
export NETSKOPESDWAN_API_TOKEN="TOKEN"
```

## Base URL

The simplest option is to pass a direct SD-WAN API host through `base_url`:

```python
client = SDWANClient(
    base_url="https://legacy123.api.eu.infiot.net",
    api_token="TOKEN",
)
```

You can also set:

```bash
export NETSKOPESDWAN_BASE_URL="https://legacy123.api.eu.infiot.net"
```

## Tenant URL Resolution

Supported `goskope.com` tenant URLs can be resolved when the SD-WAN tenant name is known:

```python
client = SDWANClient(
    tenant_url="customer.de.goskope.com",
    sdwan_tenant_name="legacy123",
    api_token="TOKEN",
)
```

Resolution remains intentionally conservative:

- direct `infiot.net` API URLs are preferred
- supported goskope suffix mapping is available
- automatic DNS and CNAME discovery are not implemented

## Optional Timeout

You can set a timeout directly:

```python
client = SDWANClient(
    base_url="https://legacy123.api.eu.infiot.net",
    api_token="TOKEN",
    timeout=30,
)
```

Or with:

```bash
export NETSKOPESDWAN_TIMEOUT="30"
```
