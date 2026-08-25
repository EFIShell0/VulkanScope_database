# VulkanScope Database 0.39.5

VulkanScope Database 0.39.5 is a GitHub Actions/source-audit reliability patch built on the 0.39.x filtering/statistics UI and the VulkanScope 0.41.7 compatibility contract.

## 0.39.5 cross-producer compare correctness

Compare now distinguishes producer/evaluator coverage from direct driver evidence. When producer versions differ, the page shows an explicit warning and offers `Common evidence only`. Normalized profile evidence is canonicalized into one `PROFILES` section, with revision changes retained as values rather than duplicate row identities.

## 0.39.4 highlights

- GitHub checkout source hygiene uses Git-tracked paths instead of recursively walking `.git` metadata.
- Every audit run prints `VulkanScope Database audit tool 0.39.4` so the exact script in use is visible in Actions logs.
- Added `tools/repair_repository.py` plus a canonical workflow template to repair hidden `.github/workflows` files after in-place ZIP updates.
- Stale workflow files and stale `assets/app.v*.js` versions are rejected.
- Pages staging now copies an explicit public-asset allow-list instead of copying the whole `assets` directory.
- Report schema 2, technicalReport schema 3, normalizer 15 and VulkanScope 0.41.7 / Vulkan 1.4.360 compatibility are unchanged.

See `release.md`, `BUILD_AUDIT.md`, `rules/PROJECT_RULES.md` and `rules/0.39.4_TRACKED_SOURCE_AUDIT_REPOSITORY_REPAIR.md`.
