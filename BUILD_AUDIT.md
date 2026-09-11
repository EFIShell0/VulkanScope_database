# VulkanScope Database 1.0.9 build audit

## Scope
1.0.9 is a live-data/UI consistency and producer-floor successor to immutable Database 1.0.8 (`aa406aafdf52bfa8e008e093e3518f4313ffd8ff4efaac1722ce923fe6f1744c`). It fixes the observed stale deploy-snapshot count / late report-row insertion path.

## Corrective contract
- preload/live reconciliation stages missing compact reports off-state and commits `state.reports` plus `state.index` only after the complete live index is satisfied;
- the initial visible render occurs after reconciliation, so Reports, metrics and statistics share one dataset;
- Report ID copies the exact 64-hex identifier; submission Date/Time/Time zone are separate and derive from server `submitted_at`;
- low (<20%) and very-low (<5%) coverage retains exact width but gains a distinct pattern/shape;
- new submissions require VulkanScope 1.0.19 / 1019 or newer; historical stored GETs remain readable.

## Preserved boundary
Schema 2, technicalReport 3, normalizer 16, Vulkan 1.4.362 registry corpus, D1 migrations, canonical report hashes, payload chunking, 2 MiB request ceiling, CORS/privacy rules and historical stored bytes are unchanged. No D1 migration or stored-report rewrite.

---

# VulkanScope Database 1.0.8 build audit

## Scope
1.0.8 is a release-tooling boundary fix over immutable Database 1.0.7 (`414da835326c3414215d598c8cf12b8391bfa112a5f02eff4031a788bfdf1b67`, 260 files). It addresses the observed GitHub tag-release failure where strict-package verification was incorrectly run against a history-bearing tagged checkout containing historical tracked frontend assets that were never members of the immutable 1.0.7 ZIP.

## Preserved runtime/data contracts
- current producer/query baseline: VulkanScope 1.0.15 / versionCode 1015 / Vulkan 1.4.362;
- submission schema 2 / technicalReport schema 3 / normalizer 16;
- VulkanScope 0.80.3 new-submission floor;
- D1 migrations remain exactly `0001_init.sql`, `0002_report_cursor_index.sql`, `0003_payload_chunks.sql`;
- Worker report validation, payload bytes, report IDs/hashes, privacy/CORS semantics and preload/live-delta behavior are unchanged;
- browser identity advances only to Database 1.0.8 / `assets/app.v1008.js` / cache key 1008.

## Root-cause correction
- tagged/long-lived Git checkout verification uses source-overlay mode, so unrelated historical tracked files do not masquerade as release-package members;
- raw tagged checkout `--strict-tree` invocation was removed from the release workflow;
- `tools/package_release.py` derives the exact package member set from the immutable predecessor manifest plus explicit successor additions/removals;
- deterministic ZIP construction excludes unrelated repository history and local `worker/package-lock.json`;
- the ZIP is clean-extracted, exact path-set checked, byte-compared to selected source files, then strict-tree and source-audited from inside the extract.

## Executed verification
- repository repair/check and source audit: PASS;
- immutable 1.0.7 -> 1.0.8 source-overlay regression: PASS;
- existing-repository overlay / generated-index / strict-package fixture: PASS;
- UTF-8, optional-lock, Vulkan registry and VulkanScope compatibility gates: PASS;
- route, Compare, historical Compare, Surface Compare and producer-baseline gates: PASS;
- loading/scroll, Encyclopedia, Vulkan 1.4.362, UI coherence and submission-diagnostics gates including negative mutations: PASS;
- retained 1.0.0/1.0.1/1.0.2/1.0.3/1.0.4/1.0.5/1.0.6/1.0.7 compatibility/hardening gates: PASS;
- new 1.0.8 release-boundary verifier and negative mutations: PASS;
- history-bearing tagged-checkout state machine with stale `site.v*.css` / `assets/app.js`: PASS;
- Worker JavaScript syntax and Worker contract: PASS;
- D1 migration-chain replay: PASS;
- Pages staging and Pages artifact audit: PASS.

