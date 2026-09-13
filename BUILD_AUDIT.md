# VulkanScope Database 1.2.11 build / regression audit

- Database/frontend/Worker release identity: **1.2.11**.
- Frontend identity: `assets/app.v1211.js`, browser gate `browser-compat.v1211.js`, cache key **1211**.
- Immutable predecessor: VulkanScope Database 1.2.10 ZIP SHA-256 `83daa53e1c4217079368a0c0bbcce6460be26cb4b0c49f69639731d2fca12a0d`.
- Scope: Compare narrow/mobile report-identity flow only. The prior 40 px normal-state cap could collide with wrapped GPU/vendor/driver identity text; the natural state now has adequate intrinsic vertical room and <=760 px identity rows stack in one column. Compact pinned Compare still collapses the identity line explicitly.
- No D1 schema/migration, report-payload/hash, normalizer, producer floor, browser floor, filter semantics, comparison evidence or routing changes.
- Mandatory gates: 1.2.11 focused verifier + negative mutations, immutable 1.2.10 regression contract, source/Pages audits, Worker transport test, D1 migration replay and deterministic strict-package build.
