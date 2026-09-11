# VulkanScope Database 1.0.19 build / regression audit

- Immutable predecessor: VulkanScope Database 1.0.18 (`0b2bc5175a285ff15db76cd2bbfdb70d707251f19045e2d8cfa72cbf840bdbbf`).
- Fixes grouped coverage glow semantics so every non-zero dominant state glows regardless of whether the percentage happens to be below 80%; strictly smaller states remain hatched.
- Replaces premature Worker-version refresh signalling with a same-origin release-ready marker published only by the tag-gated Pages deployment after the GitHub Release job succeeds.
- Preserves atomic live report synchronization, schema 2 / technicalReport 3, normalizer 16, Vulkan 1.4.362/header 362, D1/storage semantics and existing security/resource ceilings.
- Mandatory gates: current verifier, negative mutations, source audit, Node syntax/route/Worker contracts, D1 migration replay, staged Pages audit, predecessor regression contract, clean-extract strict-tree and deterministic ZIP equality.
