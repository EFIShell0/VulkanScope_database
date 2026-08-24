# VulkanScope Database 0.37.1

VulkanScope Database 0.37.1 is the matching Database release for VulkanScope 0.41.3 / versionCode 413 while retaining compatibility with VulkanScope 0.32.4+ schema-2 / technicalReport-3 reports.

## 0.37.1

- Queue and Vulkan Video query/support semantics are separated.
- Zero queue flags are displayed as zero rather than `VK_NONE`.
- Successfully queried zero Vulkan Video codec masks use `VK_VIDEO_CODEC_OPERATION_NONE_KHR`.
- Property/limit availability is labeled as query state to avoid confusing `false` values with unsupported feature state.
- Existing report storage and D1 schema remain unchanged.
