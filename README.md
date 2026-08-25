# VulkanScope Database 0.39.1

VulkanScope Database 0.39.1 is a producer-compatibility and validation-hardening release for VulkanScope 0.41.5. It preserves the complete 0.39.0 filter/statistics/hash-routing frontend and remains compatible with VulkanScope 0.32.4+ schema-2 / technicalReport-3 submissions.

## 0.39.1 highlights

- Current producer/query baseline: **VulkanScope 0.41.5 / versionCode 415 · Vulkan 1.4.360**.
- Fixed the 0.39.0 validator gap where strict query-diagnostic and queue/Vulkan Video semantics applied only to the exact string `0.41.4`.
- The strict 0.41.4 semantics now apply to every schema-compatible VulkanScope producer at **0.41.4 or newer**, including 0.41.5 and future 0.x producers.
- 0.41.5 must therefore preserve allow-listed device-extension/extended-query/Vulkan-1.4 states and the Vulkan Video null-vs-genuine-zero contract.
- Historical compatible submissions remain accepted; no D1 migration, report rewrite, schema migration or normalizer bump is introduced.
- Frontend filters, donut statistics, canonical hash routes and loaded-submission denominator semantics remain unchanged from 0.39.0.

## Canonical contract

- Database submission schema: 2.
- technicalReport schema: 3.
- Normalizer: 15.
- Compatible producer floor: VulkanScope 0.32.4+.
- Published/query baseline: Vulkan 1.4.360.
