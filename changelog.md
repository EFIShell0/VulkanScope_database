# VulkanScope Database 1.0.9

- Makes deploy-snapshot/live-Worker reconciliation atomic before the first visible database render, so a newly submitted report updates Reports, the report count and every statistics/coverage view from one committed dataset instead of appearing later as a sliding row.
- Keeps the live Worker authoritative while preserving complete deploy-time snapshot fallback when live synchronization is unavailable; incomplete live payload deltas never partially mutate visible state.
- Replaces the truncated Report ID cell with a copy control for the exact 64-character SHA-256 ID, and separates server-authoritative submission Date, Time and Time zone onto three lines.
- Gives coverage below 20% a patterned/angled progress-bar shape and below 5% a stronger very-low shape without changing exact percentage widths or semantic state colors.
- Raises the new-submission floor to VulkanScope 1.0.19 / versionCode 1019. VulkanScope 1.0.18 and every older producer are rejected for new POSTs; historical stored reports remain readable.
- Advances Database/cache identity to 1.0.9 / `assets/app.v1009.js` / key 1009. Schema 2, technicalReport 3, normalizer 16, Vulkan 1.4.362, D1 schema, report IDs/hashes, payload chunking and privacy/transport limits are unchanged. No migration or stored-report rewrite.

# VulkanScope Database 1.0.8

- Fixes GitHub tag-release failure on long-lived repositories containing historical tracked frontend assets that were never members of the immutable predecessor release ZIP.
- Restores the intended source-overlay / strict-package boundary: the tagged checkout is predecessor-hash verified in source-overlay mode, while strict-tree verification runs only against the deterministic clean release extract.
- Hardens `tools/package_release.py` to derive the exact package path set, exclude repository-history extras and local deployment state, clean-extract the ZIP, compare every packaged file byte-for-byte with the selected source, and strict-tree/source-audit the extract before publishing.
- Adds a regression state machine reproducing stale historical `assets/site.v*.css` and `assets/app.js` checkout files, proving they are tolerated as repository history but excluded from the release ZIP; injected package extras still fail closed.
- Advances release/cache identity to 1.0.8 / `assets/app.v1008.js` / key 1008 while preserving VulkanScope 1.0.15/1015, Vulkan 1.4.362, schema 2/technicalReport 3/normalizer 16, D1 schema, report hashes and preload behavior. No migration or stored-report rewrite.

# VulkanScope Database 1.0.7

- Fixes Windows-only Encyclopedia byte drift at the checkout layer with canonical LF `.gitattributes`; byte comparison remains strict and now diagnoses CRLF checkout drift explicitly.
- Fixes Worker predeploy `spawnSync npm.cmd EINVAL` by invoking npm's JavaScript CLI through the current Node executable instead of spawning the Windows command shim.
- Reuses an existing audited workspace lock and bootstraps one only when absent; exact Wrangler 4.130.0 and sharp 0.35.4 resolution/integrity checks still precede `npm audit --audit-level=high`.
- Makes Windows CI reproduce the real deployment path with setup-node v7 / Node 24, `npm install`, and `npm run security:audit`; the Linux build job also pins Node 24.
- Adds dedicated 1.0.7 verifier and negative-mutation coverage for LF checkout policy, direct `npm.cmd` regressions, lock-bootstrap behavior, and the Windows security-audit gate.
- Preserves VulkanScope 1.0.15/1015, Vulkan 1.4.362, schema 2/technicalReport 3/normalizer 16, D1 schema, report hashes and preload behavior. No migration or stored-report rewrite.

# VulkanScope Database 1.0.6

- Fixes Windows-only Encyclopedia regeneration drift by emitting deterministic UTF-8/LF bytes.
- Fixes GitHub Actions historical 1.0.2 producer verification by using retained `--skip-version` mode.
- Fixes Worker predeploy `npm audit` ENOLOCK by creating and validating an ignored audit lock before auditing.
- Pins the Wrangler/Miniflare sharp transitive to patched sharp 0.35.4 without `--force`.
- Adds a compatibility wrapper for the previously documented 1.0.5 stale-lock verifier command.
- Preserves VulkanScope 1.0.15/1015, Vulkan 1.4.362, schema 2/technicalReport 3/normalizer 16, D1 schema and report hashes. No migration.

