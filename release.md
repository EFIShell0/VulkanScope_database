# VulkanScope Database 0.39.7

- Adds native support for VulkanScope 0.41.9's separated Image Format Properties2 non-success query-outcome dataset.
- Non-success tuple outcomes no longer enter Properties & Limits property/query totals.
- Compare still matches historical AVAILABLE Image Format Properties2 rows against current UNSUPPORTED/UNAVAILABLE outcomes by the same canonical tuple key.
- Report detail Formats now shows exact non-success tuple results in a dedicated table.
- Worker validation is fail-closed for 0.41.9+: unique canonical tuple names, `unsupported` only with `VK_ERROR_FORMAT_NOT_SUPPORTED` (-11), and `unavailable` only with another non-zero numeric VkResult.
- Historical VulkanScope 0.41.8 reports remain accepted under their embedded tuple-state contract.
- Current producer baseline is VulkanScope 0.41.9 / 419; schema 2, technicalReport 3, normalizer 15, Vulkan 1.4.360 and D1 storage remain unchanged.
