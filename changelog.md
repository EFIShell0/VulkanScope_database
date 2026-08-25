# VulkanScope Database 0.39.6

- Adds tuple-aware Image Format Properties2 comparison for VulkanScope 0.41.8.
- Exact `Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED` rows now compare as **Unsupported**, not Available or Unknown.
- `Unavailable: VkResult=<n>` rows remain **Unavailable** and are never inferred Unsupported.
- Properties query-coverage semantics remain separate: an explicit format-not-supported result still proves the query executed, while Compare presents the tuple capability result.
- Historical successful Image Format Properties2 rows compare under the same tuple identity without rewriting stored reports.
- Worker validation hardens 0.41.8+ tuple-state syntax and current producer metadata advances to VulkanScope 0.41.8 / 418.
- Preserves schema 2, technicalReport 3, normalizer 15, Vulkan 1.4.360, existing D1 data and the 0.32.4+ compatibility floor.