# VulkanScope Database 1.0.5

- Fixes the 1.0.4 GitHub Actions failure caused by an old tracked-but-ignored `worker/package-lock.json` retaining Wrangler `^4.125.0` / resolved 4.125.0 while canonical source requires exact 4.130.0.
- Makes `repair_repository.py --apply` purge that optional legacy lock before CI/release verification so a long-lived repository overlay converges to the canonical source tree.
- Strengthens `verify_optional_npm_lock.py`: canonical `worker/package.json` must always pin Wrangler 4.130.0; an optional lock, when present outside the repaired checkout, must also resolve exactly 4.130.0 with integrity metadata.
- Adds a regression fixture that reproduces the stale tracked lock, proves pre-repair rejection and post-repair cleanup, plus dedicated 1.0.5 verifier/negative-mutation gates.
- Advances release/cache identity to 1.0.5 / `assets/app.v1005.js` / key 1005. VulkanScope 1.0.15 compatibility, preload behavior, schema 2 / technicalReport 3 / normalizer 16 and D1 storage are unchanged; no migration is required.

# VulkanScope Database 1.0.4

- Fixes Windows Node ESM path resolution in Compare/Surface regression tests by replacing URL pathname conversion with `fileURLToPath(import.meta.url)`, preventing doubled-drive paths such as `C:\C:\...`.
- Adds a mandatory `windows-latest` GitHub Actions gate that executes the path-sensitive Compare and Surface tests before the Linux Pages build/deploy can proceed.
- Updates the pinned Cloudflare Wrangler toolchain to 4.130.0 and makes high/critical `npm audit` findings a production deploy blocker; no `--force` downgrade path is used.
- Adds explicit npm `allowScripts` approvals for the reviewed `esbuild`, `sharp` and `workerd` toolchain installers instead of leaving install-script execution unreviewed.
- Makes GitHub Release publication automatic on `v*` tag pushes from the GitHub-hosted runner, so local `gh` installation is no longer required; reruns upload assets with `--clobber`.
- Adds deterministic strict-tree release packaging with fixed ZIP timestamps and a separate SHA-256 sidecar.
- Advances Database/cache identity to 1.0.4 / `assets/app.v1004.js` while retaining VulkanScope 1.0.15 / 1015 compatibility, preload behavior, schema 2 / technicalReport 3 / normalizer 16 and D1 storage unchanged. No migration or stored-report rewrite is required.

# VulkanScope Database 1.0.3

- Adds deploy-time same-origin report preloading: the Pages workflow builds a complete bounded snapshot from the paginated Worker index and compact reports, split into content-hashed JSON chunks, so normal visits no longer wait for a full per-report database refetch.
- Keeps the live Worker authoritative by refreshing the index asynchronously and fetching only report IDs missing from the deploy snapshot; missing/invalid snapshots fall back to the existing bounded live loader, and newer direct report/Compare routes can fetch only the requested reports first.
- Adds a fixed top reading-progress indicator that advances/reverses with page scroll position and hides when the document is not scrollable.
- Makes page up/down controls fade/translate smoothly with scroll activity while preserving top/middle/bottom eligibility and reduced-motion behavior.
- Adds semantic local inline SVG icons to the custom filter listboxes without changing the authoritative native select state or adding third-party dependencies.
- Advances current producer/query identity to VulkanScope 1.0.15 / versionCode 1015 / Vulkan 1.4.362 with exact fail-closed `1.0.P -> 1000 + P` validation.
- Records source evidence that VulkanScope 1.0.15 `technicalReportJson` and `databaseSubmissionJson` remain byte-equivalent to 1.0.2; schema 2 / technicalReport 3 / normalizer 16, D1 schema, stored report bytes/hashes and the 0.80.3 submission floor remain unchanged.
- Cache-busts the materially changed frontend to `assets/app.v1003.js` with release key 1003. No D1 migration or stored-report rewrite is required.

# VulkanScope Database 1.0.2

