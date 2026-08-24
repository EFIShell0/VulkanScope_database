# VulkanScope Database 0.37.0 Build Audit

Date: 2026-08-24

- Database identity: 0.37.0.
- Current producer/query target: VulkanScope 0.41.0 / versionCode 410 / Vulkan 1.4.360.
- Published Khronos Vulkan metadata: Vulkan 1.4.360 (2026-08-14).
- Submission schema 2 / technicalReport schema 3 unchanged.
- Current producer fixture: HTTP 201.
- Current producer versionCode mismatch: HTTP 400.
- Below-floor/malformed producer: HTTP 400.
- Malformed security patch and ABI inconsistency: HTTP 400.
- Frontend JavaScript syntax: PASS.
- Worker JavaScript syntax: PASS.
- Worker contract suite: ALL PASS.
- Trend semantics: loaded submissions only; not market share.
- Permalink ids: lowercase 64-hex and loaded-report validated.
- Cloudflare compatibility date: 2026-08-23.
- Cloudflare observability: enabled with sampled logs/traces.
- D1 migration required: no.

Wrangler is pinned to 4.125.0 for this release.
- Database static audit: PASS.
- Frontend and Worker JavaScript syntax checks: PASS.
- Worker contract tests: ALL PASS.
- Wrangler pin: 4.125.0.
- No D1 schema migration or stored-report rewrite is required.
