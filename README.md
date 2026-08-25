# VulkanScope Database 0.39.6

VulkanScope Database 0.39.6 adds exact Image Format Properties2 tuple-state comparison for VulkanScope 0.41.8 while preserving the 0.39.x filter/statistics/hash-route architecture, schema 2 / technicalReport 3, normalizer 15 and existing D1 storage.

## 0.39.6 Image Format Properties2 tuple-state correctness

- `Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED` is shown as direct Unsupported evidence for that exact VulkanScope Image Format Properties2 query combination.
- `Unavailable: VkResult=<n>` remains Unavailable and is never inferred Unsupported.
- Missing tuple evidence remains Unknown / Not reported.
- Properties query-coverage and tuple capability semantics stay separate: an explicit negative result proves the query executed while preserving its capability outcome.
- Historical successful tuple rows compare under the same canonical key without rewriting stored reports.
- Worker validation applies the 0.41.8 tuple contract fail-closed to 0.41.8+ compatible producers.

## 0.39.5 cross-producer compare correctness

Compare distinguishes producer/evaluator coverage from direct driver evidence. When producer versions differ, the page shows an explicit warning and offers `Common evidence only`. Normalized profile evidence is canonicalized into one `PROFILES` section, with revision changes retained as values rather than duplicate row identities.

## 0.39.4 highlights


- GitHub checkout source hygiene uses Git-tracked paths instead of recursively walking `.git` metadata.
- Every audit run prints `VulkanScope Database audit tool 0.39.4` so the exact script in use is visible in Actions logs.
- Added `tools/repair_repository.py` plus a canonical workflow template to repair hidden `.github/workflows` files after in-place ZIP updates.
- Stale workflow files and stale `assets/app.v*.js` versions are rejected.
- Pages staging now copies an explicit public-asset allow-list instead of copying the whole `assets` directory.
- Report schema 2, technicalReport schema 3, normalizer 15 and VulkanScope 0.41.8 / Vulkan 1.4.360 is the current producer/query baseline; historical compatible producers remain accepted.

See `release.md`, `BUILD_AUDIT.md`, `rules/PROJECT_RULES.md`, `rules/0.39.6_IMAGE_FORMAT_PROPERTIES2_TUPLE_STATE_0.41.8_AUDIT.md` and the historical audit records.
