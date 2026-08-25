# VulkanScope Database 0.39.3

VulkanScope Database 0.39.3 hardens the GitHub Actions/source-audit boundary and updates the Pages workflow to the current verified GitHub action majors without changing report semantics.

## Changes

- Source audit now prunes repository-owned top-level `.git` before recursive traversal.
- Nested `.git` remains fail-closed.
- Added explicit `--source-tree` and `--version` audit modes.
- CI logs the audit tool version before running checks.
- Updated GitHub Actions to checkout v7, setup-python v7, configure-pages v6, upload-pages-artifact v5 and deploy-pages v5.
- Disabled persisted checkout credentials and restricted Pages/id-token write permissions to deploy only.
- Preserved `_site/.nojekyll` explicitly with upload-pages-artifact v5 `include-hidden-files: true`.
- Pages still uploads only the allow-listed `_site` tree and separately audits it.
- No D1 migration, schema change, report rewrite/hash change, normalizer change, frontend filter/statistics change or producer-semantics change.

## Baseline

- Database: 0.39.3
- Current producer: VulkanScope 0.41.5 / versionCode 415
- Vulkan published/query baseline: 1.4.360
- Submission schema: 2
- technicalReport schema: 3
- Normalizer: 15

- Automated audit hygiene regression tests verify root checkout metadata acceptance and nested/artifact `.git` rejection.

- Source verification rejects extra `.github/workflows/*.yml`/`.yaml` files so an obsolete workflow cannot continue running independently.
- The distributed ZIP is laid out at repository root (not inside an extra version directory) so extraction directly over the repository replaces `tools/` and hidden `.github/` paths instead of creating a nested project.
