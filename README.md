# VulkanScope Database 0.36.1

GitHub Pages frontend plus a Cloudflare Worker + D1 submission API for VulkanScope reports.

The production frontend is configured for `https://vulkanscope-database-api.vulkanscope.workers.dev` and the Worker CORS origin is `https://efishell0.github.io`. The D1 binding remains `DB`.


## 0.36.0 luminance typography parity

Database 0.36.0 matched OpenGLESScope luminance-unit typography: the numeric luminance value remains primary text while `cd/m²` is rendered as a muted, lighter-weight visual unit at 0.92em without changing the underlying evidence value.

## 0.35.9 Display & HDR / ABI / home parity

Database 0.35.9 aligns Display & HDR naming, supported-device ABI presentation, luminance units and home compatibility metrics with the established OpenGLESScope Database information hierarchy while preserving VulkanScope evidence semantics.

## 0.35.8 exact Properties / Limits semantics

VulkanScope Database 0.35.8 fixes a report-metric classification bug found while comparing VulkanScope 0.33.10 Turnip reports. Schema-v3 structured report arrays are now authoritative for report Properties and Limits presentation.

- **Properties** comes only from the selected device's `technicalReport.devices[].detailedProperties`. DEVICE metadata, Surface metadata, feature rows, formats, profiles and limits cannot inflate the Properties count.
- **Limits** comes only from `technicalReport.devices[].limits`. A detailed-property section whose name contains `Limits` or `Sparse Properties` is no longer reclassified as a limit.
- Report-detail tab counts now match the producer arrays directly. For the same structured payload, Database Properties count therefore matches VulkanScope's property-query-result count rather than the broader TXT-normalized capability count.
- Aggregate Properties and Limits views use their own authoritative per-report arrays and keep a missing entry in a loaded report as Unknown.
- TXT parsing remains the legacy compatibility fallback. Bracketed non-feature query-result rows feed fallback Properties; the literal `LIMITS` section feeds fallback Limits.
- Worker normalizer version is **11**. Existing D1 payloads are normalized on read; no migration or stored-report rewrite is required.
- Active frontend JavaScript is `app.v0358.js`; the unchanged 0.35.7 stylesheet remains cache-safe as `site.v0357.css`.

## 0.35.7 producer/database correctness and hardening

VulkanScope Database 0.35.7 is audited against VulkanScope 0.33.7 and the current published Khronos Vulkan 1.4.359 specification (2026-08-07), while retaining VulkanScope's separately pinned 1.4.360 producer/query staging baseline.

- Schema-v3 data is cross-checked against top-level GPU, driver, loader/device API and registry metadata before new submissions are accepted.
- Current report text must carry the expected VulkanScope application/version/package and core technical sections; arbitrary long JSON/text payloads are not accepted as valid reports.
- Browser API reads now have a 20-second timeout and 4 MiB response ceiling, with repeated cursor detection and four-way bounded detail fetching.
- Aggregate property/limit/feature coverage counts a missing field in an otherwise loaded report as Unknown instead of silently dropping that report from the denominator.
- Format coverage likewise exposes Unknown when a loaded report does not contain a format row.
- Display/HDR uses the producer's explicit `hdrCapabilityStatus` when present; a missing HDR field is Unknown, while an explicitly reported empty list is Unavailable.
- Display/HDR state filtering covers supported, unsupported, available, unavailable and unknown evidence without re-enabling irrelevant GPU/vendor/API filters.
- API responses add CORP/COOP and restrictive CSP headers in addition to existing CORS, nosniff, no-referrer and permissions policy protections.
- Worker normalizer version is 10. No D1 migration or stored-payload rewrite is required.


## 0.35.6 Vulkan brand-surface parity

The public database shell now uses the same chromatic dark-surface treatment as OpenGLESScope Database, translated to Vulkan’s official `#A41E22` red. Background glow, hero, primary navigation and detail tabs, filter controls, search focus, cards, table-scroll controls, pagination, repository/error actions and other interactive chrome use Vulkan-red-derived surfaces while capability-state colors remain semantic and unchanged.

## 0.35.5 Windows account-verifier reliability

The fail-closed Cloudflare account verifier now invokes the project-local Wrangler CLI directly through Node instead of relying on Windows `npx.cmd` child-process execution. JSON `whoami` remains preferred and a plain-text `whoami` fallback is accepted only when it contains the pinned VulkanScope account ID. Debug logging environment variables are removed from the child process so machine-readable verification cannot be polluted by Wrangler debug output. Wrong, unreadable or unverified accounts remain blocked.

## 0.35.4 Cloudflare account isolation

This release pins the production Worker to the VulkanScope Cloudflare account and D1 database, adds a project-local `vulkanscope` Wrangler auth-profile workflow, and blocks npm deploy/migration tasks when the active account does not match. Local credentials, Wrangler state, dependencies, logs, environment files, caches, and build artifacts are excluded by the root `.gitignore`.

## 0.35.3 coverage background dominance fix

Coverage rows now allow semantic background emphasis to extend beyond the progress fill only for the unique dominant percentage. Non-dominant coverage cells keep only their progress-bar fill in the state color; their surrounding coverage area is transparent and their percentage text remains neutral. State-count badges are unchanged.

## 0.35.2 full-audit hardening

- Added stable cursor pagination so the frontend is no longer limited to the newest 500 report index rows.
- Preserved Surface color-space/query diagnostics in TXT compatibility normalization.
- Corrected Compare memory flag rendering and empty HDR-type semantics.
- Hardened submission privacy validation to reject sensitive identifier keys recursively without scanning harmless report text.
- Hardened stored-payload parsing and kept generic Surface scalar values as availability data rather than support booleans.
- Worker normalizer version: 9.

