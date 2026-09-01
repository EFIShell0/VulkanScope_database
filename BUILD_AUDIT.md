# VulkanScope Database 0.39.16 Build / Release Audit

Immutable predecessor: VulkanScope Database 0.39.15 ZIP SHA-256 `bdf533c45c84644f66ee29d2fccd3151b2990adb7622031c688a33904a609831`. Current producer/query baseline: VulkanScope 0.41.41 / versionCode 451; Vulkan registry 1.4.361; schema 2 / technicalReport 3; normalizer 16.

The supplied cross-version comparison demonstrates that pre-0.41.40 property-struct `VkBool32` fields stored in the historical Features dataset appear one-sided against 0.41.40+ correctly classified detailed properties. 0.39.16 adds presentation-only historical identity mapping for the exact `VkPhysicalDevice*Properties* · field` boolean pattern and changes no stored payload or report hash.

The Compare summary now labels the visible union as `Visible fields` when Differences only is disabled and `Visible differences` only when the difference filter is enabled. Historical real Features and non-boolean evidence are false-positive controls and are not remapped.

Failing-before-fix was demonstrated by `tools/test_compare_04141_compat.mjs` against immutable 0.39.15. Successor and negative-mutation gates are mandatory. No D1 migration is introduced. Production Cloudflare deployment remains a separate evidence class and is NOT EXECUTED by local source tests.

# VulkanScope Database 0.39.15 Build / Release Audit

Immutable predecessor: VulkanScope Database 0.39.14 ZIP SHA-256 `8405bef9cbe6fc1e2f1c3c5836f3c5c5f3cf612d1afc53313869b204af755777`. Current producer audited: VulkanScope 0.41.40 / versionCode 450; Vulkan registry 1.4.361; schema 2 / technicalReport 3; normalizer 16.

Demonstrated defect: Database 0.39.14 requires the historical `Loader / instance API` TXT line although VulkanScope 0.41.24+ emits separate `Loader API` and `Base probe instance API` lines. This causes a valid current complete report to fail the Worker `report_text` contract with HTTP 400. 0.39.15 uses producer-version-aware identity validation, preserves historical merged-line acceptance, and requires the split form for current producers. No D1 migration or payload rewrite is introduced.

Failing-before-fix, Worker contract, regression, source/artifact and package evidence are recorded by executable gates. Production Cloudflare deployment is a separate evidence class and is not implied by local tests.

# VulkanScope Database 0.39.15 Build / Release Audit

- Database release: 0.39.15.
- Immutable predecessor: 0.39.13.
- Producer/query baseline: VulkanScope 0.41.32 / versionCode 442.
- Canonical Vulkan registry baseline: Vulkan 1.4.361 / VK_HEADER_VERSION 361.
- Submission schema: 2; technicalReport: 3; normalizer: 16.
- Worker/D1 runtime semantics: unchanged from 0.39.13; no new migration.

## Proven regression
A real long-lived Git checkout can contain historical source files that are intentionally absent from the compact predecessor release ZIP. 0.39.13 recursively classified every such file as an `unallowlisted new file`, so its quality gate passed on the clean ZIP but failed in the actual repository. Separately, `build_index.py` legitimately regenerates `data/index.json`; 0.39.13 pinned that generated file to one SHA-256 and therefore failed after normal index generation.

## Fix
- `verify_regression_contract.py` now defaults to source-overlay mode: every predecessor-owned path remains SHA-256 protected, but unrelated pre-existing repository/history files are not attributed to this release.
- `--strict-tree` remains fail-closed for source ZIP/package verification and rejects every unexpected package file.
- `data/index.json` is semantically verified (release/schema/Vulkan metadata and structural types) rather than fixed-hash verified.
- `quality_gate.py` performs `repair_repository.py --check` before regression checks so stale versioned app/workflow state produces an actionable failure rather than misleading regression noise.
- `test_existing_repo_overlay.py` permanently reproduces the real repository scenario and checks source-overlay tolerance, stale-app repair, generated-index regeneration, strict-package rejection and immutable predecessor mutation detection.

The repository repair is explicit and never silently run by the quality gate. Existing checkouts updated by extracting a release on top should run `python tools/repair_repository.py --apply` once before the gate.

Final 0.39.16 source gate: `python tools/quality_gate.py` PASS, including immutable 0.39.15 regression verification, historical Compare compatibility/negative mutations, Worker contracts, D1 migration replay and staged Pages artifact audit. Production Cloudflare deployment remains NOT EXECUTED.
