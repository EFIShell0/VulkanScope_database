# VulkanScope Database 1.0.20 build / regression audit

- Immutable predecessor: VulkanScope Database 1.0.19 (`0e0f6ab19e86e685f0bb57188d221db702e1d9611112703d251c3498195d3728`).
- Root-cause recovery: cached 1.0.18 frontends no longer receive a Worker `databaseVersion`, so Worker deployment cannot generate a frontend refresh loop. Accurate Worker identity moved to informational release fields.
- Source release marker is fail-closed (`releaseReady:false`); only the post-GitHub-Release staged Pages artifact may transition to ready.
- Update prompts require marker + published HTML + exact application asset agreement and use bounded session retry suppression if a cache-busted refresh still serves the old frontend.
- Production Pages publication originates from validated `main`, creates/releases `v1.0.20` first, then stages/marks/audits/uploads/deploys with the documented Pages action versions.
- Live report synchronization, all 1.0.19 coverage/UI semantics, Vulkan 1.4.362/header 362, schema 2 / technicalReport 3 / normalizer 16, D1 payload semantics and security/resource ceilings are preserved.
- Mandatory gates include regression contract, 1.0.20 verifier + negative mutations, source audit, Worker contract, D1 migration replay, non-ready and ready staged Pages audits, clean-extract strict-tree verification and deterministic ZIP construction.
