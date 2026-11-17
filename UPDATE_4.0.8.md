# VulkanScope Database 4.0.8 — Cleanup release

This release removes obsolete root update notes/installers and unreferenced generated CSS, encyclopedia and JXL probe revisions. Historical rules, regression fixtures and licensing notices are retained as required by `rules/PROJECT_RULES.md`. Current v4008 browser/JXL behavior inherits 4.0.7; v4007 startup JS is kept as the one-release cache bridge. No D1 migration is required.

## Manual deployment

Use `install_4_0_8.ps1` only from an extracted, checksum-verified release, starting from a clean Git checkout. Commit/push source changes to run CI/Pages; deploy the Cloudflare Worker separately only after success. Source ZIP creation does not deploy the database or migrate D1.
