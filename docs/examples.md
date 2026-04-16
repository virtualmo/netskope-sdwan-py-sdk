# Examples

The repository includes a few small runnable examples that reflect the current SDK surface.

## List Gateways

```bash
python examples/basic_gateways.py
```

Shows:

- client initialization
- listing all gateways
- filtering online gateways with `filter="status:up"`
- friendly handling for invalid placeholder tenant URLs

## Gateway Telemetry Overview

```bash
python examples/basic_gateway_telemetry.py
```

Shows:

- selecting a gateway
- calling `client.gateways.get_telemetry_overview(...)`
- printing the raw telemetry payload

## Legacy v1 Monitoring

```bash
python examples/basic_monitoring.py
```

Shows:

- selecting a gateway, preferring active gateways
- using `client.v1.monitoring`
- running monitoring calls with a short UTC time window
- printing raw monitoring payloads

## Full Smoke Runner

```bash
python examples/smoke_all_gets.py
```

This script is meant for manual validation across the supported GET surface. It prints concise `PASS`, `SKIP`, and `FAIL` results and exits non-zero when an attempted endpoint fails.
