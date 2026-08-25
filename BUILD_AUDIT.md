# VulkanScope Database 0.39.0 Build / Contract Audit

- Database version: 0.39.0
- Current producer: VulkanScope 0.41.4 / versionCode 414
- Vulkan baseline: 1.4.360
- Submission schema: 2
- technicalReport schema: 3
- Worker normalizer: 15
- Worker compatibility date: 2026-08-23
- Wrangler: 4.125.0

Release verification covers frontend JavaScript syntax, canonical hash-route tests, Worker contract tests, JSON/HTML resource integrity, filter-matrix semantics, Display/HDR isolation, Properties/Limits query-state semantics, local Statistics dependencies and package hygiene. Headless Chromium interaction tests additionally cover advanced queue/display/statistics filters, Clear-filters default grouping/sorting, 64-bit/zero-mask format semantics, and 360/412/1920 px responsive overflow/navigation behavior.

No Worker semantic change, normalizer bump, D1 migration or stored-report rewrite is introduced by 0.39.0.
