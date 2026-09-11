# VulkanScope Database 1.0.16 build / regression audit

## Release identity
- Database version: 1.0.16
- Immutable predecessor: VulkanScope Database 1.0.15
- Producer/query baseline: VulkanScope 1.0.19 / Vulkan 1.4.362
- Submission schema 2 / technicalReport 3 / normalizer 16

## Mandatory release gates
- Repository overlay repair followed by canonical repository-state verification.
- Immutable 1.0.15 -> 1.0.16 source-overlay and strict-package regression verification.
- 1.0.16 live synchronization / modal-detail / Versions verifier plus negative mutations.
- Worker contract including `databaseVersion: 1.0.16`, Vulkan registry lock, UTF-8 checks, D1 migration replay and Pages allow-list staging.
- Deterministic ZIP packaging with clean-extract strict regression verification.

## User-requested scope
- Expanded Submitted/Vendor/Type disclosures fit full values while keeping the three-line control pinned left and table growth horizontal.
- Distinct/value drill-downs use the same right-arrow centered dark-backdrop modal as Coverage reports.
- Versions uses the Statistics donut language for GPU/version/report cohorts with a separate exact-count table and no coverage bars.
- Live reports synchronize every 10 seconds and on focus/visibility/online recovery; only missing payloads are fetched and the report map is swapped atomically.
- A newer API database version produces a centered update dialog with an explicit Refresh now action rather than silently replacing frontend code.

No D1 migration, stored payload rewrite, submission schema bump, normalizer bump or Vulkan registry change is introduced.
