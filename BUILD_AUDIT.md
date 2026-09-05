# VulkanScope Database 0.39.27 build / regression audit

## Release identity
- Database version: 0.39.27
- Immutable predecessor: VulkanScope Database 0.39.26
- Predecessor ZIP SHA-256: `e3fe56410d806e65ad09c4cf0595ba743e925f89f9525b89ad667284f266d99b`
- Predecessor census: 206 files
- Current producer/query baseline: VulkanScope 0.80.12 / versionCode 812 / Vulkan 1.4.362
- New-submission floor: VulkanScope 0.80.3
- Submission schema 2 / technicalReport 3 / normalizer 16

## Confirmed defect and correction
Database 0.39.26 selected the correct registry version but compared the submission registry-baseline fields against bare `1.4.362` / `1.4.361`. Real VulkanScope producers emit the locked catalog baseline including the `Vulkan ` prefix: 0.80.10+ emits `Vulkan 1.4.362`, while 0.80.3-0.80.9 emits `Vulkan 1.4.361`.

0.39.27 validates those exact producer strings and derives the existing header-provenance string from the same exact baseline. It does not rewrite, trim, normalize or accept the former unprefixed fixture spelling as an alias.

## Regression evidence
- Exact 0.39.27 registry-baseline verifier: PASS.
- Registry-baseline negative mutations plus harmless false-positive control: PASS.
- Retained 0.39.26 submission-diagnostics verifier and negative mutations: PASS.
- Worker contract: PASS; canonical 0.80.12/812 and 0.80.9/809 prefixed fixtures are accepted, unprefixed variants are rejected by the bounded registry-contract classes.
- Immutable 0.39.26 -> 0.39.27 source-overlay regression contract: PASS.
- Repository repair/state, UTF-8, registry lock, report-text identity, source audit/hygiene, route/Compare/Surface, producer metadata, loading/scroll, Encyclopedia, and Vulkan 1.4.362 retained gates: PASS.
- D1 migration-chain replay: PASS.
- Staged GitHub Pages artifact audit: PASS.

The aggregate single-process `tools/quality_gate.py` run reached and passed all gates through the 0.39.25 UI-coherence verifier before the execution environment time limit. The remaining 0.39.25 negative suite, 0.39.26 diagnostics, 0.39.27 targeted gates, Worker contract, D1 replay and Pages artifact audit were then executed separately and pass. The timed-out aggregate invocation itself is not labeled PASS.

## Non-regression boundary
No D1 migration, stored-report rewrite, report-hash rewrite, schema bump, normalizer bump, producer-floor change, Vulkan registry/Encyclopedia corpus change, Compare semantic change or privacy/resource-bound weakening is introduced.

Live Cloudflare Worker/Pages deployment and remote production D1 smoke testing are NOT EXECUTED in this packaging environment.
