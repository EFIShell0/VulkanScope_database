# VulkanScope Database 0.39.2

VulkanScope Database 0.39.2 fixes the GitHub Pages CI/release-artifact boundary without changing report data semantics.

## Fixed

- Fixed `tools/audit_database.py` falsely treating GitHub Actions' repository-owned top-level `.git/` checkout metadata as shipped release content.
- Split source-tree verification from deployable Pages-artifact verification.
- Added `tools/build_pages_artifact.py` to build an explicit allow-listed `_site` tree.
- GitHub Pages now uploads `_site` instead of the repository root.
- Added fail-closed Pages-artifact checks for unexpected top-level files, `.git`, `.github`, `worker`, `tools`, `rules`, caches, local dependencies, binaries, symlinks and broken local HTML asset references.
- Kept nested/embedded `.git` material forbidden; only the repository-owned top-level checkout metadata is ignored by source verification.

## Preserved

- VulkanScope 0.41.5 / versionCode 415 current-producer identity.
- Vulkan 1.4.360 producer/query baseline.
- Schema 2 / `technicalReport` 3 / normalizer 15.
- 0.41.4+ strict query-diagnostic and queue/Vulkan Video validation introduced in 0.39.1.
- Existing report IDs, report hashes and D1 rows.
- 0.39.0 filter/statistics/hash-routing behavior.
- No D1 migration, report rewrite, capability inference or schema migration.

## CI verification

The release gate explicitly verifies both sides of the boundary:

- source checkout with a top-level `.git/` directory: **PASS**;
- staged `_site` without repository/development content: **PASS**;
- staged `_site` with an injected `.git/` directory: **FAIL**, as required.
