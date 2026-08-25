# VulkanScope Database 0.39.0

VulkanScope Database 0.39.0 is a filter, statistics and usability release for the VulkanScope 0.41.4 producer baseline. It retains compatibility with VulkanScope 0.32.4+ schema-2 / technicalReport-3 submissions.

## 0.39.0 highlights

- Rebuilt filtering as a **view-scoped filter matrix** so each page exposes only filters meaningful to that data class.
- Added cohort filters for exact driver version, exact enumerated device-extension token, device model, application ABI/version and bounded submission age where applicable.
- Added section-specific filters for Properties, Limits, Features, Formats, Memory, Queues, Surface/WSI, Extensions, Instance, Profiles and Compare.
- Corrected Format subgroup filtering so a reported zero `VkFormatFeatureFlags2` mask remains direct evidence of zero bits; selecting a required bit makes the aggregate counts describe that exact bit while unavailable masks remain Unknown.
- Removed meaningless generic support filtering from Properties/Limits and removed their aggregate Supported/Unsupported columns; these views now describe query availability plus reported values.
- Kept Display/HDR isolated from unrelated GPU vendor/model, Vulkan API, driver, extension and generic Vulkan capability-state filters.
- Added Device API / Loader API / paired distribution modes to Versions.
- Upgraded Statistics with interactive keyboard-accessible local SVG/CSS donut charts, exact slice-to-filter actions, visible active-slice state and click-again-to-clear behavior.
- Added Loader API, application ABI and VulkanScope producer-version donuts alongside vendor, Device API, device type, driver mode and Android distributions.
- Added configurable donut detail (5/8/12 slices) with explicit `Other` grouping while preserving total counts.
- Added extension ranking filters by namespace, minimum enumeration coverage and text search; extension membership remains a frequency table rather than an invalid overlapping pie chart.
- Added a single **Clear filters** action that restores applicable cohort and view-local defaults.
- Preserved canonical hash routes introduced in 0.38.0.

## Filter semantics

Filtering never changes stored reports or infers unsupported capabilities. Exact extension cohort filtering means the selected device extension was enumerated in a report; absence remains Unknown/not listed.

Properties and Limits use **Query available / Query unavailable / Unknown** semantics. Boolean `false`, numeric zero and empty masks remain reported values and are not converted into Unsupported unless the underlying field is explicitly a support boolean.

Display/HDR uses only directly relevant Android/display filters: Android version, device model, submission date/order, HDR availability/type, wide-gamut state, preferred wide-gamut color space, resolution, refresh rate and exact display mode.

Queue state filtering is enabled only after a concrete queue capability is selected. Surface state filtering is similarly scoped to a concrete Surface subgroup.

- Clear filters restores each active view to its default sorting/grouping as well as clearing applicable cohort and local filters.
- Display/HDR search is scoped to Android device/display evidence and does not match hidden GPU/driver/Vulkan fields.

## Statistics semantics

All charts use only successfully loaded reports that match the active filters. Percentages are explicitly **filtered-submission share** and are not Vulkan ecosystem, hardware, GPU, vendor, driver or market share.

Donuts are used only for mutually exclusive per-report dimensions. Extension membership overlaps, so extensions remain an enumeration-frequency ranking. High-cardinality distributions combine trailing categories into an explicit `Other` slice without truncating report data or changing totals.

Charts use first-party local SVG/CSS only. No third-party chart runtime, remote font, analytics, advertising or chart-generation service is loaded.

## Compatibility

- Published Vulkan specification: **1.4.360 (2026-08-14)**
- Current producer/query baseline: **VulkanScope 0.41.4 · Vulkan 1.4.360**
- Compatible producer floor: **VulkanScope 0.32.4+ · schema 2 / technicalReport 3**
- Submission schema: **2**
- technicalReport schema: **3**
- Worker normalizer: **15**

No D1 migration, stored-payload rewrite, report-hash rewrite or schema migration is required for 0.39.0.

## Deployment baseline

- Wrangler: **4.125.0**
- Worker compatibility date: **2026-08-23**

The compatibility date remains the last project deployment-verified date and is not advanced by this frontend-only filter/statistics release.
