# VulkanScope Database 0.39.3

VulkanScope Database 0.39.3 is a CI/source-audit hardening release built on the 0.39.2 Pages-artifact separation and the 0.39.1 VulkanScope 0.41.5 compatibility contract.

## 0.39.3 highlights

- Source audit prunes repository-owned root `.git` before traversal.
- Nested `.git` remains forbidden.
- `--source-tree` and `--version` make CI scope/version explicit.
- GitHub Actions updated to checkout/setup-python v7, configure-pages v6 and upload-pages-artifact v5; deploy-pages v5.
- Checkout credentials are not persisted and write permissions are limited to the deploy job.
- Pages continues to deploy only allow-listed `_site`.
- `.nojekyll` is preserved explicitly via `include-hidden-files: true`.
- Database schema 2, technicalReport 3, normalizer 15 and VulkanScope 0.41.5/415 producer semantics are unchanged.

See `release.md`, `BUILD_AUDIT.md`, `rules/PROJECT_RULES.md` and `rules/0.39.3_GITHUB_ACTIONS_SOURCE_AUDIT_HARDENING.md`.

- Automated audit hygiene regression tests verify root checkout metadata acceptance and nested/artifact `.git` rejection.

- Source verification rejects extra `.github/workflows/*.yml`/`.yaml` files so an obsolete workflow cannot continue running independently.
- The distributed ZIP is laid out at repository root (not inside an extra version directory) so extraction directly over the repository replaces `tools/` and hidden `.github/` paths instead of creating a nested project.
