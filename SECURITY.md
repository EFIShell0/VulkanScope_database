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
- VulkanScope 0.41.4+ producer validation is fail-closed for queue/video null-vs-zero semantics and for device-extension, extended-query and Vulkan 1.4 query status tokens; 0.41.5 cannot bypass these checks by using a newer compatible version string.
- Static HTTP error pages use the current cache-busted local stylesheet and their local resource references are release-audited.
- The public write endpoint remains intentionally unauthenticated; deployment-level Cloudflare abuse/rate-limiting policy remains an operator control and must not store request IP addresses in report data.

## 0.39.0 filter/statistics integrity

- Filtering is client-side presentation only and does not modify canonical payloads, report hashes or D1 rows.
- Exact extension filters match only enumerated extension evidence; missing tokens are not inferred unsupported.
- Statistics slice actions assign only option values generated from already-normalized loaded reports.
- Donut labels and filter values continue through existing HTML escaping; route/report identifiers remain separately validated by the canonical router.
- No third-party chart JavaScript, analytics, remote font, ad or chart-generation endpoint was added.
- Worker request, CORS, bounded-body, privacy-key and prepared D1 protections are unchanged.

## 0.39.12 VulkanScope 0.41.32 / resource hardening

- The current producer baseline is VulkanScope 0.41.32 and the packaged canonical registry snapshot is Vulkan 1.4.361. Current-producer summary provenance and complete-report markers are cross-checked rather than trusted independently.
- Request bodies remain capped at 2,097,152 bytes and are never truncated. Incremental `TextDecoder(..., { fatal: true })` processing bounds raw-body memory and rejects malformed UTF-8.
- D1's documented 2,000,000-byte single string/BLOB/row ceiling is below the producer transport ceiling. Migration `0003_payload_chunks.sql` therefore stores larger canonical payloads in bounded child rows while preserving one canonical SHA-256 report identity. D1 batch writes are transactional; partial parent/chunk commits are not accepted as a successful write.
- Compact detail reads avoid Worker-side creation of a second normalized representation of the complete technical report. Legacy expanded detail remains an explicit compatibility path.
- Request-scoped payloads are not stored in module-level mutable state. Reused Worker isolates therefore do not intentionally retain prior report objects.
- Concurrent identical submissions remain idempotent through canonical SHA-256 IDs, `INSERT OR IGNORE`, and `(report_id, chunk_index)` primary keys.
- The public write API remains intentionally unauthenticated. Cloudflare rate limiting / WAF remains an operator-level abuse control and must not be represented as application authentication.

## 0.39.13 Windows/locale deterministic release tooling

- Release verification no longer depends on the Windows active code page or Python's default locale encoding. Repository JSON, JavaScript and SQL inputs used by Python gates are decoded explicitly as UTF-8.
- The exact frontend byte stream that triggered CP1252 failure is retained as a regression fixture; a future implicit `Path.read_text()` / `Path.write_text()` call causes the quality gate to fail.
- This is a release-tooling hardening change only. Worker request validation, D1 storage, report identity, submission privacy controls, payload limits, CORS and public-write policy are unchanged from 0.39.12.


## 0.39.15 release-tree / repository-overlay separation

- Regression checks distinguish a long-lived source checkout from a distributable release tree. Historical source files that predate the packaged predecessor are not treated as newly introduced release content in source-overlay mode.
- Predecessor-owned paths remain SHA-256 protected. This tolerance cannot hide a modification to an immutable predecessor file.
- Release ZIP validation uses strict-package mode, where unexpected files remain fatal. Pages staging remains separately allow-listed and audited.
- Stale versioned frontend app JavaScript is removed only through the explicit repository-repair command; the quality gate checks but does not silently mutate the checkout.
- Generated `data/index.json` is semantic state, not a fixed release hash. Its schema/version/Vulkan producer metadata and structural types are validated after regeneration.
- No Worker runtime, D1, request-body, privacy, CORS, report-hash or authentication policy changes are made in this release.
