# VulkanScope Database 0.39.8 Build / Release Audit

- Database: `0.39.8`
- Current VulkanScope producer baseline: `0.41.10` / `420`
- Vulkan producer/query baseline: `1.4.360`
- Submission schema: `2`
- technicalReport schema: `3`
- Normalizer: `15`
- D1 migration: none
- Stored payload/hash rewrite: none

## Image Format Properties2 correctness
0.39.8 consumes VulkanScope 0.41.10's complete bounded tuple-state ledger separately from normal detailed properties. Current-producer validation requires six canonical states per scheduled format and cross-checks them against the fixed query recipe and aggregate query counters. Available rows retain their full property payload; Unsupported, Unavailable and Not applicable remain distinct and never inflate Properties & Limits totals.

## Verification
Release verification is performed from both the source tree and the final packaged ZIP. The final results are recorded before packaging is published.

## Final source-tree gate execution — 2026-08-25

The 0.39.8 working source was rebuilt/indexed and verified after the final changes:

- repository canonical-state check: **PASS**
- source-tree audit: **PASS**
- audit-hygiene regression suite: **PASS**
- frontend JavaScript syntax: **PASS**
- hash-route contract suite: **PASS**
- Compare contract suite, including the Image Format Properties2 canonical tuple identity: **PASS**
- Worker JavaScript syntax: **PASS**
- Worker contract suite, including the explicit `VK_FORMAT_S8_UINT · LINEAR · ANDROID_HARDWARE_BUFFER` missing-ledger rejection: **PASS**
- allow-listed Pages staging and staged-artifact audit: **PASS**
- supplemental Python/JSON syntax checks: **PASS**

The staged `_site` directory is an audit product only and is removed before the source release ZIP is created.

## Candidate source-ZIP extraction gate

A root-layout candidate 0.39.8 source ZIP was created from the clean release tree and extracted into a new empty directory. From that extracted candidate, source audit, repository-state check, audit-hygiene suite, frontend syntax, hash-route tests, Compare contract tests, Worker syntax/contracts, Pages staging and staged Pages-artifact audit all returned **PASS**. The published ZIP is rebuilt from this same audited source after this record is added and is rechecked once more after creation.
