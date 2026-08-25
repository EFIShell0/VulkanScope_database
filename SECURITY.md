# Security and data policy

The public database contains technical Vulkan capability information only.

Do not publish IMEI, Android ID, device serial numbers, MAC addresses, user/account identifiers, private file paths, authentication tokens or IP addresses as report fields.

The site has no third-party JavaScript, analytics, remote fonts or advertising dependencies. Its Content Security Policy permits same-origin resources and the configured VulkanScope Worker API only.

Unknown, unsupported and unavailable capability states remain distinct. Missing query data is never inferred as unsupported without direct evidence.

## 0.33.8 submission hardening

The Worker accepts report submissions only as `application/json`. The outer schema must identify the producer as VulkanScope (`com.efishell.vulkanscope`) and `collection.status` must be `available`; incomplete collection submissions are rejected. Existing payload-size, forbidden-field, D1 parameter binding and no-request-IP-storage controls remain in force.

## 0.34.0 audit

No new network permission or third-party dependency was added. The UI-only transition and GPU-name styling changes retain the existing CSP, JSON submission validation, D1 parameterization, payload limits and no-IP-storage rules.

## 0.35.2 audit hardening

- POST media type is matched exactly as `application/json` (parameters such as `charset` are allowed); prefix lookalikes such as `application/jsonp` are rejected.
- Request bodies remain byte-bounded while streaming before JSON materialization.
- Sensitive personal/account/authentication field names are rejected recursively from parsed JSON. The validator deliberately operates on field names rather than scanning harmless technical report prose.
- Stored malformed JSON is converted to a generic JSON 500 response; stack details are not exposed.
- Report-list cursor parameters are validated and D1 queries remain parameter-bound.
- A composite `(submitted_at, id)` index supports stable report cursor pagination.

The submission endpoint intentionally remains unauthenticated so the VulkanScope Android application can submit reports without user accounts. Schema checks, size limits and Cloudflare deployment controls reduce abuse, but they are not a cryptographic proof that a caller is the official APK. Production operators should additionally use Cloudflare edge/rate-limiting controls appropriate to their deployment if public-write abuse becomes a concern; request IP addresses remain outside stored report data.

## Structured property/limit authority

For schema-v3 VulkanScope reports, `technicalReport.devices[].detailedProperties` and `technicalReport.devices[].limits` are separate authoritative datasets. Human-readable TXT normalization is a legacy compatibility fallback and must not cause DEVICE, Surface, feature or other metadata to be presented as a Vulkan property or limit. Existing stored payloads are interpreted on read; the correction does not mutate D1 rows.

## 0.38.0 routing, statistics and current-producer hardening

- Canonical public navigation is hash-based. Report routes accept only already-loaded lowercase 64-hex report IDs and allow-listed section names; compare routes require exactly two valid loaded IDs.
- Legacy query-string routes are accepted only for migration and are canonicalized to the validated hash representation.
- Distribution charts are rendered locally with first-party SVG/CSS. No chart CDN, remote script, analytics endpoint, remote font, ad service or chart-generation service is introduced.
- Statistics describe loaded submissions only and are not represented as market or global Vulkan ecosystem share.
- VulkanScope 0.41.4 current-producer validation is fail-closed for queue/video null-vs-zero semantics and for device-extension, extended-query and Vulkan 1.4 query status tokens.
- Static HTTP error pages use the current cache-busted local stylesheet and their local resource references are release-audited.
- The public write endpoint remains intentionally unauthenticated; deployment-level Cloudflare abuse/rate-limiting policy remains an operator control and must not store request IP addresses in report data.

## 0.39.0 filter/statistics integrity

- Filtering is client-side presentation only and does not modify canonical payloads, report hashes or D1 rows.
- Exact extension filters match only enumerated extension evidence; missing tokens are not inferred unsupported.
- Statistics slice actions assign only option values generated from already-normalized loaded reports.
- Donut labels and filter values continue through existing HTML escaping; route/report identifiers remain separately validated by the canonical router.
- No third-party chart JavaScript, analytics, remote font, ad or chart-generation endpoint was added.
- Worker request, CORS, bounded-body, privacy-key and prepared D1 protections are unchanged.
