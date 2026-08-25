# VulkanScope Database changelog

## 0.39.4

- Replaced recursive Git-checkout hygiene scanning with a tracked-file manifest.
- Added canonical workflow verification and an in-place repository repair tool.
- Rejects stale workflows and stale versioned frontend app JavaScript.
- Pages staging now copies an exact public asset allow-list.

## 0.39.3

- Hardened source checkout audit by pruning root `.git` before recursion.
- Added explicit audit version/source modes and CI diagnostics.
- Updated GitHub Pages actions and least-privilege workflow permissions.
- Preserved `.nojekyll` through the current Pages artifact uploader.
- No report/data/schema/normalizer/filter semantic changes.

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
