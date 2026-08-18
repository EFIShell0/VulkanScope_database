# VulkanScope Database 0.33.0

- Full UI parity audit against the public Vulkan Hardware Database navigation and listing structure, while preserving VulkanScope state semantics and design language.
- Added local inline SVG icons to every primary navigation tab.
- Added Portability view for explicit VK_KHR_portability_subset reports without inferring unsupported from absence.
- Queue families now expose every normalized boolean capability as an explicit Supported/Unsupported/Unknown state instead of hiding false values.
- Surface/WSI now has dedicated Capabilities, Formats/Color spaces, Present modes, Transform modes, Composite alpha modes, Usage flags and Presentation queues subviews.
- Properties, limits, features, formats, memory, extensions, instance data and profiles use state-semantic counts/percentages consistently; Unavailable is amber everywhere and Unknown is gray.
- Report-detail Surface and Instance views now preserve state colors and expose parsed device layers.
- Core/extension property and feature aggregates now expose value distributions and per-capability report drill-downs, matching the useful device-coverage detail of the reference site without copying its unsupported inference.
- Instance aggregate view now exposes parsed device layers separately instead of leaving them only in raw report text.
- No third-party UI assets or runtime dependencies were added.
