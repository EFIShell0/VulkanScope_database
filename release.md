# VulkanScope Database 0.37.1

- Updated current producer identity to VulkanScope 0.41.3 / versionCode 413.
- Fixed queue flag zero-mask presentation: `VkQueueFlags == 0` is no longer shown as a fabricated `VK_NONE` token.
- Added explicit Vulkan Video codec-operation query state handling. Successfully queried zero masks display `VK_VIDEO_CODEC_OPERATION_NONE_KHR`; Not applicable, Unavailable and Unknown remain distinct.
- Queue capability booleans continue to use Supported/Unsupported because they are direct `VkQueueFlags` evidence.
- Properties and limits now label availability as query state so a reported boolean `false` is not visually confused with unsupported feature state.
- No D1 migration, stored-payload rewrite, report-hash rewrite, or schema change is required.
