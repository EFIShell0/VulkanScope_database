# CapsViewer / Vulkan Hardware Database site parity audit

Reference comparison target: the public `vulkan.gpuinfo.org` frontend source tree as audited for this release.

## Navigation and aggregate coverage

- Reports -> VulkanScope `Reports`
- Devices -> `Devices`
- Core properties 1.0 / 1.1 / 1.2 / 1.3 / 1.4 -> `Properties` subfilter
- Extension properties -> `Properties > Extension properties`
- Device limits -> `Limits`
- Core features 1.0 / 1.1 / 1.2 / 1.3 / 1.4 -> `Features` subfilter
- Extension features -> `Features > Extension features`
- Linear tiling formats -> `Formats > Linear tiling`
- Optimal tiling formats -> `Formats > Optimal tiling`
- Buffer formats -> `Formats > Buffer features`
- Memory types -> `Memory > Memory type coverage`, with heaps and per-report type mappings preserved separately
- Queue families -> `Queues`, with every normalized boolean queue capability shown explicitly
- Surface formats / color spaces -> `Surface > Formats / color spaces`
- Surface present modes -> `Surface > Present modes`
- Surface transform modes -> `Surface > Transform modes`
- Surface composite alpha modes -> `Surface > Composite alpha modes`
- Surface usage flags -> `Surface > Usage flags`
- Presentation queue support -> `Surface > Presentation queues`
- Device extensions -> `Extensions`
- Instance extensions -> `Instance > Instance extensions`
- Instance layers -> `Instance > Instance layers`
- Parsed device layers -> `Instance > Device layers`
- Vulkan Profiles -> `Profiles`
- Portability subset reports -> `Portability`
- Report comparison -> `Compare`
- Per-capability device coverage -> Properties/Features `Coverage reports` drill-down opens the corresponding VulkanScope report

## Intentional semantic differences

- Missing extensions are not converted to Unsupported. They stay Unknown/not listed unless the submitted report supplies direct unsupported evidence.
- Missing memory-type data is Unknown. A memory flag combination is Unavailable only when a report actually enumerated memory types and did not contain that exact combination.
- False feature/queue capability booleans are Unsupported only when the boolean is explicitly present in normalized report data.
- Scalar zero/false-like property values remain Available unless the field itself is a support boolean.

## State palette audit

- Supported: green
- Unsupported: red
- Available: blue
- Unavailable: amber
- Unknown: neutral gray

The active `site.v0332.css` assigns these colors consistently to badges, state counts and percentage bars. Unavailable never uses the Supported green path.
