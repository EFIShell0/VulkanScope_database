# VulkanScope Database 1.2.2 build / regression audit

- Database/frontend/Worker release identity: **1.2.2**.
- Immutable predecessor: VulkanScope Database 1.2.1 ZIP SHA-256 `8df3051f0c495a1c245792cbccf431660de906a1ab757129c140f197a1944107`.
- Frontend identity: `assets/app.v1202.js`, cache key **1202**.
- Release workflow keeps job-scoped `contents: write` only on the release job.
- GitHub Release creation/upload uses bounded retry for transient HTTP 429/5xx failures and re-checks tag/release ownership against validated `GITHUB_SHA` before every mutating attempt.
- Existing tags/releases that resolve to another commit fail closed and require a version bump; no published tag is retargeted.
- D1 schema/migrations, stored payload bytes/hashes, report IDs, normalizer 16, Vulkan 1.4.362 and VulkanScope 1.2.5 producer floor are unchanged.
- Mandatory gates: immutable 1.2.1→1.2.2 regression contract, 1.2.2 release-retry verifier + negative mutations, inherited 1.2.1 UI semantics, Worker transport contract, source audit, D1 migration replay, Pages release-ready transition and deterministic strict ZIP construction.