- Advanced the current producer/query identity to VulkanScope 1.0.2 / versionCode 1002 / Vulkan 1.4.362.
- Advanced the cache-busted Pages frontend to `assets/app.v1002.js`.
- Preserved VulkanScope 1.0.1/1001 and 1.0.0/1000 historical producer identities, the 0.80.3 submission floor, schema 2 / technicalReport 3, normalizer 16, Surface/Compare semantics and D1 storage.
- No D1 migration, stored-report rewrite, report-hash rewrite or normalizer bump.

# VulkanScope Database 1.0.1

- Corrects Surface evidence-state normalization so incomplete, unavailable, not-applicable and unknown Surface queries are never displayed as fabricated Unsupported presentation evidence.
- Makes Worker report-text Surface classification independent of whether `Query status=` appears before or after the Boolean availability line.
- Makes the Pages Surface detail view use the same query-aware state helpers as Compare/normalization.
- Advances current producer identity to VulkanScope 1.0.1 / versionCode 1001 while retaining VulkanScope 1.0.0 / 1000 and 0.80.x historical compatibility.
- Preserves schema 2 / technicalReport 3 / normalizer 16, Vulkan 1.4.362, the 0.80.3 submission floor, D1 schema and report hashes. No migration or stored-report rewrite is required.

# VulkanScope Database 1.0.0

- Advances Database release identity and current producer metadata to VulkanScope 1.0.0 / versionCode 1000 / Vulkan 1.4.362.
- Extends producer semantic-version parsing across the 1.0.0 major-version boundary without weakening the VulkanScope 0.80.3 new-submission floor.
- Preserves the exact 0.80.10+ `Vulkan 1.4.362` registry/header contract and fail-closed producer identity validation.
- Preserves schema 2 / technicalReport 3 / normalizer 16, D1 data, report hashes, payload chunking, privacy/security boundaries and the Vulkan 1.4.362 Encyclopedia corpus.
- No D1 migration or stored-report rewrite is required.

# VulkanScope Database 0.39.27

- Fixes HTTP 400 `[vulkan_1_4_362_registry_contract]` for real VulkanScope 0.80.12 reports by validating the exact producer-emitted `Vulkan 1.4.362` registry-baseline string instead of the incorrect bare `1.4.362` test-fixture spelling.
- Applies the same exact-string correction to accepted VulkanScope 0.80.3-0.80.9 reports, whose producer baseline is `Vulkan 1.4.361`.
- Replaces Worker acceptance fixtures with producer-realistic prefixed baselines and adds negative coverage proving unprefixed aliases are rejected rather than silently normalized.
- Retains VulkanScope 0.80.12 producer metadata, 0.80.3 submission floor, schema 2 / technicalReport 3 / normalizer 16, Vulkan 1.4.362 registry/Encyclopedia corpus, report hashes and D1 storage. No migration is required.

# VulkanScope Database 0.39.25

- Aligns the startup/loading surface with the existing VulkanScope Database panel, typography, border/radius and accent language while preserving accessible truthful loading progress.
- Redesigns the offline Vulkan Encyclopedia to use the same Database cards, badges, notices, search field and compact statistics language instead of a separate visual subsystem.
- Preserves Vulkan 1.4.362, the 842/6248/2461/476/50 Encyclopedia corpus, evidence semantics, two-character large-family search floor and 24-result bound.
- Preserves VulkanScope 0.80.10 producer/query baseline, 0.80.3 new-submission floor, schema 2 / technicalReport 3 / normalizer 16, D1 storage and report hashes.
- Adds an immutable 0.39.24 -> 0.39.25 regression contract and targeted UI-coherence negative-mutation coverage.

# VulkanScope Database 0.39.25

- Advances the current producer/query baseline to VulkanScope 0.80.10 / Vulkan 1.4.362 while keeping the new-submission floor at VulkanScope 0.80.3.
- Accepts VulkanScope 0.80.10 reports with the new Vulkan 1.4.362 registry/header identity while retaining 0.80.3-0.80.9 / Vulkan 1.4.361 compatibility.
- Regenerates the offline Encyclopedia to 842 commands, 6248 VK_* tokens, 2461 Vk* types, 476 extensions and 50 VkResult entries and updates visible Encyclopedia copy to 1.4.362.
- Preserves schema 2, technicalReport 3, normalizer 16, D1 storage, historical report hashes and read compatibility without a migration.

