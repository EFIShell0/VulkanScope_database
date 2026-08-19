# VulkanScope Database 0.33.6

Scrollbar, filter-animation, Surface-layout, error-state and full regression-audit release.

- Replaced browser-native horizontal table scrollbars with VulkanScope-styled controls on every overflowing technical table: left/right actions, edge fades, a clickable/draggable position track, touch panning and keyboard support.
- Fixed the custom filter opening transition. The listbox and chevron now animate symmetrically when opening and closing instead of the chevron appearing instantly in its final state.
- Added automatic drop-up placement for filter menus when there is not enough viewport space below the control.
- Fixed long canonical Surface present-mode tokens overflowing their cards. Tokens wrap without abbreviation or information loss.
- Added a polished VulkanScope-styled `404.html`, reusable common 4xx/5xx static error pages, and a matching live frontend API-load error state with Reports, GitHub and Retry actions.
- Improved Worker HTTP semantics: known routes called with an unsupported method return `405 Method Not Allowed` with an accurate `Allow` header instead of a misleading 404. API responses remain JSON.
- Added defensive Worker response headers while preserving the existing CORS contract, parameterized D1 access, 2 MiB submission bound and no-IP-storage policy.
- Fixed a portrait/mobile sticky-detail-tab offset that could overlap the two-row header.
- Reduced repeated global-search CPU work by caching each report's normalized search text and applying a short input debounce.
- Re-audited CapsViewer / Vulkan Hardware Database category parity. Properties/features Core 1.0–1.4 and extension views, formats, memory, queues, Surface, instance, profiles, portability and full report comparison remain represented without changing VulkanScope's stricter Unknown/Unsupported semantics.
- VulkanScope 0.32.4/0.32.5 schema-v3 compatibility, Vulkan 1.4.360 baseline, exact-width flag handling and canonical/raw Vulkan presentation are preserved.
