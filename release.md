# VulkanScope Database 0.32.1

- Expanded Memory to CapsViewer-style aggregate memory-type flag coverage, while preserving per-report heaps and memory-type mappings.
- Added Available, Unavailable and Unknown counts and percentages for exact memory type flag combinations.
- Unavailable is derived only when a report actually enumerated memory types and that exact combination is absent; reports without memory data remain Unknown.
- Added state-aware coverage colors: Supported green, Unsupported red, Available blue, Unavailable amber, Unknown gray.
- Extended the state filter to every aggregate view where the stored data supports a meaningful state distinction, including Memory, Extensions and Instance; Surface filtering now also applies beyond only surface formats.
- Extension absence remains Unknown/not listed rather than being silently reclassified as Unsupported.
- Preserved the existing VulkanScope Database visual language, raw report access and Vulkan 1.4.357 registry baseline.
