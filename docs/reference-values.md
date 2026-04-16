# Reference Values

This page collects enum-backed values from the uploaded OpenAPI files that show up in the current SDK GET surface.

## v1 monitoring WAN metrics

Used by `client.v1.monitoring.get_paths_links(...)`.

- `latency`
- `jitter`
- `rx_loss`
- `tx_loss`
- `rx_throughput`
- `tx_throughput`
- `rx_bytes`
- `tx_bytes`
- `rx_packets`
- `tx_packets`

## v1 edge roles

- `hub`
- `spoke`
- `dcedge`

## v1 edge models

- `iX100W`
- `iX101CW`
- `iXVirtual`
- `iX500W`
- `iX1000W`
- `iX3000`
- `iX1500W`
- `iX2000`
- `iX100CW`
- `iXCloud`
- `Client`
- `v500`
- `v600`
- `v700`
- `v800`
- `v5000`
- `v7000`
- `v1000`
- `v1500`
- `v2000`
- `v3000`

## v2 address group usage types

Used by the `usage_type` field in address-group and device-group GET responses.

- `device`
- `static`

## v2 address object types

Used by the `type` field in address object GET responses.

- `ipv4`
- `ipv6`
- `mac`

## v2 audit types

Used by audit event GET responses and by the SDK-level `audit_events.list(type=...)` filter helper.

- `AUDIT`
- `AUTHENTICATION`
- `CLIENT`
- `GATEWAY`
- `SYSTEM`

## v2 audit subtypes

Used by audit event GET responses and by the SDK-level `audit_events.list(subtype=...)` filter helper.

- `SYSTEM_ERROR`
- `SYSTEM_USER`
- `SYSTEM_GATEWAY`
- `SYSTEM_SSE_TUNNEL`
- `SYSTEM_IDP`
- `SYSTEM_CONTROL_PLANE`
- `SYSTEM_TENANT`
- `AUDIT_IAAS_ACCOUNT`
- `AUDIT_ROLE`
- `AUDIT_CONTROLLER`
- `AUDIT_TENANT`
- `AUDIT_SITE_COMMAND`
- `AUDIT_GATEWAY_TEMPLATE`
- `AUDIT_POLICY`
- `AUDIT_RTP`
- `AUDIT_TAG`
- `AUDIT_ADDRESS_GROUP`
- `AUDIT_NOTIFICATION_CHANNEL`
- `AUDIT_GATEWAY`
- `AUDIT_NETWORK_LOCATION`
- `AUDIT_SERVICE`
- `AUDIT_SITE_GROUP`
- `AUDIT_MONITOR`
- `AUDIT_CLIENT_TEMPLATE`
- `AUDIT_USER_GROUP`
- `AUDIT_CONTROLLER_OPERATOR`
- `AUDIT_APP_ACCESS_POLICY`
- `AUDIT_SIM`
- `AUDIT_CLIENT`
- `AUDIT_LINK_MONITOR`
- `AUDIT_SEGMENT`
- `AUDIT_CA_CERTIFICATE`
- `AUDIT_VPN_PEER`
- `AUDIT_REPORTING`
- `AUDIT_NTP_SERVER`
- `AUDIT_MANAGED_DEVICE`
- `AUDIT_CUSTOM_APP`
- `AUTHENTICATION_UNAUTHORIZED`
- `AUTHENTICATION_KEY`
- `AUTHENTICATION_USER`
- `CLIENT_SYSTEM`
- `GATEWAY_ERROR`
- `GATEWAY_UNDERLAY`
- `GATEWAY_OVERLAY`
- `GATEWAY_HA`
- `GATEWAY_CONFIG`
- `GATEWAY_SYSTEM`

## v2 other GET response enums

- `GatewayGroup.type`: `hub`, `spoke`
- `Policy.type`: `client`, `gateway`
- `User.controlled`: `manual`, `sso`, `x509`, `idp`
- `VpnPeer.type`: `IKEV2`, `GRE`
