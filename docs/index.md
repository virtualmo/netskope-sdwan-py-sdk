# netskope-sdwan-py-sdk

`netskope-sdwan-py-sdk` is an unofficial, read-only Python SDK for Netskope SD-WAN APIs.

It is designed for practical API access in scripts, diagnostics, and internal tooling:

- `GET` endpoints only
- v2-first client surface
- explicit `client.v1.*` namespace for legacy v1-only endpoints
- lightweight models with minimal transformation

The SDK stays intentionally close to the backend API so filters, IDs, and response payloads remain understandable when you move between code, examples, and API documentation.

## What It Covers

- Gateway operations through `client.gateways`
- Read-only v2 resources such as users, user groups, policies, segments, cloud accounts, software, and certificates
- Special GET helpers such as software downloads, site command output, and gateway telemetry overview
- Transitional v1 managers under `client.v1.edges`, `client.v1.monitoring`, and `client.v1.users`

## What It Does Not Cover

- `POST`, `PUT`, `PATCH`, or `DELETE`
- async client support
- code generation
- automatic DNS or CNAME discovery for tenant resolution

Start with [Getting Started](getting-started.md) for installation and a first request.