# VulkanScope Database 0.39.23

- Updates the current producer/query baseline to VulkanScope 0.80.9 / versionCode 809 with Vulkan 1.4.361.
- Raises the new-submission producer floor to VulkanScope 0.80.3; 0.80.2 and lower new submissions are rejected while historical stored reports remain readable.
- Adds a Database-native offline Vulkan Encyclopedia generated from the same locked Vulkan 1.4.361 registry and curated VulkanScope evidence/VkResult reference model as the application.
- Provides All, VkResult, Commands, VK_*, Types and Extensions search categories with the locked 842 / 6241 / 2457 / 474 / 50 census and bounded 24-result presentation.
- Preserves explicit registry-reference versus runtime-evidence separation, existing loading progress, global page scroll arrows, historical canonical device-type presentation, Compare semantics and report hashes.
- Cache-busts the Pages frontend to `assets/app.v03923.js` plus `assets/encyclopedia.v03923.js`.

# VulkanScope Database 0.39.22

- Updates the current producer/query baseline to VulkanScope 0.80.8 / versionCode 808 with Vulkan 1.4.361.
- Requires VulkanScope 0.80.1 or newer for new report submissions while keeping all existing historical stored reports readable.
- Adds a visible loading state from first paint and progressive report-index/report-body loading feedback.
- Adds boundary-aware global page up/down controls with keyboard and reduced-motion support.
- Canonicalizes historical friendly physical-device labels such as `Integrated GPU` to `VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU` at read/presentation time without rewriting stored payloads or report hashes.
- Cache-busts the Pages frontend to `assets/app.v03922.js`.
- Preserves schema 2, technicalReport 3, normalizer 16, Vulkan 1.4.361, D1 storage and the existing bounded/non-truncating transport model; no D1 migration is required.

# VulkanScope Database 0.39.20

- Advances current producer/query metadata to VulkanScope 0.41.45 / versionCode 455 with Vulkan 1.4.361.
- Cache-busts the Pages frontend to `assets/app.v03920.js` and advances Database version metadata to 0.39.20.
- Preserves schema 2, technicalReport 3, normalizer 16, Compare semantics, report hashes, D1 storage and all historical reports; no D1 migration is required.

# VulkanScope Database 0.39.19

- Advances current producer/query metadata to VulkanScope 0.41.44 / versionCode 454 with Vulkan 1.4.361.
- Cache-busts the Pages frontend to `assets/app.v03919.js` and advances Database version metadata to 0.39.19.
- Preserves schema 2, technicalReport 3, normalizer 16, Surface/Compare semantics, report hashes, D1 storage and all historical reports; no D1 migration is required.

# VulkanScope Database 0.39.18

- Advances current producer/query metadata to VulkanScope 0.41.43 / versionCode 453 with Vulkan 1.4.361.
- Cache-busts the Pages frontend to `assets/app.v03918.js` and advances Database version metadata to 0.39.18.
- Preserves Database 0.39.17 Surface query-state Compare semantics and 0.39.16 historical property/feature Compare compatibility unchanged.
- Preserves schema 2, technicalReport 3, normalizer 16, Worker validation, canonical report hashing, D1 payload/chunk storage, privacy/CORS controls and the 2 MiB transport limit.
- Adds failing-before-fix and negative-mutation coverage for stale producer/frontend metadata. No D1 migration, stored-report rewrite or report-hash rewrite is required.

# VulkanScope Database 0.39.17

