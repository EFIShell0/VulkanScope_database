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
