# VulkanScope Database 0.33.3

GitHub Pages frontend plus a Cloudflare Worker + D1 submission API for VulkanScope reports.

The production frontend is configured for `https://vulkanscope-database-api.vulkanscope.workers.dev` and the Worker CORS origin is `https://efishell0.github.io`. The D1 binding remains `DB`.

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


## 0.33.3 compatibility
VulkanScope 0.32.2 schema-v3 `technicalReport` data is consumed losslessly when present. Memory type and heap masks are decoded to canonical Vulkan names while raw masks remain visible. The UI labels Vulkan-Headers 1.4.360 compilation separately from the validated 1.4.357 / VulkanCapsViewer 4.12 query catalog.