The aggregate `tools/quality_gate.py` was started and progressed through its initial gates, but the hosted execution environment terminates long single commands before this project-wide chain completes. Every constituent gate was therefore executed separately and its result recorded above; no aggregate PASS is claimed for the timed-out single invocation.

## Packaging evidence
- deterministic release member count: 266 files;
- independent package build A: clean-extract exact path set, source-byte equality, strict-tree and source audit PASS;
- independent package build B: clean-extract exact path set, source-byte equality, strict-tree and source audit PASS;
- build A / build B ZIP byte equality: PASS.
The SHA-256 sidecar is emitted from the final sealed package after this audit and the successor hash contract are finalized.

# VulkanScope Database 1.0.7 build audit

## Scope
1.0.7 is a release/tooling hardening successor to immutable Database 1.0.6 (`a8f22f801d5b745179c4953450e48f5adcb2f59067149a805a84ab28f4391db9`, 253 files). It addresses the observed Windows `windows-tooling` Encyclopedia regeneration drift and the observed Windows Worker predeploy `spawnSync npm.cmd EINVAL` failure without changing report/data semantics.

## Corrective changes
- root `.gitattributes` enforces canonical LF text checkout and excludes binary artwork;
- Encyclopedia regeneration remains strict byte equality and now diagnoses CRLF checkout drift explicitly;
- `security-audit.mjs` launches npm's JavaScript CLI through `process.execPath` using `npm_execpath`, never `npm.cmd`;
- an existing audit lock is reused; a missing ignored lock is bootstrapped before exact Wrangler 4.130.0 / sharp 0.35.4 resolution+integrity checks and `npm audit --audit-level=high`;
- Windows CI pins Node 24, runs `npm install`, and executes the real `npm run security:audit`; Linux build also pins Node 24;
- a network-independent security-audit runner state machine verifies exact npm argv, existing-lock reuse, missing-lock bootstrap and audit invocation;
- browser identity advances only to Database 1.0.7 / `assets/app.v1007.js` / cache key 1007.

## Preserved invariants
- VulkanScope 1.0.15 / versionCode 1015 / Vulkan 1.4.362 current producer/query baseline;
- VulkanScope 0.80.3 new-submission floor;
- submission schema 2 / technicalReport schema 3 / normalizer 16;
- D1 migrations remain exactly `0001_init.sql`, `0002_report_cursor_index.sql`, `0003_payload_chunks.sql`;
- no stored-report rewrite, report-ID/hash rewrite, API schema change or capability/evidence semantic broadening;
- preload/live-delta, Compare, Surface and Encyclopedia semantics retained;
- Wrangler remains exact 4.130.0, sharp override exact 0.35.4, reviewed install scripts only; `npm audit fix --force` remains forbidden.

## Executed packaging-environment evidence
- repository repair/check: PASS;
- immutable 1.0.6 -> 1.0.7 source-overlay and strict-tree regression: PASS;
- source audit and audit-hygiene regressions: PASS;
- UTF-8, Vulkan registry, report-text, route, Compare, Surface, producer-baseline, floor/Encyclopedia, Vulkan 1.4.362, UI coherence and submission-diagnostic gates: PASS when run in bounded groups;
- retained 1.0.3/1.0.4/1.0.5/1.0.6 gates plus 1.0.7 verifier and negative mutations: PASS;
- security-audit npm-cli runner state machine (existing lock + missing-lock bootstrap): PASS;
- Worker syntax/contract: PASS;
- in-memory D1 migration replay: PASS;
- staged Pages artifact audit: PASS;
- deterministic packaging: two independently generated ZIPs byte-identical PASS;
- clean-extract source equality: 260/260 packaged files byte-identical PASS;
- clean-extract repository check, strict regression, source audit, Encyclopedia regeneration, retained 1.0.6 verifier, 1.0.7 verifier/negative mutations, security-audit runner, Worker contract, D1 replay and Pages artifact audit: PASS.

The monolithic `quality_gate.py` exceeds this packaging environment's single-command 120-second execution budget; its constituent gates above were executed separately rather than misreported as one aggregate PASS. A real GitHub `windows-latest` checkout and a network-backed `npm audit` are **NOT EXECUTED** in this packaging environment and remain mandatory runtime evidence in the pushed workflow/operator deployment.
