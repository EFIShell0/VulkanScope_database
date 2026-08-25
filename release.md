# VulkanScope Database 0.39.5

- Canonicalizes profile comparison so normalized profile evidence is shown once instead of being duplicated as `PROFILES` and `VULKAN PROFILES`.
- Adds a cross-producer comparison notice when VulkanScope producer versions differ.
- Adds a `Common evidence only` compare filter to separate common capability evidence from one-sided collector/evaluator coverage.
- Calls out profile revision mismatches so differing profile definitions are not mistaken for driver regressions.
- Advances the current producer/query baseline to VulkanScope 0.41.7 / 417 while preserving schema 2, technicalReport 3, normalizer 15 and the 0.32.4+ compatibility floor.
- Keeps Vulkan 1.4.360 and the deployment-verified Cloudflare compatibility date unchanged.
