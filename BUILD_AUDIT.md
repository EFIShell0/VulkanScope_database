# VulkanScope Database 0.39.2 Build / Contract Audit

## Release identity

- Database: `0.39.2`
- Current producer: VulkanScope `0.41.5` / versionCode `415`
- Compatible producer floor: VulkanScope `0.32.4+`
- Vulkan baseline: `1.4.360`
- Submission schema: `2`
- `technicalReport` schema: `3`
- Worker normalizer: `15`
- D1 migration: none

## CI failure fixed

0.39.1 recursively scanned the source checkout and reported GitHub Actions' normal `.git/` metadata as `forbidden release artifact`. That was a layer-boundary error: repository metadata is expected in a source checkout but must never be present in the deployable Pages artifact.

0.39.2 separates those concerns:

1. `tools/audit_database.py` audits the source checkout while ignoring only repository-owned top-level `.git` metadata.
2. `tools/build_pages_artifact.py _site` stages only explicitly public files/directories.
3. `tools/audit_database.py --artifact-tree _site` performs a strict deployable-artifact audit.
4. `actions/upload-pages-artifact` uploads `_site`, not `.`.

The artifact audit rejects VCS/development directories, unexpected top-level entries, symlinks, build/cache artifacts and broken local HTML resources.

## Verification performed

- `python tools/build_index.py`: PASS
- Source `python tools/audit_database.py`: PASS
- Frontend JavaScript syntax: PASS
- Canonical hash-route contract suite: PASS
- Worker JavaScript syntax: PASS
- Worker contract suite: PASS
- `_site` staging: PASS
- `_site` artifact audit: PASS
- Simulated GitHub checkout with top-level `.git`: source audit PASS
- Injected `_site/.git`: artifact audit FAIL as required
- Clean `_site` after negative test: artifact audit PASS

No report schema, normalizer, D1 data, report ID/hash, filter/statistics semantics or VulkanScope 0.41.5 producer semantics changed in this patch.
