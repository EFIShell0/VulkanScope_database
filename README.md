# VulkanScope Database 0.37.0

VulkanScope Database 0.37.0 is the matching Database release for VulkanScope 0.41.0 / versionCode 410.

## 0.37.0

- Current producer/query baseline: VulkanScope 0.41.0 · Vulkan 1.4.360.
- Compatible producer floor remains VulkanScope 0.32.4+ · schema 2 / technical report 3.
- Adds report and two-report Compare permalinks.
- Adds GPU, vendor, driver/version, Vulkan API and exact enumerated-extension submission trends.
- Trend percentages describe loaded VulkanScope submissions only and are explicitly not market share.
- Extension absence is never converted into Unsupported.
- Existing normalized Compare still spans properties, features, formats, memory, queues, Surface/WSI, Display/HDR, extensions, profiles and report metadata.
- Schema 2 / technicalReport 3, D1 payload storage and stable report hashes are unchanged.
- Cloudflare observability is enabled with sampled logs and traces.
- No D1 migration is required.

Production Worker compatibility date remains 2026-08-23, the last deployment-verified non-future date recorded by this project.

Wrangler is pinned to 4.125.0 for this release.
