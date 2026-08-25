# VulkanScope Database 0.39.1 Build / Contract Audit

## Release identity

- Database: `0.39.1`
- Current producer: VulkanScope `0.41.5` / versionCode `415`
- Compatible producer floor: VulkanScope `0.32.4+`
- Vulkan baseline: `1.4.360`
- Submission schema: `2`
- `technicalReport` schema: `3`
- Worker normalizer: `15`
- D1 migration: none

## 0.41.5 compatibility hardening

The 0.39.0 Worker applied strict query-diagnostic and queue/Vulkan Video semantic checks only to the exact `0.41.4` producer string. 0.39.1 makes that contract version-range aware: every schema-compatible VulkanScope producer at `0.41.4` or newer is subject to the same fail-closed evidence semantics.

- Non-available Vulkan Video query states require null numeric masks.
- A genuinely queried zero mask remains valid zero evidence.
- Device-extension, extended-query and Vulkan 1.4 query states remain allow-listed.
- VulkanScope 0.41.5/415 is the current producer identity.
- Historical supported producer versions remain accepted.
- Future compatible versions cannot bypass the 0.41.4+ semantic gate merely by changing the version string.

## Verification performed

- Frontend JavaScript syntax: PASS
- Worker JavaScript syntax: PASS
- Worker contract suite: PASS
- Canonical hash-route contract suite: PASS
- `tools/audit_database.py`: PASS
- JSON parsing and source hygiene: PASS
- Structural responsive smoke with current HTML/CSS at 360 px / 412 px / 1920 px: PASS

The 0.39.0 filter/statistics frontend behavior is retained; 0.39.1 changes producer metadata and Worker validation semantics rather than the filter engine. Stale unreferenced pre-0.39.0 JavaScript/CSS assets were removed from the release source package.
