# VulkanScope Database 0.39.4 Build / Contract Audit

## Release identity
- Database: `0.39.4`
- VulkanScope producer: `0.41.5 / 415`
- Vulkan baseline: `1.4.360`
- Submission schema: `2`
- technicalReport schema: `3`
- Normalizer: `15`

## 0.39.4 CI correction

The source checkout audit no longer derives release-file hygiene by recursively walking the working directory when `.git` is present. A real Git checkout is audited from `git ls-files`, which contains repository content but not `.git` implementation metadata. This removes the `.git/objects`, `.git/refs`, `.git/logs`, hooks and pack false-positive class without weakening the deploy-artifact audit.

The release also checks the hidden workflow against a canonical visible template and provides an in-place repair tool for updates where a copy/extraction method left the old `.github/workflows/pages.yml` behind.

Pages staging now copies exact public assets rather than the complete source assets directory, preventing stale versioned JavaScript from being deployed after in-place archive extraction.
