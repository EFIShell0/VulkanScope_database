# VulkanScope Database 0.39.0

## Filtering

- Reworked the Database into a view-scoped filtering model so hidden or irrelevant controls do not continue affecting unrelated pages.
- Added exact driver-version and enumerated device-extension cohort filters.
- Expanded applicable cohort filtering with GPU/device, API, Android/device-model, ABI, VulkanScope version and bounded submission-age dimensions.
- Added per-page row/value/coverage filters across Properties, Limits, Features, Formats, Memory, Queues, Surface, Extensions, Instance, Profiles and Compare.
- Added Device sorting/minimum-report filters and Device API / Loader API / paired modes to Versions.
- Added a unified Clear filters action for applicable global and active view-local filters; it now restores each view's default subgroup/sort as required by the project rules.

## Semantic corrections

- Properties and Limits now expose only Query available / Query unavailable / Unknown state filtering.
- Removed Supported/Unsupported aggregate columns from Properties and Limits because generic property/limit values are query evidence, not support booleans.
- Display/HDR deliberately excludes Vulkan GPU/vendor/API/driver/extension filters and uses only directly reported Android/display dimensions, including preferred wide-gamut color space and exact display mode. Its global search is restricted to device/display evidence.
- Queue generic state filtering is hidden until one concrete queue capability is selected; queue-family, presentation-state and Vulkan Video query-state filters are available independently.
- Surface generic state filtering is hidden on the unscoped All view and becomes subgroup-specific when a Surface category is selected.
- Corrected Format subgroup semantics so an explicitly reported zero feature mask remains direct zero-bit evidence instead of being dropped as missing; a selected format-feature bit now drives its own Supported/Unsupported/Unknown counts.
- Exact extension filtering means enumerated evidence only; missing extension tokens remain Unknown/not listed.

## Statistics

- Upgraded donut charts to keyboard-accessible, clickable local SVG/CSS distributions that apply the exact selected cohort filter, expose the active slice with `aria-pressed`, and toggle the same slice to clear that filter.
- Added distributions for GPU vendor, Device Vulkan API, Loader/instance API, GPU device type, driver mode, Android version, application ABI and VulkanScope producer version.
- Added configurable 5/8/12-slice chart detail with explicit Other grouping.
- Added extension-ranking device/instance/both scope, namespace, minimum enumeration-share and text filters.
- Extension membership remains a ranking instead of a pie chart because memberships overlap.
- All percentages are labeled filtered-submission share and are never presented as market share.

## Compatibility

- Current producer remains VulkanScope **0.41.4 / versionCode 414** with Vulkan **1.4.360**.
- Submission schema **2**, technicalReport schema **3**, Worker normalizer **15**, canonical report hashes and existing D1 data remain unchanged.
- No D1 migration, stored report rewrite, report-hash rewrite, Worker compatibility-date change or Wrangler upgrade is required.
