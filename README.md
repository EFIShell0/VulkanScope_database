# VulkanScope Database 0.39.2

VulkanScope Database 0.39.2 is a CI and GitHub Pages artifact-hygiene patch built on the 0.39.1 VulkanScope 0.41.5 compatibility contract.

## 0.39.2 highlights

- Fixes GitHub Actions builds failing because `tools/audit_database.py` confused checkout-owned top-level `.git/` metadata with shipped release files.
- Source verification now tolerates only the repository-owned top-level `.git` checkout metadata; nested `.git` content remains forbidden.
- GitHub Pages deployment is staged into an explicit allow-listed `_site` tree rather than uploading the repository root.
- The staged Pages tree receives its own fail-closed artifact audit before upload.
- Repository-only content such as `.git`, `.github`, `worker`, `tools`, `rules`, dependencies, caches and native/build outputs cannot enter the Pages artifact.
- Local HTML assets are revalidated against the staged tree before deployment.

## Canonical contract

- Current producer: **VulkanScope 0.41.5 / versionCode 415**.
- Compatible producer floor: VulkanScope 0.32.4+.
- Vulkan producer/query baseline: **1.4.360**.
- Database submission schema: **2**.
- `technicalReport` schema: **3**.
- Normalizer: **15**.
- D1 migration: none.

The 0.39.1 fail-closed validation for VulkanScope 0.41.4+ query diagnostics and queue/Vulkan Video semantics remains unchanged. The 0.39.0 filter, donut/statistics and canonical hash-routing frontend also remains unchanged.
