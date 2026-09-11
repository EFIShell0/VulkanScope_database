# VulkanScope Database 1.0.18 build / regression audit

## Release identity
- Version: 1.0.18
- Immutable predecessor: VulkanScope Database 1.0.17
- Predecessor ZIP SHA-256: `4279690b5c88d14747528b9a4e4d14eca695d3946743d9af66a5f51ada4264e2`
- Predecessor package census: 311 files
- Current frontend: `assets/app.v1018.js`
- Producer/query baseline: VulkanScope 1.0.19 · Vulkan 1.4.362
- Submission schema: 2
- technicalReport schema: 3
- Normalizer: 16

## 1.0.18 scope
This release fixes the bounded modal page-size selector, restores Android robot brand color, adds Devices circular report-distribution statistics plus an exact GPU report-count table, and replaces the stale historical Database audit implementation with a current source/artifact audit gate.

No D1 migration, stored-report rewrite, report-ID/hash rewrite, normalizer bump or capability/evidence semantic broadening is part of 1.0.18.

## Audit coverage
The release gate checks release/cache identity, canonical workflow parity, single-current frontend asset hygiene, local HTML resource integrity, Vulkan registry/header metadata, schema/normalizer locks, raw vendor-ID provenance, retained coverage/live-sync/modal semantics, CSP and Worker resource/security ceilings, pinned toolchain versions, Python/JavaScript syntax, route/compare/Worker contract tests, D1 migration replay and staged Pages allow-list boundaries.

The previous `tools/audit_database.py` implementation was discovered to be stale relative to the current 1.0.x source line. 1.0.18 replaces it with a release-current checker and makes both source and staged-artifact audit execution mandatory in the quality gate and GitHub workflow.

## External baseline review
- Vulkan registry/header baseline remains Vulkan 1.4.362 / header 362, publication date 2026-09-04.
- Android robot online brand green used by the Database is `#3DDC84`.
- Wrangler remains pinned to 4.130.0 and sharp remains overridden to 0.35.4; no dependency version change is required by this release.

## Evidence boundary
Successful local gates establish source-tree and deterministic-package evidence. They do not by themselves prove a live Cloudflare Pages/Worker deployment or remote D1 state; those remain separate operational checks.
