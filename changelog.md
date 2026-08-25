# VulkanScope Database changelog

## 0.39.2

- Fixed GitHub Actions audit failures caused by treating checkout-owned top-level `.git/` metadata as shipped release content.
- Added explicit allow-listed GitHub Pages staging via `_site`.
- Added a separate fail-closed deployable-artifact audit.
- GitHub Pages now uploads `_site` instead of the repository root.
- Preserved 0.39.1 producer validation, schema/normalizer/D1 semantics and 0.39.0 filter/statistics/hash-routing behavior.

## 0.39.1

- Updated the current producer identity to VulkanScope 0.41.5 / versionCode 415.
- Made the strict 0.41.4 query-diagnostic and queue/Vulkan Video validation contract version-range aware so it also applies to 0.41.5 and future compatible producers.
- Preserved schema 2, technicalReport 3, normalizer 15, report hashes and existing D1 rows.
