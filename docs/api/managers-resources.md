# Resource Manager Module

The sections below cover the GET-backed resource manager methods that are described by the uploaded v2 OpenAPI file.

For most v2 list methods, the SDK mirrors the same query parameters as the API: `after`, `first`, `sort`, and `filter`. Path IDs are usually passed positionally in Python.

`audit_events.list(...)` is the one notable SDK-level wrapper: the OpenAPI only exposes `filter`, but the SDK requires `created_at_from` and `created_at_to` and composes the bounded filter for you.

## address_groups.list

Returns address groups.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `description`, `usage_type`, `metadata_tags`, `created_at`, and `modified_at`
- `usage_type` uses the `AddressGroupUsageType` enum values listed in [reference-values.md](../reference-values.md)

## address_groups.get

Returns one address group by ID.

### Parameters
- `id`: required address group ID

### Response notes
- key fields include `id`, `name`, `description`, `usage_type`, `metadata_tags`, `created_at`, and `modified_at`

## address_groups.list_address_objects

Returns address objects that belong to an address group.

### Parameters
- `group-id`: required address group ID
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `address`, `type`, `group_ids`, `site_id`, `segment_id`, and `tags`
- `type` uses the `AddressObjectType` enum values listed in [reference-values.md](../reference-values.md)

## audit_events.list

Returns audit event records within a bounded time range.

### Parameters
- `created_at_from`: required SDK argument that contributes the lower bound of the event-time filter
- `created_at_to`: required SDK argument that contributes the upper bound of the event-time filter
- `type`: optional SDK argument appended to the filter; values come from the audit type enum in [reference-values.md](../reference-values.md)
- `subtype`: optional SDK argument appended to the filter; values come from the audit subtype enum in [reference-values.md](../reference-values.md)
- `activity`: optional SDK argument appended to the filter; the spec also defines this as a large enum of event constants
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional raw filter expression merged with the bounded time range

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `event_time`, `type`, `subtype`, `activity`, `actor_nrn`, `target_nrn`, `note`, and `diff`

## applications.list_categories

Returns application categories.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, and `qosmos_id`

## applications.list_custom_apps

Returns custom applications.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `description`, `category_id`, `enabled`, `definitions`, `definitions_v2`, and `icon_url`

## applications.get_custom_app

Returns one custom application by ID.

### Parameters
- `id`: required custom app ID

### Response notes
- key fields include `id`, `name`, `description`, `category_id`, `enabled`, `definitions`, `definitions_v2`, and `icon_url`

## applications.list_qosmos_apps

Returns qosmos applications.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `category`, and `qosmos_id`

## applications.list_webroot_categories

Returns webroot categories.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `group`, and `nid`

## ca_certificates.list

Returns CA certificates.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `pem_encoded`, `client_auth_enabled`, `disabled`, `created_at`, and `modified_at`

## ca_certificates.get

Returns one CA certificate by ID.

### Parameters
- `id`: required CA certificate ID

### Response notes
- key fields include `id`, `name`, `pem_encoded`, `client_auth_enabled`, `disabled`, `created_at`, and `modified_at`

## client_templates.list

Returns client templates.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `enabled`, `dtls`, `dns_servers`, `dns_suffixes`, `allow_unmanaged`, and `assign_ip_from_template`

## client_templates.get

Returns one client template by ID.

### Parameters
- `id`: required client template ID

### Response notes
- key fields include `id`, `name`, `enabled`, `dtls`, `dns_servers`, `dns_suffixes`, `allow_unmanaged`, and `assign_ip_from_template`

## clients.list

Returns clients.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `template_id`, `labels`, `device_config_raw`, `created_at`, and `modified_at`

## clients.get

Returns one client by ID.

### Parameters
- `id`: required client ID

### Response notes
- key fields include `id`, `name`, `template_id`, `labels`, `device_config_raw`, `created_at`, and `modified_at`

## cloud_accounts.list

Returns cloud accounts.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `provider`, `config`, `created_at`, and `modified_at`

