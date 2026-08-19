# VulkanScope Database project rules
- The public database contains VulkanScope technical report data only; personal identifiers, account data, authentication data, private file paths and request IP addresses are not report fields.
- Supported, unsupported, unavailable and unknown are distinct states. A missing query must never be labeled unsupported without direct runtime evidence.
- A successfully queried scalar/property is available even when its value is zero or false unless that field is itself a support boolean.
- Runtime feature booleans and explicit SUPPORTED / NOT SUPPORTED report tokens are support evidence and must preserve supported/unsupported semantics.
- Runtime-enumerated extensions are supported. An absent extension is not labeled unsupported unless the report contains explicit evidence that the extension enumeration is complete and that inference is intentionally implemented.
- Loader/instance API version, physical-device API version and driver version remain separate.
- Vulkan names, extension tokens, format names, color spaces and profile names remain canonical and are not renamed for presentation.
- Vendor presentation may add a human-readable vendor/GPU-family label, but the raw vendor ID remains visible and is the filter key.
- Every technical category present in a submitted VulkanScope report must remain accessible in the database UI, either in a dedicated aggregate view, report detail tab or raw report view. Parsed summaries must never replace or discard the original report text.
- Aggregate coverage statistics are computed only from reports actually loaded by the database and must not imply global Vulkan ecosystem coverage.
- The frontend has no third-party JavaScript, analytics, remote fonts or advertising dependencies.
- The production frontend and API use HTTPS. The Content Security Policy only permits the configured VulkanScope Worker API in addition to same-origin resources.
- Submitted payloads are size-limited and schema-validated. Existing reports are normalized on read so parser fixes apply without rewriting stored payloads.
- Frontend report fetching is concurrency-bounded to prevent avoidable memory/network spikes.
- Browser-visible static assets that materially change must use versioned filenames or an equivalent cache-busting strategy so GitHub Pages/browser caches cannot silently retain an older UI release.
- The vendor filter must show a human-readable GPU family derived from authoritative vendor identity when that family is unambiguous, while retaining the canonical raw vendor ID as the filter key. A separate GPU-model filter must expose the actual reported device name.
- Report detail navigation must remain visible even when a normalized category is empty; an empty category is shown as not reported rather than silently removing the tab.
- The frontend must be able to normalize the stored report text as a compatibility fallback when the deployed Worker normalizer is older than the frontend parser, without changing supported/unsupported/unavailable/unknown semantics.
- Report submission time displayed by the UI must come from the server-side D1 `submitted_at` value, not a client-provided clock, and must preserve an exact machine-readable timestamp while the presentation may be localized.
- Physical-device API version and loader/instance API version must be displayed as separate report metadata fields.
- Reports pagination must never render more than 50 report rows per page; sorting and filtering must be applied before pagination so page boundaries are deterministic.
- Version-like report metadata should use numeric-aware ordering where possible; ordering must never reinterpret missing or unknown technical values as supported/unsupported state.
- Aggregate state filters must be exposed on every view where the normalized data provides a meaningful supported, unsupported, available, unavailable or unknown distinction; a filter must not invent a state that the underlying report cannot justify.
- Coverage visualization is state-semantic: supported is green, unsupported is red, available is blue, unavailable is amber, and unknown is neutral gray. Unavailable or unknown percentages must never reuse the supported green treatment.
- Memory aggregate coverage is based on exact reported VkMemoryPropertyFlags combinations. A combination may be marked unavailable for a report only when that report enumerated memory types and did not contain the combination; missing memory-type data is unknown.
- Aggregate views that contain boolean queue-family capabilities must display both true and false states; false queue capabilities must not disappear from presentation.
- Surface/WSI aggregate presentation keeps capabilities, formats/color spaces, present modes, transform modes, composite-alpha modes, usage flags and presentation queues individually accessible when the report provides those fields.
- Navigation icons are local inline SVG presentation only; they must not introduce third-party assets, scripts, fonts or network dependencies, and text labels remain present for accessibility.
- VK_KHR_portability_subset absence is Unknown/not listed unless a report supplies direct unsupported evidence; the portability view must never infer unsupported solely from absence.
- Explicit state counts and percentages use the same semantic palette everywhere, including aggregate tables and report detail views: supported green, unsupported red, available blue, unavailable amber, unknown gray.

