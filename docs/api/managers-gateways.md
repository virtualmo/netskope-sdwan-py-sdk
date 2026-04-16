# Gateway Manager Module

The sections below summarize the GET methods backed by the uploaded v2 OpenAPI file.

Path parameter names follow the OpenAPI schema. In Python, these IDs are usually passed positionally, for example `client.gateways.get("gw-123")`.

`GatewayManager.get_telemetry_overview(...)` is intentionally not expanded here because it is currently exposed by the SDK but not described in the uploaded official OpenAPI files.

## gateways.list

Returns gateways.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression such as `status:up`

### Response notes
- top-level response includes `data` and `page_info`
- the SDK stores the last `page_info` value on `client.gateways.last_page_info`
- gateway objects include fields such as `id`, `name`, `is_activated`, `managed`, `overlay_id`, `created_at`, `modified_at`, and `device_config_raw`

## gateways.get

Returns one gateway by ID.

### Parameters
- `id`: required gateway ID

### Response notes
- gateway objects include fields such as `id`, `name`, `is_activated`, `managed`, `overlay_id`, `created_at`, `modified_at`, and `device_config_raw`

## gateways.get_localui_password

Returns the local UI password payload for a gateway.

### Parameters
- `id`: required gateway ID

### Response notes
- response is a top-level object
- key fields include `calculated` and `config`

## gateways.get_ssh_password

Returns the SSH password payload for a gateway.

### Parameters
- `id`: required gateway ID

### Response notes
- response is a top-level object
- key fields include `calculated` and `config`

::: netskopesdwan.managers.gateways