- Preserves Surface `queryStatus` and `queryReason` through structured and TXT normalization so Compare can distinguish available, unavailable, incomplete, not-applicable and unknown evidence.
- Treats generic Surface capability/diagnostic scalar values with availability semantics; diagnostic `false` / `NO` values are no longer mislabeled as unsupported capabilities.
- Reports `presentationSupported=false` as Unsupported only when the owning Surface query completed as Available; failed, incomplete, not-applicable or unknown Surface probes retain their evidence state instead of fabricating negative support.
- Applies the same query-result rule to per-queue presentation support: `false` becomes Unsupported only after a successful queue-support query.
- Preserves VulkanScope Database 0.39.16 historical pre-0.41.40 property/feature Compare canonicalization and corrected `Visible fields` / `Visible differences` wording.
- Advances current producer metadata to VulkanScope 0.41.42 / versionCode 452 while preserving Vulkan 1.4.361, schema 2, technicalReport 3 and normalizer 16.
- Adds failing-before-fix, behavioral and negative-mutation tests for Surface evidence-state Compare semantics. No D1 migration, stored-report rewrite or report-hash rewrite is required.

# VulkanScope Database 0.39.16

- Canonicalizes pre-0.41.40 `VkPhysicalDevice*Properties* · field` boolean rows from the historical Features representation to the current detailed-property identity during Compare only.
- Preserves historical stored payloads, report hashes and raw report detail; real Feature structs and non-boolean historical evidence are not rewritten.
- Corrects the Compare summary metric so unfiltered union rows are labeled `Visible fields`; `Visible differences` is used only when Differences only is active.
- Advances current producer/query metadata to VulkanScope 0.41.41 / versionCode 451 while preserving Vulkan 1.4.361, schema 2, technicalReport 3 and normalizer 16.
- Adds failing-before-fix, behavioral and negative-mutation coverage for historical Compare compatibility.
- No D1 migration, stored-report rewrite or report-hash rewrite is required.

# VulkanScope Database 0.39.15

- Fixes regression-gate false positives when a release is overlaid onto the real long-lived Git repository containing historical source/audit/assets that were not shipped in the predecessor release ZIP.
- Adds explicit source-overlay and strict-release-package regression modes: predecessor-owned files remain hash-protected in both, while only strict-package mode rejects unrelated source-history files.
- Treats generated `data/index.json` as semantic generated state so `build_index.py` no longer invalidates the predecessor contract merely by regenerating metadata/report inventory.
- Adds an existing-repository fixture covering historical extras, stale app repair, generated-index regeneration, strict-package rejection and immutable predecessor mutation detection.
- Cache-busts the frontend to `app.v03915.js` for release identity only; Worker/D1/API behavior is unchanged from 0.39.13.
- Preserves VulkanScope 0.41.32 / Vulkan 1.4.361, schema 2 / technicalReport 3, normalizer 16, D1 payload chunking and the 2 MiB non-truncating transport limit without a new migration.

# VulkanScope Database 0.39.13

- Fixes the Windows Python quality-gate crash caused by implicit CP1252 decoding of UTF-8 repository assets.
- Makes every Python `Path.read_text` / `Path.write_text` operation in release tooling encoding-explicit and reads D1 migrations as UTF-8.
- Adds a permanent regression test that proves the real frontend asset fails CP1252, succeeds UTF-8, and the VulkanScope 0.41.32 compatibility verifier completes successfully.
- Runs the UTF-8 determinism test both directly in the Pages workflow and inside the aggregate quality gate.
- Cache-busts the frontend as `app.v03913.js` only to publish the 0.39.13 Database release identity; capability, normalization and API behavior are unchanged.
- Preserves VulkanScope 0.41.32 / Vulkan 1.4.361, schema 2 / technicalReport 3, normalizer 16, D1 chunk storage, 2 MiB transport, report hashes and existing stored data without a new migration.

# VulkanScope Database 0.39.12

- Adds verified VulkanScope 0.41.32 compatibility while preserving submission schema 2, technicalReport 3 and normalizer 16.
- Advances the canonical producer/query baseline to Vulkan 1.4.361 and locks the packaged `vk.xml` snapshot by SHA-256.
- Accepts and cross-checks the additive 0.41.24+ multi-device summary provenance fields that 0.39.11 incorrectly rejected as unexpected keys.
- Enforces authoritative 0.41.18+ complete-report markers and 0.41.24+ physical-device enumeration completeness before accepting current reports.
- Enforces the 0.41.32 registry-coverage contract, including `VkPhysicalDevicePrivateDataBaseHandleFeaturesNV`.
- Preserves the producer's 2 MiB non-truncating transport contract despite D1's 2,000,000-byte single-row value limit by adding atomic payload chunk storage for large canonical reports.
- Switches request-body decoding to bounded incremental strict UTF-8, avoiding a second full raw-byte buffer and rejecting malformed byte sequences.
- Adds a compact report-detail path used by the frontend to avoid duplicating normalized large arrays inside Worker memory; the legacy expanded detail response remains available.
- Adds negative/current/historical, large-payload reconstruction and concurrent-idempotency contract tests plus registry/producer/regression quality gates.
- Requires D1 migration `0003_payload_chunks.sql`; existing inline report rows require no rewrite.