- VkMemoryType.propertyFlags must be decoded to canonical Vulkan memory-property flag names in the UI while retaining the raw numeric/hex mask. Current known bits include DEVICE_LOCAL, HOST_VISIBLE, HOST_COHERENT, HOST_CACHED, LAZILY_ALLOCATED, PROTECTED, DEVICE_COHERENT_AMD, DEVICE_UNCACHED_AMD and RDMA_CAPABLE_NV; unknown future bits remain visible as UNKNOWN_BITS_0x....
- VkMemoryHeap.flags must likewise expose canonical heap flag names while retaining raw masks; unknown bits are never discarded.
- Schema-v3 technicalReport structured memory/queue/format/surface data from VulkanScope is preferred over reparsing human-readable TXT when present; TXT parsing remains a compatibility fallback.
- Desktop navigation must not silently clip the final tab. Compact button geometry is used on wide layouts and the menu layout activates before the navigation can overflow; portrait/mobile layouts must remain usable without horizontal page overflow.

- Main navigation tabs are never clipped or hidden because of viewport width. The brand and navigation retain a deliberate gap; the tab strip is horizontally scrollable with mouse/trackpad/touch, and portrait/mobile uses a two-row header with a full-width scrollable tab strip.
- Canonical Vulkan presentation applies beyond memory: queue flags, video codec operation flags, format feature flags, surface transforms, composite-alpha flags and image-usage flags are decoded to current canonical VK_* token names while the raw mask remains visible. Unknown future bits remain explicit UNKNOWN_BITS_0x....
- Vulkan 64-bit masks must not be rounded by JavaScript Number conversion. For schema-v3 submissions whose structured JSON carries numeric 64-bit format masks, exact reportText decimal masks take precedence until the application emits those values as lossless strings; this exception overrides the general structured-data preference only for unsafe-width integer masks.

- For core property fields whose Vulkan type is unambiguous, canonical decoding also covers subgroup shader-stage flags, subgroup feature flags, sample-count flags and depth/stencil resolve-mode flags. Arbitrary numeric extension properties are not guessed into enums: their raw value remains authoritative unless the field type is explicitly mapped.

- Database release 0.33.4 is compatible with VulkanScope 0.32.4. Both the compile-header baseline and independently validated runtime query catalog are Vulkan 1.4.360; the UI/Worker must not retain the obsolete 1.4.357 validated-query label.
- Schema-v3 structured technicalReport features, detailedProperties, limits, profiles, memory, queues, formats, surface and registry coverage are authoritative when present. TXT remains a compatibility fallback and raw report text remains accessible.
- Exact-width unsigned decimal strings (for example *U64 fields) supplied by VulkanScope take precedence over lossy JavaScript numeric values; producer-supplied canonical names may be displayed while raw exact masks remain visible.
- The browser document title follows navigation state. Main views use '<Section> - VulkanScope Database' (Reports may use the bare product title); report-detail views include the GPU/report context and active detail section.
- Frontend and Worker code must not assume IPv4 address syntax. Request IP addresses are neither parsed into report data nor persisted. Cloudflare edge IPv4/IPv6 handling must remain transport-only and technical report identity must not depend on client IP.
- Database release 0.33.5 preserves VulkanScope 0.32.4/0.32.5 structured-report compatibility; UI-only application 0.32.5 changes do not alter report schema semantics.
- Primary navigation scrolling uses dedicated left/right controls plus direct touch, trackpad and wheel scrolling. Native horizontal scrollbar chrome is hidden; navigation labels must never be covered by the controls or edge fades. Arrow disabled state and edge fade visibility follow the actual scroll position.
- Filter selectors are progressively enhanced into local custom listboxes so option presentation follows the VulkanScope Database design language. The original native select remains the authoritative form state; mouse, touch and keyboard operation (Enter/Space, arrows, Home/End, Escape) must remain functional.
- The hero may link to the official VulkanScope repository, but external links use noopener/noreferrer and introduce no third-party script, font or analytics dependency.
- Report comparison must expose normalized Devices, Properties/Features, Extensions, Formats, Queue families, Memory, Surface and Profiles when the reports provide them; it must not reduce comparison to the generic capability map alone. Missing data remains Unknown/not reported.

- Technical tables with horizontal overflow must not expose browser-native scrollbar chrome as the primary control. The UI must provide design-consistent horizontal controls while retaining direct touch/trackpad scrolling and keyboard accessibility; controls must reflect actual overflow state and never cover data.
- Canonical Vulkan tokens must remain complete and readable. Long tokens may wrap but must not be silently truncated, abbreviated or ellipsized when doing so would hide technical information.
- Custom listbox opening and closing transitions must be symmetrical; DOM refresh must not recreate animated controls in their final state and bypass the opening animation.
- Frontend fatal/API-load errors and static error documents use the VulkanScope Database design language and always provide a Reports-home action plus the official VulkanScope GitHub link. API endpoints themselves remain machine-readable JSON.
- Known Worker API paths called with unsupported HTTP methods return 405 and an accurate Allow header rather than 404.
