# VulkanScope Database 1.0.12 build / regression audit

## Release identity
- Database version: 1.0.12
- Immutable predecessor: VulkanScope Database 1.0.11
- Predecessor ZIP SHA-256: `cda8c117ae023f9d7abfdb532ad410f053a0a44140c4107bb7cfd78a957cf0dc`
- Current producer/query baseline: VulkanScope 1.0.19 / versionCode 1019 / Vulkan 1.4.362
- New-submission floor: VulkanScope 1.0.19
- Submission schema 2 / technicalReport 3 / normalizer 16
- D1 migration: none

## UI/navigation scope
1. Low coverage retains exact ratio width and state color while replacing the former wedge/white treatment with a thick black diagonal hatch only.
2. Coverage >=80% receives a bounded state-colored glow and moving highlight; reduced-motion disables the decorative animation.
3. Reports submission Date/Time/Time zone are collapsed by default behind a three-line Submitted-header control and remain server-authored from D1 `submitted_at`.
4. Source-route scroll position is remembered before entering report detail and restored after route rendering on browser/in-page Back.
5. Android-version filter artwork is the exact current VulkanScope application `ic_android.xml` vector geometry/colors, embedded locally.

## Non-regression boundary
The 1.0.11 GitHub Actions command-boundary behavior, 1.0.10 row-array contract and 1.0.9 atomic live/report-ID/1.0.19-floor behavior remain protected. No D1 migration, stored-report rewrite, report-hash rewrite, schema/normalizer change, Vulkan registry change or privacy/transport weakening is introduced.

## Required evidence
- `tools/verify_1_0_12_reports_visual_navigation_ui.py`
- `tools/test_1_0_12_reports_visual_navigation_ui_negative_mutations.py`
- aggregate `tools/quality_gate.py`
- immutable 1.0.11 -> 1.0.12 source-overlay and strict-package verification
- Worker contract and in-memory D1 migration-chain replay
- Pages allow-list staging and deterministic release ZIP construction

Live Cloudflare deployment, browser visual inspection and remote production D1 smoke testing are not executed by this packaging environment.
