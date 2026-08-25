# VulkanScope Database 0.39.4

VulkanScope Database 0.39.4 fixes the remaining GitHub Actions checkout/audit failure class and hardens in-place repository updates.

## Changes

- Source hygiene uses `git ls-files` in a GitHub checkout, so `.git/objects`, `.git/refs`, logs and other repository metadata are structurally outside the audited release-file manifest.
- The non-Git/release-ZIP fallback still prunes only the repository root `.git` entry and rejects nested VCS metadata and symlinks.
- Normal audit runs print their own version before any checks.
- Added a canonical workflow template and `tools/repair_repository.py`.
- Repository repair can replace `.github/workflows` even when a file-copy/update method failed to overwrite hidden dot-directories.
- Repository repair removes stale versioned frontend app JavaScript left by archive extraction.
- Exactly one current `app.v*.js` is accepted.
- GitHub Pages staging uses an explicit public asset allow-list instead of copying the entire source `assets/` tree.
- Staged artifact auditing rejects any unexpected/stale asset even if it has a normally allowed file extension.
- Existing hash routing, advanced filters, statistics/donut behavior, Worker validation, privacy and report semantics are unchanged.

## Contract

- Database: 0.39.4
- Current VulkanScope producer: 0.41.5 / versionCode 415
- Vulkan baseline: 1.4.360
- Submission schema: 2
- `technicalReport` schema: 3
- Normalizer: 15
- D1 migration: none
