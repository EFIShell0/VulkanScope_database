# VulkanScope Database 0.36.3

VulkanScope Database 0.36.3 adds a design-consistent technical-differences filter to Compare while preserving the VulkanScope 0.34.2 / Vulkan 1.4.360 report contract.

- `Differences only` remains available and enabled by default.
- New `Technical differences only` is also enabled by default.
- Application version/versionCode and server-authored submission timestamp are hidden only from the technical comparison view.
- Driver, Vulkan API, Android/ABI/device, memory, queue, Surface, format, extension, capability, Display/HDR and profile differences remain visible.
- Compare metrics are recalculated against the active technical field universe.
- Disabling the technical filter restores application/submission metadata comparison.
- No report schema, Worker normalizer, D1 data, submission hash or stored raw report is changed.
- Current producer/query baseline remains VulkanScope 0.34.2 · Vulkan 1.4.360.
