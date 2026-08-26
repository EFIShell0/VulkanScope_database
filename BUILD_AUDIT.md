# VulkanScope Database 0.39.10 Build / Release Audit

- Database: `0.39.10`
- Current producer: VulkanScope `0.41.12` / versionCode `422`
- Vulkan producer/query baseline: `1.4.360`
- Submission schema: `2`
- technicalReport schema: `3`
- Normalizer: `16`
- D1 migration: none
- Stored payload/hash rewrite: none

## HTTP 400 root cause

Database 0.39.9 validated Image Format Properties2 tuple names with a format-token grammar equivalent to `VK_FORMAT_[A-Z0-9_]+`. That grammar is not valid for the complete Vulkan format namespace: canonical ASTC format tokens contain lowercase `x` dimension separators, for example `VK_FORMAT_ASTC_10x8_SRGB_BLOCK` and `VK_FORMAT_ASTC_4x4x3_UNORM_BLOCK_EXT`.

VulkanScope 0.41.12 correctly preserves those canonical Vulkan names. The 0.39.9 Worker therefore rejected otherwise valid complete reports with HTTP 400 (`Incomplete or invalid VulkanScope submission schema`). The earlier synthetic submission fixture used `VK_FORMAT_S8_UINT`, so it did not exercise the broken name class.

## Correction

- Worker tuple validation now accepts registry-style lowercase `x` numeric dimension separators inside canonical `VK_FORMAT_*` tokens.
- Arbitrary lowercase text and punctuation remain rejected.
- Producer evidence is not rewritten, uppercased, filtered or omitted.
- Existing complete tuple-ledger result/diagnostic cross-checks remain unchanged and fail closed.
- Worker tests cover both `VK_FORMAT_ASTC_10x8_SRGB_BLOCK` and `VK_FORMAT_ASTC_4x4x3_UNORM_BLOCK_EXT`, plus a malformed lowercase-separator rejection case.
- Cross-check against VulkanScope 0.41.12's checked-in format-name table found 298 format tokens; the previous grammar rejected 72 canonical ASTC names, while the corrected grammar accepts all 298.

## Final source-tree gates

- canonical repository-state check: **PASS**
- source-tree audit: **PASS**
- audit-hygiene regression suite: **PASS**
- frontend JavaScript syntax: **PASS**
- hash-route contract suite: **PASS**
- Compare contract suite: **PASS**
- Worker JavaScript syntax: **PASS**
- Worker contract suite, including canonical ASTC 2D/3D submission fixtures: **PASS**
- allow-listed Pages staging and staged-artifact audit: **PASS**
- supplemental Python/JSON syntax checks: **PASS**