## cloud_accounts.get

Returns one cloud account by ID.

### Parameters
- `id`: required cloud account ID

### Response notes
- key fields include `id`, `name`, `provider`, `config`, `created_at`, and `modified_at`

## controller_operators.list

Returns controller operators.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `display_name`, `identity`, `default`, `nrn`, `public_ipv4`, `created_at`, and `modified_at`

## controller_operators.get

Returns one controller operator by ID.

### Parameters
- `id`: required controller operator ID

### Response notes
- key fields include `id`, `display_name`, `identity`, `default`, `nrn`, `public_ipv4`, `created_at`, and `modified_at`

## controllers.list

Returns controllers.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `operator_nrn`, `overlay_id`, `overlay_ip`, `public_ipv4`, `generation`, `created_at`, and `modified_at`

## controllers.get

Returns one controller by ID.

### Parameters
- `id`: required controller ID

### Response notes
- key fields include `id`, `operator_nrn`, `overlay_id`, `overlay_ip`, `public_ipv4`, `generation`, `created_at`, and `modified_at`

## controllers.get_operator_status

Returns controller operator status.

### Parameters
- `id`: required controller ID

### Response notes
- response is a top-level object
- key fields include `at`, `generation`, `can_delete`, and `error`

## device_groups.list

Returns device groups.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `description`, `usage_type`, `metadata_tags`, `latest_member_modified_at`, `created_at`, and `modified_at`

## device_groups.get

Returns one device group by ID.

### Parameters
- `id`: required device group ID

### Response notes
- key fields include `id`, `name`, `description`, `usage_type`, `metadata_tags`, `latest_member_modified_at`, `created_at`, and `modified_at`

## gateway_groups.list

Returns gateway groups.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `description`, `type`, `geo_ip_enabled`, `gateways`, `tenant_id`, `created_at`, and `modified_at`
- `type` values are `hub` and `spoke`

## gateway_groups.get

Returns one gateway group by ID.

### Parameters
- `id`: required gateway group ID

### Response notes
- key fields include `id`, `name`, `description`, `type`, `geo_ip_enabled`, `gateways`, `tenant_id`, `created_at`, and `modified_at`

## gateway_templates.list

Returns gateway templates.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `labels`, `device_config_raw`, `created_at`, and `modified_at`

## gateway_templates.get

Returns one gateway template by ID.

### Parameters
- `id`: required gateway template ID

### Response notes
- key fields include `id`, `name`, `labels`, `device_config_raw`, `created_at`, and `modified_at`

## inventory_devices.list

Returns inventory devices.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `serial_number`, `mac_address`, `hw_model`, `pub_key`, `site_id`, and `claimed`
- the SDK does not expose `inventory_devices.get(...)` because the official GET surface only includes the list endpoint

## jwks.get

Returns the controller JWKS document.

### Parameters
- none

### Response notes
- returns a standard JWKS object
- expect a top-level `keys` array

## ntp_configs.list

Returns NTP configurations.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `description`, `servers`, `is_default`, `created_at`, and `modified_at`

## ntp_configs.get

Returns one NTP configuration by ID.

### Parameters
- `id`: required NTP config ID

### Response notes
- key fields include `id`, `name`, `description`, `servers`, `is_default`, `created_at`, and `modified_at`

## overlay_tags.list

Returns overlay tags.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `description`, `config`, `enabled`, `system`, `tenant_id`, `created_at`, and `modified_at`

## overlay_tags.get

Returns one overlay tag by ID.

### Parameters
- `id`: required overlay tag ID

### Response notes
- key fields include `id`, `name`, `description`, `config`, `enabled`, `system`, `tenant_id`, `created_at`, and `modified_at`

## policies.list

Returns policies.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `type`, `disabled`, `policy_config_raw`, `destinations_config_raw`, `productivity_score_config_raw`, `created_at`, and `modified_at`
- `type` values are `client` and `gateway`

## policies.get

Returns one policy by ID.

