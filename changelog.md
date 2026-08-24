# VulkanScope Database 0.37.1

## Queue and Vulkan Video semantics
- Corrected zero `VkQueueFlags` presentation.
- Added explicit `videoCodecQueryStatus` / `videoCodecQueryReason` handling from VulkanScope 0.41.3 technical reports.
- Uses `VK_VIDEO_CODEC_OPERATION_NONE_KHR` only for a successfully queried zero codec-operation mask.
- Old reports without explicit query state are conservatively derived from `VK_KHR_video_queue` and Queue Family Properties 2 query evidence; missing evidence stays Unknown.

## Property availability clarity
- Property and limit tables label Available/Unavailable as query availability rather than capability support.
- A property value of `false` can therefore be shown as `QUERY AVAILABLE` without implying feature support.
