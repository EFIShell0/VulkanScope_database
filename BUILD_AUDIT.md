# VulkanScope Database 0.39.3 Build / Contract Audit

## Release identity
- Database: `0.39.3`
- VulkanScope producer baseline: `0.41.5 / 415`
- Vulkan baseline: `1.4.360`
- Submission schema: `2`
- technicalReport schema: `3`
- Normalizer: `15`

## 0.39.3 CI correction
The source audit prunes the checkout-owned root `.git` directory before recursion. Artifact auditing is separate and still rejects every `.git` occurrence. CI prints the audit-tool version, uses explicit source/artifact modes, stages only `_site`, preserves `.nojekyll`, and uses least-privilege GitHub Actions permissions.

## Release gates
- Source audit with a real Git repository checkout
- Nested `.git` negative test
- Pages staging and artifact audit
- Pages `.git` negative test
- Frontend and Worker JavaScript syntax
- Hash-route and Worker contract tests
- JSON/HTML/local-resource/package-hygiene checks

- Automated audit hygiene regression tests verify root checkout metadata acceptance and nested/artifact `.git` rejection.

- Source verification rejects extra `.github/workflows/*.yml`/`.yaml` files so an obsolete workflow cannot continue running independently.
- The distributed ZIP is laid out at repository root (not inside an extra version directory) so extraction directly over the repository replaces `tools/` and hidden `.github/` paths instead of creating a nested project.
