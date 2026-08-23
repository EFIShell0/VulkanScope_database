# VulkanScope Database 0.36.5

VulkanScope Database 0.36.5 re-audits and hardens the complete-report contract for VulkanScope 0.35.1 / versionCode 352 while preserving schema 2 / technicalReport 3 and the existing D1 corpus.

## Changes

- Current producer/query baseline is VulkanScope 0.35.1 · Vulkan 1.4.360.
- Producer versions are parsed canonically and must be compatible VulkanScope 0.x releases at or above 0.32.4.
- VulkanScope 0.35.1 is bound to versionCode 352; mismatches are rejected fail-closed.
- Android security patch must use canonical YYYY-MM-DD form.
- Top-level application ABI and supported-device ABI evidence must exactly agree with technicalReport ABI evidence.
- Worker normalizer metadata is 13.
- Published Vulkan specification metadata remains Vulkan 1.4.360 dated 2026-08-14.
- Cloudflare Worker compatibility date is 2026-08-24.
- Compare technical filtering and all existing detailed Vulkan report destinations are preserved.
- No D1 migration, stored-report rewrite or submission-hash rewrite is required.


## 0.36.5 deployment correction

Cloudflare compatibility_date is 2026-08-23 so the Worker can deploy without API error 10021 during the audited deployment window. No schema or D1 migration change is required.