## 0.35.1 coverage emphasis

Coverage percentage labels now use semantic color only for the unique dominant state in each compared distribution. Non-dominant percentage labels remain neutral white while their progress-bar fills retain their state colors; count badges are unchanged. Ties remain neutral.

## 0.35.0 audit notes

Database 0.35.0 fixes current-schema Compare field mapping, property/limit state normalization, TXT fallback queue/registry parsing, fallback memory-flag rendering, and Worker input hardening. Worker normalizer version is 8. The Android Display preferred wide-gamut field is an Android-reported preferred composition color space and is not presented as measured physical-panel gamut coverage.

The public Khronos specification version and VulkanScope's producer/query catalog baseline are intentionally separate labels. The database does not claim that its VulkanScope 1.4.360 producer/query baseline is the current published Khronos Registry version.

## Deploy the API

From `worker/`, run `npm install`, apply D1 migrations when needed, then run `npx wrangler deploy`.

The API validates schema and payload size, rejects personal-identifier classes, deduplicates reports by SHA-256, and does not persist the request IP address as a report field.

## Publish the frontend

Push the repository contents to GitHub. GitHub Pages uses the included Actions workflow. `config.js` points to the production Worker API and the Content Security Policy allows only that Worker origin in addition to same-origin resources.

## Submission semantics

Submission is explicit and user initiated from VulkanScope. There is no per-capability selection. The complete technical report plus structured device/GPU/driver/Vulkan metadata is submitted as one payload.

Supported, unsupported, unavailable and unknown are kept distinct. Runtime feature booleans and explicit SUPPORTED / NOT SUPPORTED report tokens are support evidence. Query failures and unavailable values are never converted to supported merely because the field exists. Enumerated extensions are supported; absence alone is not fabricated as unsupported.

The vendor UI keeps the raw Vulkan vendor ID visible while adding a readable vendor and GPU-family label, for example `Qualcomm / Adreno (0x5143)`.

## Reports view

The Reports view exposes exact submission timestamps down to seconds with timezone, GPU/device identity, driver mode and decoded/raw driver versions, physical-device API version, loader/instance API version, vendor/family/raw vendor ID, Vulkan device type, Android release/SDK/security patch, VulkanScope version/versionCode, application ABI and report ID. Reports can be ordered newest/oldest, ascending/descending by driver, API, GPU, vendor, Android version or application version. Pagination is capped at 50 reports per page.


## 0.33.6 compatibility
VulkanScope 0.32.6 schema-v3 `technicalReport` data is consumed losslessly when present. Memory type and heap masks are decoded to canonical Vulkan names while raw masks remain visible. The UI labels Vulkan-Headers 1.4.360 compilation separately from the validated Vulkan 1.4.360 query catalog.

## 0.33.6 UI and reliability notes

Overflowing technical tables use local design-consistent horizontal controls instead of browser-native scrollbar chrome while keeping direct touch panning and keyboard access. Filter listboxes animate in both directions and may open upward when needed. Long canonical Vulkan tokens wrap without truncation. Frontend load failures and the GitHub Pages 404 experience use the same VulkanScope visual language and link back to Reports and the official VulkanScope repository.




## 0.34.0 highlights

- Consistent bold GPU model emphasis across report-backed lists.
- Lightweight, reduced-motion-aware primary navigation transitions using compositor-friendly opacity/transform only.
- Re-audited CapsViewer category parity, canonical/raw Vulkan data handling, security and mobile sticky-tab behavior.

## 0.33.8 highlights

- Local GPU vendor artwork from the VulkanScope Android app is shown in a fixed-width **Logo** column beside report-backed GPU/device names.
- Explicit Turnip / third-party driver labels use a dedicated red accent without changing raw driver values.
- Worker submissions now require JSON, VulkanScope application identity and a complete/available collection state.
- VulkanScope 0.32.6 / Vulkan 1.4.360 structured-report compatibility and current CapsViewer/Vulkan Hardware Database category parity were re-audited.

## 0.33.7 interaction notes
Report-detail tabs and value-distribution accordions use symmetric, accessibility-aware transitions. Queue detail includes presentation support when reported, and Surface detail includes presentation queues/query diagnostics from schema-v3 submissions.



### 0.34.8
- Compact filter controls on desktop and mobile; custom listbox buttons/options now include local semantic SVG icons.
- Display/HDR adds a submission-order control for newest/oldest reports while keeping Vendor/GPU/Vulkan filters excluded.

### 0.34.7

- Uses the dedicated HDR10 artwork supplied for VulkanScope Database. HDR10 is no longer synthesized by cropping the HDR10+ logo.
- The HDR10 asset has an opaque white background so the original black wordmark remains legible on the dark UI.
- Browser-origin API requests are restricted to the configured VulkanScope Database origin when an Origin header is present; native Android submissions without an Origin header remain supported.
- Confirmed compatibility with VulkanScope 0.32.7; the SAF-only app change does not alter schema-v3 report semantics.

### 0.34.5
- Restored smooth compositor-only transitions between primary navigation sections.
- Fixed numeric Vulkan API-version ordering in filters, Devices and Versions.
- Re-audited VulkanScope 0.32.6 structured-report compatibility, CapsViewer category parity, security and performance.

- 0.34.5 also exposes schema-v3 Android Display/HDR data and nested layer extension lists that were previously retained but not fully surfaced in the UI.


### 0.35.0
- Compare and Portability controls/summary surfaces use a denser responsive layout while preserving all data and status semantics.