# VulkanScope Database 0.39.11

- Fixed HTTP 400 rejection of complete VulkanScope 0.41.12 reports when the isolated Image Format Properties2 query group explicitly finishes as Unavailable or Not applicable before tuple evidence can be produced.
- Keeps the complete six-slot Image Format Properties2 tuple ledger mandatory whenever that query group is Available.
- Rejects contradictory unavailable-group reports that also contain tuple, successful property or aggregate diagnostic evidence.
- Adds bounded validation-class text to HTTP 400 schema rejections for deterministic producer/Worker diagnosis.
- Advances the current producer baseline to VulkanScope 0.41.13 / 423 while keeping VulkanScope 0.41.12 / 422 compatible with the corrected query-group contract.
- Preserves schema 2, technicalReport 3, normalizer 16, Vulkan 1.4.360, existing D1 records and the 0.39.10 canonical ASTC format-token fix; no migration is required.

# VulkanScope Database 0.39.10

- Fixed valid Vulkan Image Format Properties2 submissions being rejected when canonical `VK_FORMAT_ASTC_*` names contain the registry-defined lowercase `x` dimension separator.
- Advanced the current producer baseline to VulkanScope 0.41.12 / 422 while preserving schema 2, technicalReport 3, normalizer 16 and existing D1 data without migration.

# VulkanScope Database 0.39.9

- Corrected zero-mask, format-mask, Not applicable and Compare state semantics for VulkanScope 0.41.11.
- Advanced normalizer to 16 and current producer baseline to VulkanScope 0.41.11 / 421 without a D1 migration.

# VulkanScope Database 0.39.8

- Adds native support for VulkanScope 0.41.10's complete bounded Image Format Properties2 tuple-state ledger.
- Eliminates ambiguous current-producer `Not reported` holes for scheduled base, OPAQUE_FD and Android Hardware Buffer tuples by requiring exactly six canonical slots per scheduled format.
- `AVAILABLE` requires `VkResult=0` plus the matching successful full property payload; the ledger never replaces that full value.
- `UNSUPPORTED` remains exact `VK_ERROR_FORMAT_NOT_SUPPORTED` (-11); other non-zero results remain `UNAVAILABLE`.
- Missing external-memory prerequisites are represented explicitly as `NOT APPLICABLE` with null `VkResult` and an exact reason, never inferred Unsupported.
- Worker validation cross-checks tuple counts/states against the fixed query recipe and aggregate query diagnostics and rejects missing, duplicate, malformed or contradictory current-producer evidence.
- The complete tuple ledger remains excluded from Properties & Limits totals; Compare overlays only non-available states under the canonical tuple identity.
- Historical VulkanScope 0.41.9 separated outcomes and 0.41.8 embedded negative tuple evidence remain compatible.
- Current producer baseline is VulkanScope 0.41.10 / 420; schema 2, technicalReport 3, normalizer 15, Vulkan 1.4.360 and D1 storage remain unchanged.
### 0.39.25 CI hotfix
- GitHub Actions now repairs stale versioned frontend assets from long-lived/overlay-updated checkouts before the release source audit, preventing old `assets/app.v*.js` files from failing the build.
- Fixed the frontend JavaScript syntax step so both current assets execute inside one valid YAML multiline command block.
- Added exact stale-checkout regression coverage; Vulkan/report/Worker/Database semantics are unchanged.



## 0.39.26
- Preserves fail-closed report validation while making current 0.80.12 rejection classes precise; no submitted report contents are echoed in errors.
