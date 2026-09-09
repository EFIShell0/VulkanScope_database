# VulkanScope Database 1.0.4 build / regression audit

## Release identity
- Database version: 1.0.4
- Immutable predecessor: VulkanScope Database 1.0.3
- Predecessor ZIP SHA-256: `bebd99a8823070239e949ca1c1c06f8460519fcbe2e4173ebb56a800b96623a0`
- Predecessor package census: 235 files
- Current producer/query baseline: VulkanScope 1.0.15 / versionCode 1015 / Vulkan 1.4.362
- New-submission floor: VulkanScope 0.80.3
- Submission schema 2 / technicalReport 3 / normalizer 16
- D1 migration: none

## Release scope
Database 1.0.4 is a release-engineering hardening successor to 1.0.3. It preserves the 1.0.3 preload/live-delta browser behavior, scroll progress/controls, filter-icon semantics, VulkanScope 1.0.15 producer contract, evidence-state semantics, D1 data model and stored report bytes/hashes.

The Windows-only `C:\\C:\\...` regression exposed by the 1.0.3 deployment log is corrected in all four affected path-sensitive Node ESM tests by using `fileURLToPath(import.meta.url)`. The canonical GitHub workflow now has a mandatory `windows-latest` prerequisite job that executes those Compare and Surface tests before the Linux build/deploy is eligible to proceed.

Worker tooling advances from Wrangler 4.125.0 to exactly pinned Wrangler 4.130.0. Project `allowScripts` explicitly reviews `esbuild`, `sharp` and `workerd`; blanket install-script approval is not used. `npm run deploy` now runs the fail-closed Cloudflare account verifier and `npm audit --audit-level=high` through `predeploy`, so high/critical npm advisories block production deploy rather than being silenced with `npm audit fix --force`.

GitHub Release creation no longer depends on a locally installed `gh`. The canonical workflow handles `v*` tag pushes after the mandatory build gates, creates deterministic release assets on a GitHub-hosted runner, and uses the runner-provided GitHub CLI plus scoped `github.token`. Reruns upload assets with `--clobber` when the release already exists.

No D1 migration, stored-report rewrite, report-ID/hash rewrite, normalizer bump, producer-floor change or capability/evidence inference change is introduced.

## Executed packaging-environment evidence
- repository repair/check: PASS;
- source audit: PASS;
- deterministic UTF-8 tooling and optional-lock policy: PASS (optional lock absent in release workspace);
- Vulkan 1.4.362 registry lock and retained VulkanScope 0.41.32 report-text compatibility: PASS;
- immutable 1.0.3 -> 1.0.4 source-overlay and strict-package regression contract: PASS;
- existing-repository overlay/generated-index/strict-package fixture: PASS;
- source/artifact audit-hygiene regression suite: PASS;
- frontend and Encyclopedia JavaScript syntax: PASS;
- hash routes and Compare contract: PASS;
- historical Compare compatibility and negative mutations: PASS;
- Surface Compare evidence contract and negative mutations: PASS;
- retained 0.41.46 producer-baseline surface and negative mutations: PASS;
- retained 0.80.8 loading/scroll/floor/device-type model and negative mutations: PASS;
- retained 0.80.9 floor/Encyclopedia model and negative mutations: PASS;
- retained Vulkan 1.4.362 corpus, UI coherence, submission diagnostics and exact registry-prefix gates: PASS;
- retained 1.0.0 producer baseline and 1.0.1 Surface-evidence contract/model/negative suite: PASS;
- retained 1.0.2 producer baseline/state model/negative suite: PASS;
- retained 1.0.3 preload/UI/compatibility verifier and preload-builder fixture on 1.0.4: PASS;
- 1.0.4 Windows/toolchain/release verifier and negative-mutation suite: PASS;
- complete Worker contract: PASS;
- in-memory D1 migration-chain replay: PASS;
- staged Pages artifact build and audit: PASS.

The aggregate `tools/quality_gate.py` was started and passed its early immutable-regression/source-audit stages, but the container execution ceiling terminated the long one-command chain. The same mandatory constituents were subsequently executed explicitly in grouped commands and pass. The aggregate command is therefore not mislabelled as a packaging-environment one-command PASS.

## Dependency / live-runtime evidence boundary
The packaging container cannot resolve `registry.npmjs.org`, so a fresh network-backed `npm audit` for Wrangler 4.130.0 is **NOT EXECUTED** here. This is not waived: `worker/package.json` makes `npm audit --audit-level=high` part of `predeploy`; production deployment fails if that audit is not clean at high/critical severity.

A real `windows-latest` GitHub Actions execution is also **NOT EXECUTED** in this local packaging environment. The path conversion is statically/behaviorally regression-protected here, and the canonical CI makes the Windows runtime test a prerequisite for Pages deploy and tag release.

Live Cloudflare Worker/Pages deployment, remote D1 smoke testing and the automatic GitHub Release job for 1.0.4 are **NOT EXECUTED** in this packaging environment. They may only be promoted to PASS after the user pushes/deploys this release.

## Packaging evidence
- strict release-tree verification against immutable 1.0.3: PASS;
- two independently generated deterministic ZIPs: byte-identical PASS;
- final package census: 241 files;
- clean-extract source/package SHA-256 equality for every packaged file: PASS;
- extracted-package repository check, strict regression verification and source audit: PASS;
- extracted-package retained 1.0.3 preload/UI verifier and preload-builder fixture: PASS;
- extracted-package 1.0.4 Windows/toolchain/release verifier and negative-mutation suite: PASS;
- extracted-package Worker contract and in-memory D1 migration replay: PASS;
- extracted-package staged Pages artifact build/audit: PASS.

The final ZIP digest is emitted as a separate `.sha256` sidecar so the archive does not contain a self-referential package hash. The independently generated reproduction ZIP is not embedded in the release archive.
