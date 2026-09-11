# VulkanScope Database 1.0.17 build / regression audit

## Release identity
- Database version: 1.0.17
- Immutable predecessor: VulkanScope Database 1.0.16
- Producer/query baseline: VulkanScope 1.0.19 / Vulkan 1.4.362
- Submission schema 2 / technicalReport 3 / normalizer 16

## Mandatory release gates
- Repository overlay repair followed by canonical repository-state verification.
- Immutable 1.0.16 -> 1.0.17 source-overlay and strict-package regression verification.
- 1.0.17 high-coverage glow / Versions identity / paged evidence-modal verifier plus negative mutations.
- Worker contract including `databaseVersion: 1.0.17`, Vulkan registry lock, UTF-8 checks, D1 migration replay and Pages allow-list staging.
- Deterministic ZIP packaging with clean-extract strict regression verification.

## User-requested scope
- Repairs the global >=80% coverage glow/spray endpoint so every qualifying semantic coverage bar, including 100%, has a valid positioned endpoint and continuously visible halo.
- Versions keeps its Statistics donut and separate report-count table while adding Devices-parity bold GPU name, vendor logo and canonical vendor/family/raw-ID columns.
- Coverage Reports and Distinct/value modals use a shared vertical-scroll paged list with 10 / 25 / 50 per-page options, a hard 50-row visible-page cap, explicit range/page text and Previous/Next navigation.
- Existing live synchronization, new-database refresh notification, report-disclosure behavior and evidence semantics remain unchanged.

No D1 migration, stored payload rewrite, submission schema bump, normalizer bump or Vulkan registry change is introduced.
