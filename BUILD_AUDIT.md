# VulkanScope Database 1.0.3 build / regression audit

## Release identity
- Database version: 1.0.3
- Immutable predecessor: VulkanScope Database 1.0.2
- Predecessor ZIP SHA-256: `0ef8b84379cff75c1d4e4cccb0aa1a79fc8c678efc671118e0cf6d5ed56fff4c`
- Predecessor package census: 228 files
- Current producer/query baseline: VulkanScope 1.0.15 / versionCode 1015 / Vulkan 1.4.362
- Historical 1.0.x producers retained under exact fail-closed identity mapping
- New-submission floor: VulkanScope 0.80.3
- Submission schema 2 / technicalReport 3 / normalizer 16
- D1 migration: none

## Release scope
Database 1.0.3 replaces the repeated browser-side full-database startup fetch with a deploy-time same-origin preload snapshot plus asynchronous live delta refresh. The snapshot builder consumes the complete paginated Worker index, fetches compact reports with bounded concurrency, writes content-hashed JSON chunks below the frontend 4 MiB response ceiling, and publishes a manifest under `data/preload/`. The browser prefers a complete snapshot, falls back to the bounded live loader when the snapshot is absent/invalid, and can fetch only route-requested reports before applying newer report/Compare permalinks.

The page-scroll controls preserve top/middle/bottom eligibility but use opacity/transform/visibility transitions instead of abrupt hidden/display swaps. A fixed 3 px reading-progress indicator follows the real scroll fraction in both directions and disappears when the document has no scroll range. `prefers-reduced-motion` removes decorative motion without removing navigation behavior.

Custom filter listboxes retain native `<select>` elements as authoritative state and add local inline SVG concepts for vendor/GPU, API/loader, driver, extension, device type, Android/device, ABI, VulkanScope version, date, HDR/gamut, resolution, refresh and display-mode filters. No third-party JavaScript, fonts, analytics or icon network dependency is introduced.

VulkanScope 1.0.15 compatibility is source-evidenced in `compat/vulkanscope-1.0.15-database-contract.json`: `technicalReportJson` and `databaseSubmissionJson` remain byte-equivalent to VulkanScope 1.0.2. The application-side validated-network guard does not alter the Database payload contract. Worker identity validation maps `1.0.P` exactly to versionCode `1000 + P`; 1.0.15/1015 is accepted and 1.0.15/1014 is rejected.

No D1 migration, stored-report rewrite, report-ID/hash rewrite, normalizer bump or evidence-state semantic broadening is introduced.

## Executed evidence
- immutable 1.0.2 -> 1.0.3 source-overlay regression contract: PASS;
- repository repair/check, source audit and audit-hygiene regression suite: PASS;
- deterministic UTF-8 tooling, optional-lock policy, Vulkan registry lock and report-text identity: PASS;
- hash routes, Compare, historical Compare and Surface Compare contracts plus negative mutations: PASS;
- retained 0.41.46 producer baseline and negative mutations: PASS;
- retained 0.80.8 loading/scroll/floor/device-type gates and negative mutations: PASS;
- retained 0.80.9 floor/Encyclopedia gates, state machine and negative mutations: PASS;
- retained Vulkan 1.4.362, UI coherence, submission diagnostics and exact registry-prefix gates plus negative mutations: PASS;
- retained 1.0.0 producer verifier and 1.0.1 full Surface-evidence verifier/model/negative suite: PASS;
- retained 1.0.2 producer verifier, identity model and negative suite: PASS;
- 1.0.3 preload/UI/compatibility verifier and paginated preload-builder fixture: PASS;
- frontend/Encyclopedia/Worker JavaScript syntax checks: PASS;
- complete Worker contract, including 1.0.15/1015 acceptance and 1.0.15/1014 rejection: PASS;
- in-memory D1 migration-chain replay: PASS; no new migration is present;
- staged Pages artifact build and strict artifact audit: PASS.

The aggregate `tools/quality_gate.py` is not labelled as a one-command PASS because this execution environment terminates the long combined process at its command-time ceiling. The same mandatory constituents were executed explicitly in order and pass.

## Packaging evidence
- strict release-tree verification against immutable 1.0.2: PASS;
- two independently generated deterministic ZIPs: byte-identical PASS;
- clean extract package census: 235 files;
- source/extract SHA-256 manifest equality for every packaged file: PASS;
- extracted-package strict regression verification and source audit: PASS;
- extracted-package 1.0.3 UI/preload compatibility verifier and preload-builder fixture: PASS;
- extracted-package Worker contract: PASS;
- extracted-package in-memory D1 migration replay: PASS;
- extracted-package staged Pages artifact build/audit: PASS.

The final ZIP digest is emitted as a separate `.sha256` sidecar so the archive does not contain a self-referential package hash. The independently generated reproduction ZIP is not included inside the release package.

## Runtime evidence boundary
Live Cloudflare Pages/Worker deployment and remote production D1 smoke testing are **NOT EXECUTED** in this packaging environment. No live deployment status is promoted to PASS.
