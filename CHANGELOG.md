# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - Unreleased

### Added

- Read-only Netskope SD-WAN SDK surface with v2-first managers and a separate `client.v1` legacy namespace for selected v1-only GET endpoints.
- Shared transport, shallow resource models, structured gateway model, and binary download support for site command output.
- Smoke example, tests, packaging metadata, release docs, and minimal CI for Python 3.11.

### Notes

- Functional scope remains GET-only.
- V1 support is transitional and intentionally isolated from the primary v2 client surface.
