# VulkanScope Database 0.35.0

GitHub Pages frontend plus a Cloudflare Worker + D1 submission API for VulkanScope reports.

The production frontend is configured for `https://vulkanscope-database-api.vulkanscope.workers.dev` and the Worker CORS origin is `https://efishell0.github.io`. The D1 binding remains `DB`.


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