### Parameters
- `id`: required policy ID

### Response notes
- key fields include `id`, `name`, `type`, `disabled`, `policy_config_raw`, `destinations_config_raw`, `productivity_score_config_raw`, `created_at`, and `modified_at`

## radius_servers.list

Returns RADIUS servers.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `ip`, `port`, `attributes`, `ip_bind_disabled`, `created_at`, and `modified_at`

## radius_servers.get

Returns one RADIUS server by ID.

### Parameters
- `id`: required RADIUS server ID

### Response notes
- key fields include `id`, `name`, `ip`, `port`, `attributes`, `ip_bind_disabled`, `created_at`, and `modified_at`

## segments.list

Returns segments.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `description`, `network_id`, `tenant_id`, `created_at`, and `modified_at`

## segments.get

Returns one segment by ID.

### Parameters
- `id`: required segment ID

### Response notes
- key fields include `id`, `name`, `description`, `network_id`, `tenant_id`, `created_at`, and `modified_at`

## site_commands.list

Returns site commands.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `site_id`, `note`, `spec`, `status`, `created_at`, and `modified_at`

## site_commands.get

Returns one site command by ID.

### Parameters
- `id`: required site command ID

### Response notes
- key fields include `id`, `site_id`, `note`, `spec`, `status`, `created_at`, and `modified_at`

## site_commands.get_output

Returns one site command output file as a binary download.

### Parameters
- `id`: required site command ID
- `name`: required file name within the command output set

### Response notes
- the API returns `application/octet-stream`
- the SDK wraps the response in `DownloadResult` with `content`, `content_type`, `content_disposition`, and `filename`

## software.list_downloads

Returns software download records.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `version`, `description`, `url`, `recommended`, `beta`, and `prod`

## software.list_versions

Returns software version records.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `version`, `channel`, `controller`, `customer_channels`, and `manifest_url`
- the SDK does not expose `software.get(...)` because the official GET surface only includes `/software-downloads` and `/software-versions`

## tenants.list

Returns tenants.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `description`, `domains`, `enabled`, `has_active_network`, `labels`, `parent_id`, `created_at`, and `modified_at`

## tenants.get

Returns one tenant by ID or `current`.

### Parameters
- `id`: required tenant ID or `current`

### Response notes
- key fields include `id`, `name`, `description`, `domains`, `enabled`, `has_active_network`, `labels`, `parent_id`, `created_at`, and `modified_at`

## user_groups.list

Returns user groups.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `template_id`, `auto_provision`, `enabled`, `created_at`, and `modified_at`

## user_groups.get

Returns one user group by ID.

### Parameters
- `id`: required user group ID

### Response notes
- key fields include `id`, `name`, `template_id`, `auto_provision`, `enabled`, `created_at`, and `modified_at`

## users.list

Returns users.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `email`, `enabled`, `controlled`, `groups`, `raw_role`, `created_at`, and `modified_at`
- `controlled` is an enum-backed field with values `manual`, `sso`, `x509`, and `idp`

## users.get

Returns one user by ID.

### Parameters
- `id`: required user ID

### Response notes
- key fields include `id`, `name`, `email`, `enabled`, `controlled`, `groups`, `raw_role`, `created_at`, and `modified_at`

## vpn_peers.list

Returns VPN peers.

### Parameters
- `after`: optional cursor for the next page
- `first`: optional maximum number of results
- `sort`: optional backend sort expression
- `filter`: optional backend filter expression

### Response notes
- top-level response includes `data` and `page_info`
- key item fields include `id`, `name`, `type`, `ip_address`, `ip_location`, `location`, `description`, `created_at`, and `modified_at`
- `type` values are `IKEV2` and `GRE`

## vpn_peers.get

Returns one VPN peer by ID.

### Parameters
- `id`: required VPN peer ID

### Response notes
- key fields include `id`, `name`, `type`, `ip_address`, `ip_location`, `location`, `description`, `created_at`, and `modified_at`

::: netskopesdwan.managers.resources
