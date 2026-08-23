# VulkanScope Database 0.36.5 Build Audit

Date: 2026-08-24

## Release gates

- Database identity: 0.36.5.
- Current producer/query target: VulkanScope 0.35.1 / versionCode 352 / Vulkan 1.4.360.
- Published Khronos Vulkan metadata: Vulkan 1.4.360 (2026-08-14).
- Submission schema 2 / technicalReport schema 3 unchanged.
- Current producer submission: accepted (HTTP 201).
- Current producer versionCode mismatch: rejected (HTTP 400).
- Malformed or below-floor producer version: rejected (HTTP 400).
- Malformed Android security patch: rejected (HTTP 400).
- Top-level/technicalReport ABI disagreement: rejected (HTTP 400).
- Historical compatible producer behavior retained.
- Static audit, frontend syntax, Worker syntax and Worker contract suite: PASS after final packaging validation.
- Cloudflare Worker compatibility date: 2026-08-24.
- D1 migration required: no.

The release tightens complete-report identity/provenance validation without modifying existing stored payloads or hashes.

- Cloudflare compatibility date deployability: 2026-08-23, non-future for observed API window.
