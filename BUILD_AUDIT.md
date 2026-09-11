# VulkanScope Database 1.0.13 build / regression audit

## Identity
- Database version: 1.0.13
- Immutable predecessor: VulkanScope Database 1.0.12
- Predecessor ZIP SHA-256: `5584a3bf4ae4103b23ce7100915b51abb6d7b307ada5b52599fca41cf50a4078`
- Current producer/query baseline: VulkanScope 1.0.19 / versionCode 1019 / Vulkan 1.4.362
- Submission schema 2 / technicalReport 3 / normalizer 16
- D1 migration: none

## Scope
This release repairs Reports Submitted disclosure geometry/animation and replaces the >=80% white shine with semantic state-colored endpoint spray/pulse presentation. It does not change normalized report semantics, Worker validation, D1 storage, report IDs/hashes, preload/live reconciliation, privacy/security boundaries or transport limits.

## Mandatory verification
- 1.0.13 disclosure/spray verifier and negative mutations.
- Immutable 1.0.12 -> 1.0.13 source-overlay and strict-package regression verification.
- Worker contract and JavaScript syntax.
- D1 migration-chain replay.
- Pages allow-list staging.
- Deterministic ZIP and clean-extract byte equality.

Live Cloudflare deployment and production D1/browser smoke testing are not claimed by the packaging environment.
