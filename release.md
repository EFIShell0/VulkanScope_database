# VulkanScope Database 0.33.8

## GPU vendor identity polish

- Added the GPU vendor artwork already bundled with VulkanScope Android as local Database assets.
- Added a compact **Logo** column immediately beside report-backed GPU/device-name columns in Reports, Devices, Memory heaps/types, Queues, Surface formats/presentation queues and Portability tables.
- Vendor ID remains authoritative; GPU-name family matching is only a presentation fallback and unknown identities use the bundled unknown mark.
- Web copies are optimized 128x128 PNGs, loaded locally with lazy loading/async decoding.

## Third-party driver presentation

- Explicit **Turnip / third-party driver** labels now use a restrained VulkanScope red accent in report lists, report detail, overview values, compare values, custom select presentation and raw-report presentation.
- System Vulkan driver text and unrelated statuses are unchanged.
- Underlying driver strings are not rewritten.

## Security and correctness audit

- `/v1/reports` POST now requires `application/json` (HTTP 415 otherwise).
- Submission identity must match VulkanScope / `com.efishell.vulkanscope`.
- Incomplete collection submissions are rejected; only `collection.status=available` is accepted.
- Added a matching 415 error page.
- Tightened Permissions-Policy while preserving existing CSP/CORS, 2 MiB body limit, parameterized D1 SQL, SHA-256 report IDs and no request-IP persistence.
- Rechecked VulkanScope 0.32.5 structured-report compatibility and the validated Vulkan 1.4.360 baseline.
- Rechecked current Vulkan Hardware Database/CapsViewer category coverage; no new category-level gap was found beyond the presentation-queue detail already fixed in 0.33.7.

## Preserved behavior

- Supported / Unsupported / Available / Unavailable / Unknown remain distinct.
- Exact U64 masks and canonical/raw Vulkan values remain lossless.
- Missing report data is never inferred as Unsupported.
- Existing touch/mouse/keyboard table scrolling, custom filters, responsive navigation and report-detail animations remain intact.
