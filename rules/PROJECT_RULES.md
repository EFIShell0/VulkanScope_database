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

- Report-detail tab and disclosure transitions are presentation-only and must not delay, mutate, or reinterpret normalized Vulkan data. Rapid interaction must not permit stale animation completion to restore an older tab.
- Disclosure controls that replace native details use semantic buttons, `aria-expanded`, keyboard focus and reduced-motion handling; touch and mouse must share the same state path.
- Queue-family presentation support is shown only from explicit submitted Surface presentation-queue evidence. Missing queue presentation evidence is Unknown, not Unsupported.
- Surface query diagnostics are displayed only when supplied by the report and remain raw/authoritative; UI never fabricates query results.

- Database release 0.33.8 may reuse the local GPU vendor artwork bundled with the VulkanScope Android application. Vendor artwork remains a presentation aid only: vendor IDs and reported GPU names remain authoritative, unknown vendors use the bundled unknown mark, and a logo must never be used to infer unsupported technical data.
- Tables that expose a report/device GPU name include a compact **Logo** column immediately adjacent to the GPU/device-name column when a report object is available. Logo cells are fixed-width, lazy-decoded local assets and must not cause horizontal text truncation or third-party network requests.
- Only explicit Turnip / third-party driver presentation text uses the red accent. The underlying driver mode/name/version remains unchanged and copyable; System Vulkan driver text and unrelated status values must not inherit this treatment.
- Public report POSTs accept `application/json` only, require the VulkanScope application identity fields expected by schema 2, and reject collection states other than complete/available. These checks supplement, not replace, payload-size, forbidden-field and schema validation.

- Database release 0.34.0 renders reported GPU model names with consistent strong emphasis in all report-backed list/table contexts; presentation styling must not alter the raw GPU name.
- Primary navigation view changes use short compositor-friendly opacity/transform transitions only. They must not animate table dimensions, delay Vulkan normalization, or allow stale transition completion to restore an older view; prefers-reduced-motion disables the transition.
- On portrait/mobile layouts with the two-row header, report-detail sticky tabs must clear the full header height and never be hidden beneath the top bar.

- Database release 0.34.0 custom listboxes render System Vulkan driver choices with strong emphasis on the reported GPU model only; system driver mode/version text stays normal weight. Turnip / third-party choices keep their explicit red-accent presentation. This is presentation-only and must not alter native select state or raw report values.

- Database release 0.34.2 requires explicit custom-listbox contrast: in System Vulkan driver choices, the reported GPU model is strong white text while the driver suffix remains muted normal-weight text in normal, hover, focus and selected states; inherited row color must not erase this distinction.

- Database release 0.34.2 presents the Compare “Differences only” option as a custom VulkanScope-styled checkbox while retaining the native checkbox as the authoritative state. The control must preserve mouse, touch, label-click and keyboard operation, expose a visible focus state, use a minimum ~44 px touch target, and honor prefers-reduced-motion.

- Database release 0.34.3 presents physical-device API, loader/instance API and equivalent Vulkan API version values with the shared `api-version-chip` presentation in every applicable aggregate/report/compare view. The underlying version string remains authoritative and must not be renamed, rounded, promoted, or inferred for styling.

- Database 0.34.5 primary-section navigation uses short compositor-only opacity/translate transitions driven by Web Animations API. Rapid navigation is token-gated so stale transitions cannot commit an older view; `prefers-reduced-motion` disables decorative motion.
- Vulkan API-version lists and maxima use numeric-aware version ordering. Lexicographic string ordering must not be used for Vulkan versions because it can misorder values such as 1.4.9 and 1.4.10.
- Database 0.34.5 is regression-audited against VulkanScope 0.32.6 schema-v3 structured reports. Queue video decode/encode/optical-flow/data-graph fields and Surface completeness/query diagnostics remain representable without inventing unsupported state.

- Android Display/HDR data present in schema-v3 `technicalReport.display` is a first-class technical category and must be accessible in both aggregate and per-report Database UI; raw report access alone is not sufficient.
- Instance/device layer extension lists carried by schema-v3 reports must remain visible and must not be discarded when normalizing layers.
- A Database-global baseline label describes the VulkanScope producer/query catalog, not an assertion about the Khronos Registry's current published release. Per-report raw registry/header metadata remains authoritative for that report.

- Database 0.34.5 Display/HDR aggregate identifies the Android device/model, not the GPU. GPU names, GPU-vendor labels and GPU logo assets must not appear in the Display/HDR aggregate view or its hidden filter state.
- Empty reported HDR type lists are presented as Unavailable in Display/HDR, not Unknown or Unsupported. Logos are presentation-only and may be shown only for HDR types explicitly reported by the submission; logo presence never implies support.
- Recognized HDR type artwork may use local assets for Dolby Vision, Dolby Vision 2, HDR10, HDR10+, HDR10+ Advanced and HDR Vivid. Unknown/unmapped HDR type strings remain escaped raw text and are never renamed or dropped.

- Database 0.34.6 uses a dedicated HDR10 asset for HDR10. HDR10 must never be synthesized by cropping, masking or relabeling the HDR10+ artwork. The supplied black HDR10 artwork is rendered on an opaque white background for dark-theme legibility.
- HDR brand artwork is presentation-only. A logo asset never creates support evidence; it may render only when the submitted report explicitly reports the corresponding HDR type.
- When the Worker receives an HTTP Origin header and ALLOWED_ORIGIN is configured to a concrete origin, mismatched browser origins are rejected. Requests without Origin remain valid so the native VulkanScope Android client and command-line diagnostics are not broken.
- Database 0.34.6 is schema-compatible with VulkanScope 0.32.7; the app's Turnip SAF picker fix does not change structured report semantics.

- Database 0.34.7 Display/HDR must not expose or apply vendor, GPU-model, or Vulkan API-version filters. Display/HDR is Android device/display metadata; only filters with direct semantic relevance to that view may affect its rows. Hidden stale filter state must never suppress Display/HDR results.


- Database 0.34.8 top-level filter custom listboxes use a compact responsive presentation and local semantic SVG iconography. The hidden native select remains authoritative; keyboard, mouse and touch behavior and supported/unsupported/available/unavailable/unknown semantics must not change for styling.
- Database 0.34.8 Display/HDR may expose submission-time ordering (Newest first / Oldest first) because it orders report rows without inferring display capability. Vendor, GPU-model and Vulkan API-version filters remain forbidden in Display/HDR, and ordering must use the server-provided `submittedAt` value with deterministic report-ID tie-breaking.


## Release 0.34.9 Compare / Portability density
- Compare and Portability may use denser presentation than general aggregate pages, but no compared capability, raw value, canonical Vulkan token, status state or portability evidence may be omitted or collapsed away solely to save space.
- Compare selector/listbox native select state remains authoritative and Differences-only remains keyboard, mouse and touch operable.
- Portability continues to treat absence of VK_KHR_portability_subset as Unknown/not listed unless direct runtime evidence justifies another state.
- Density changes are presentation-only and must be scoped to Compare/Portability so unrelated views do not regress.

## Release 0.35.0 full database audit
- Generic Vulkan scalar/property values are availability data: zero/false values remain Available unless the field is explicitly a feature/support boolean. Feature booleans retain Supported/Unsupported semantics.
- Compare reads the canonical VulkanScope schema-v2 field names `gpu.deviceType` and `vulkan.loaderInstanceApiVersion`; legacy aliases must not replace current producer fields.
- TXT compatibility normalization parses the current queue `videoCodecOperations` field and registry-coverage section instead of silently folding or dropping them.
- Worker POST body processing is byte-bounded while streaming; requests over 2 MiB are rejected before an unbounded body string is materialized.
- Worker schema checks validate required object shapes, bounded index metadata strings, application/package identity, and technicalReport schema 3 when present.
- Android Display `preferredWideGamut` is presented as the preferred wide-gamut color space reported by Android, never as measured physical-panel gamut coverage. Display/HDR remains separate from Vulkan Surface color-space support.
- The published Khronos Registry version and the VulkanScope producer/query baseline are distinct. As of this audit the public Khronos latest specification is 1.4.359 (2026-08-07); the database keeps VulkanScope's independently pinned producer/query baseline 1.4.360 labeled as such and does not call it Khronos latest.
- Frontend report-detail fetch failures must be surfaced as a visible loaded-set warning/metric; silently dropping failed reports while presenting the loaded set as complete is forbidden.
- Submission deduplication hashes a stable key-sorted JSON representation so equivalent payload objects cannot bypass deduplication merely by reordering object keys; nesting is bounded before canonicalization.


## Release 0.35.1 dominant coverage emphasis
- In coverage distributions, progress-bar fills always retain the semantic state palette for every state.
- Percentage text uses a semantic state color only when that state is the unique largest percentage within the same compared distribution.
- Non-dominant percentage text is neutral white. If the highest percentages are tied, all tied percentage labels remain neutral because no state dominates.
- State-count badges/pills are not changed by dominance styling and retain their existing semantic colors.
- Dominance styling is presentation-only; counts, denominators, percentages, filters and supported/unsupported/available/unavailable/unknown semantics are unchanged.


## Release 0.35.2 full-audit hardening
- The report index is cursor-paginated by the server-authored `(submitted_at, id)` ordering. The frontend must follow all returned index pages; an API page-size limit must never silently make older stored reports disappear from the public UI.
- TXT compatibility normalization preserves current Surface `Color-space extension` and `Format query` diagnostic lines. Structured schema-v3 remains preferred, but fallback parsing must not silently discard these diagnostics.
- Generic Surface capability/property values are availability data unless the field itself is an explicit support state. A false/zero scalar must not be reinterpreted as Unsupported. Query-diagnostic booleans are diagnostic values, not feature-support booleans.
- Compare uses plain canonical memory flag text as data. HTML presentation fragments must never be stored as Compare values or rendered as escaped technical values.
- An explicitly reported empty `display.hdrTypes` list is Unavailable in Compare as it is in Display/HDR; it is not Unknown and never implies Unsupported.
- Submission privacy validation operates on parsed JSON field names, recursively rejects sensitive personal/account/authentication identifiers, and does not reject harmless technical report text merely because it mentions a sensitive-looking phrase. GPU `deviceId` remains the Vulkan device identifier field and is not treated as a personal device identifier.
- Malformed stored JSON must fail as an explicit server error without leaking stack details or corrupting neighboring report responses.
- Worker normalizer version 9 corresponds to the 0.35.2 TXT compatibility behavior.


## Release 0.35.3 dominant coverage background containment
- Coverage progress fills always retain their semantic state color.
- A non-dominant coverage state must not paint its semantic background outside the progress-bar fill; its surrounding coverage container remains transparent/neutral and its percentage label remains neutral white.
- Only the unique dominant percentage in the same distribution may extend semantic emphasis to the percentage text and the surrounding coverage container.
- If the top percentage is tied, no tied state is dominant and all tied coverage containers/percentage labels remain neutral outside their progress fills.
- State-count badges/pills are independent of coverage dominance and must remain unchanged.
- This is presentation-only; counts, percentages, denominators, filters and capability-state semantics must not change.

## Release 0.35.4 Cloudflare account isolation
- Production Wrangler configuration is pinned to VulkanScope Cloudflare account `ccf3de9d3f2a4394af2fb7be7fd5bbf4`; it must not silently deploy to a different Cloudflare account.
- Production D1 binding remains `DB` and is pinned to database `vulkanscope-database` with UUID `8fa65ef5-701d-4110-993d-87381f9763ab`.
- The project-local Wrangler auth profile is named `vulkanscope`. Authentication state itself remains local and must never be committed to the repository.
- npm production deploy, migration, migration-list and D1 diagnostic commands fail closed when the active Wrangler account cannot be verified as the pinned VulkanScope account.
- Local dependencies, Wrangler state, environment/secret files, logs, caches and generated build output must remain excluded from Git through the repository `.gitignore`.
- Account-isolation hardening must not change report schema semantics, stored report contents, public frontend capability-state semantics or D1 report data.


## Release 0.35.5 Windows account-verifier reliability
- The fail-closed account guard must work on Windows without treating a valid activated `vulkanscope` profile as unverifiable solely because `.cmd` execution through Node child-process APIs fails.
- Project-local pinned Wrangler is the preferred verifier executable; JSON `whoami` is preferred and exact account-ID text fallback is allowed only as a compatibility path.
- Debug logging must not contaminate machine-readable identity verification.
- Any missing, unreadable or mismatched account identity still blocks production deploy, migrations, migration listing and D1 diagnostics.


## Release 0.35.6 Vulkan brand-surface parity
- The database shell follows the same chromatic dark-surface quality model as OpenGLESScope Database, but all product-brand accents and interactive chrome are derived from Vulkan official red `#A41E22`; OpenGL ES magenta must not be copied into VulkanScope.
- Background ambient glow, hero surfaces, active/hovered navigation and detail tabs, search focus, filter controls, scroll controls, pagination and action surfaces use restrained Vulkan-red-derived tones rather than neutral gray-only chrome.
- Product-brand theming must never overwrite technical state semantics: supported stays green, unsupported stays red, available stays blue, unavailable stays amber and unknown stays neutral gray.
- Release 0.35.3 dominant-coverage containment remains authoritative; brand theming must not alter coverage denominators, dominance, state colors or percentage meaning.
- Browser-visible changed CSS/JS uses versioned filenames so GitHub Pages and browser caches cannot retain the previous neutral theme.


## Release 0.35.7 producer/database full audit
- VulkanScope 0.33.7 schema-v2 + schema-v3 submissions are the current producer contract. New submissions with schema-v3 data are cross-checked so primary GPU name/vendor/device ID, device API, driver mode/version, loader/instance API and registry/header/report-baseline metadata cannot disagree with the top-level index metadata.
- Current VulkanScope report text must identify the VulkanScope application/version/versionCode/package and contain the core registry, instance, profile, device, feature, limit, format and Surface sections. Report text remains authoritative raw evidence and is never discarded.
- The current published Khronos specification and VulkanScope staging/query baseline are separate facts. As of this audit, the published Registry specification is Vulkan 1.4.359 dated 2026-08-07; VulkanScope's independently pinned producer/query staging baseline remains 1.4.360 and must not be labeled as the published latest specification.
- Frontend API reads are bounded to 4 MiB and 20 seconds. Cursor pagination rejects repeated cursors and report-detail fetching remains concurrency-bounded to four workers.
- Aggregate property, limit and feature coverage uses every loaded report in the denominator. If a capability exists in the loaded universe but is absent from a particular loaded report, that report contributes Unknown, never Unsupported and never disappears from the denominator.
- Format aggregate coverage likewise includes Unknown for a loaded report that does not contain a format row in the selected format set.
- Display/HDR prefers the producer's explicit `hdrCapabilityStatus`. A genuinely missing HDR field is Unknown; an explicitly reported empty `hdrTypes` list is Unavailable. Unsupported is never inferred from an empty HDR list.
- Display/HDR state filtering may expose Supported/Unsupported for explicit wide-gamut support evidence and Available/Unavailable/Unknown for display/HDR availability evidence, but vendor, GPU-model and Vulkan API filters remain inapplicable to the Display/HDR view.
- API responses retain CORS/nosniff/no-referrer/permissions protections and additionally send CORP/COOP plus a restrictive API CSP. Native Android submissions without an Origin header remain supported.
- Worker normalizer version 10 corresponds to the 0.35.7 validation and TXT/structured compatibility behavior.
- No D1 migration is required for 0.35.7; existing payloads remain normalized on read.

## Release 0.35.8 exact Properties / Limits semantics
- For schema-v3 reports, the selected device's `technicalReport.devices[].detailedProperties` is the authoritative Properties dataset and `technicalReport.devices[].limits` is the authoritative Limits dataset.
- DEVICE metadata, Surface metadata, formats, profiles, features, extensions and other compatibility-normalizer rows must never inflate the Properties count.
- A detailed-property section must not become a Limit merely because its section label contains `Limits` or `Sparse Properties`; only the producer's structured `limits` array is authoritative for schema-v3.
- TXT compatibility fallback keeps bracketed non-feature query-result rows as Properties and rows under the literal `LIMITS` heading as Limits.
- Report-detail Properties and Limits tab counts must equal the lengths of their corresponding authoritative per-report arrays when schema-v3 data is present.
- Aggregate Properties and Limits views consume those same separated arrays. Loaded reports missing a property/limit contribute Unknown to that capability's denominator; they are never silently dropped or labeled Unsupported.
- Raw report text and the broader compatibility capability collection remain available for raw/Compare compatibility, but neither is allowed to redefine Properties/Limit counts when structured schema-v3 arrays exist.
- Worker normalizer version 11 corresponds to the 0.35.8 separated Properties/Limits semantics.
- No D1 migration is required for 0.35.8; existing payloads are corrected on read without rewriting stored reports.



## Release 0.35.9 Display & HDR / ABI / home-metric parity
- The primary and report-detail navigation label is **Display & HDR**. Internal normalized field names remain unchanged; presentation naming must not alter Vulkan evidence semantics.
- Reports show the installed application ABI as the primary Platform / ABI value and list every producer-reported `supportedDeviceAbis` value beneath it. Missing ABI evidence is shown as Unknown and is never inferred from GPU identity.
- Android luminance values (`minLuminance`, `averageLuminance`, `maxLuminance`) are displayed with `cd/m²` when the reported value is numeric. Existing `cd/m2`, `cd/m^2`, or `cd/m²` text is normalized for presentation without changing stored report evidence.
- The home metrics expose the current VulkanScope producer/query baseline and the compatible producer contract as separate cards, matching the information hierarchy used by OpenGLESScope Database.
- VulkanScope 0.33.10 remains the current producer reference for Database 0.35.9. Compatibility presentation begins at VulkanScope 0.32.4 for the schema-2 / technical-report-3 contract already preserved by the Database compatibility path.
- No logo, ABI string, HDR value, or presentation label may be used to infer Vulkan feature support.
- Release assets that change JavaScript behavior use cache-busted `app.v0359.js`; the unchanged stylesheet remains `site.v0357.css`.
- No D1 migration or stored-payload rewrite is required for 0.35.9.


## Release 0.36.0 luminance-unit typography parity

- Display & HDR luminance evidence must preserve the producer-reported numeric/text value and must not infer or alter capability state.
- When a luminance value is numeric or already carries a recognized `cd/m2`, `cd/m^2`, or `cd/m²` suffix, presentation normalizes the visible unit to `cd/m²`.
- The `cd/m²` unit must use the same visual hierarchy as OpenGLESScope Database: dedicated `.luminance-unit`, `white-space: nowrap`, `color: var(--muted)`, and `font-size: .92em`; the numeric value remains normal primary table/detail text.
- Aggregate Display & HDR and report-detail Display & HDR must use the same luminance typography.
- Release assets that change JavaScript and CSS use cache-busted `app.v0360.js` and `site.v0360.css`.
- No D1 migration or stored-payload rewrite is required for 0.36.0.

## Release 0.36.2 VulkanScope 0.34.2 complete-report parity
- Database version is 0.36.2.
- Current producer/query baseline is VulkanScope 0.34.2 with Vulkan 1.4.360.
- Current published Khronos Vulkan specification metadata is Vulkan 1.4.360 dated 2026-08-14.
- Schema 2 / technical report 3 remains the accepted complete-report contract; VulkanScope 0.34.2 must not be rejected because of its application version.
- Structured technicalReport `devices[].detailedProperties` is authoritative for generic extension/property values, including Host Image Copy source/destination layout arrays.
- The frontend must expose structured detailed properties in report Properties, relevant aggregate/compare paths and Raw report without extension-specific field whitelists that could silently drop new validated fields.
- Features, limits, memory, queues, formats, Surface/WSI, Display & HDR, device/instance extensions, layers, profiles, registry provenance and raw report text remain independently accessible.
- Database normalization must preserve Unknown, Unsupported, Unavailable and Not applicable distinctions and must not infer missing capability evidence from GPU/device/vendor identity.

## Release 0.36.2 Host Image Copy promoted-core comparison parity
- Compare normalization treats the Vulkan 1.4 Host Image Copy property family as the promoted equivalent of VkPhysicalDeviceHostImageCopyPropertiesEXT without rewriting stored raw report provenance.
- Core 1.4 copySrcLayoutCount, pCopySrcLayouts or legacy copySrcLayouts, copyDstLayoutCount, pCopyDstLayouts or legacy copyDstLayouts, optimalTilingLayoutUUID and identicalMemoryTypeRequirements compare against the corresponding extension-structure fields under one canonical compare identity.
- Existing 0.34.1 reports using copySrcLayouts/copyDstLayouts and 0.34.2+ reports using canonical pCopySrcLayouts/pCopyDstLayouts must compare against older VK_EXT_host_image_copy reports as reported values, not as Not reported.
- The compare alias is presentation/normalization only; raw TXT, stored payloads, detail provenance and source sections remain unchanged.
- Unavailable legacy pointer placeholders remain unavailable evidence and must not be converted into supported or available values.


## Release 0.36.3 technical-differences compare filter
- Compare keeps `Differences only` and adds a second, independently toggleable `Technical differences only` control using the existing compare-toggle visual language.
- `Technical differences only` is enabled by default and removes report-generation metadata differences that do not describe Vulkan, Android platform, device, driver, Surface, memory, queue, format, extension, feature/property, Display/HDR or profile capability state.
- VulkanScope application version/versionCode and server-authored submission timestamp are metadata and are excluded only from the technical Compare view; their stored/raw report values remain unchanged and remain visible when the technical filter is disabled.
- Driver version/mode, Vulkan API versions, Android/ABI/device identity, memory budget, Surface extent and all capability/query evidence remain technical and must never be hidden by this filter.
- Filtering is presentation-only. It must not mutate normalized reports, D1 payloads, support/availability semantics, promoted aliases, raw report text or submission hashes.
- Compare summary field, difference and section counts must reflect the active technical filter so the displayed metrics describe the same visible universe as the tables.


## Release 0.36.5 VulkanScope 0.35.1 complete-report contract
- Database version is 0.36.5 and remains independent from VulkanScope application versioning.
- Current producer/query baseline is VulkanScope 0.35.1 / versionCode 352 with Vulkan 1.4.360.
- Compatible producer versions must use canonical VulkanScope 0.x semantic version form and remain at or above the declared VulkanScope 0.32.4 schema-2 / technical-report-3 floor.
- VulkanScope 0.35.1 must carry versionCode 352. A mismatched current producer identity is rejected fail-closed.
- Android security-patch evidence must use canonical `YYYY-MM-DD` form.
- Top-level application ABI and supported-device ABI evidence must exactly agree with technicalReport ABI evidence; contradictory duplicate evidence is invalid and must not be silently normalized.
- Submission schema 2 and technicalReport schema 3 remain unchanged; detailed properties, limits, formats, memory, queues, Surface/WSI, Display/HDR, extensions, features, profiles, registry provenance and raw report evidence remain accessible.
- Published Vulkan specification metadata remains Vulkan 1.4.360 dated 2026-08-14.
- Production Worker compatibility date is 2026-08-24.
- Browser-visible JavaScript metadata changes use cache-busted `app.v0364.js`; unchanged CSS remains `site.v0362.css`.
- No D1 migration, stored-payload rewrite, report-hash rewrite or capability inference is permitted for this release.
## Release 0.36.5 Cloudflare compatibility-date deploy correctness
- Database version is 0.36.5.
- `worker/wrangler.jsonc` compatibility_date must never be later than the date accepted by the Cloudflare Workers API at deployment time.
- Local timezone rollover must not be used to advance compatibility_date before Cloudflare accepts that date.
- When the local calendar is ahead of Cloudflare/API UTC acceptance, use the latest non-future accepted compatibility date and update it later only after deployment validation.
- Release verification must fail if compatibility_date is the known rejected future date for the audited deployment window.

## Release 0.37.0 VulkanScope 0.41.0 trends and permalink requirements
- Database version is 0.37.0 and remains independent from VulkanScope application versioning.
- Current producer/query baseline is VulkanScope 0.41.0 / versionCode 410 with Vulkan 1.4.360. Compatible producer floor remains VulkanScope 0.32.4+ with schema 2 / technicalReport 3.
- VulkanScope 0.41.0 must carry versionCode 410. Existing 0.35.1 / 352 identity validation remains enforced for that historical release.
- Submission schema 2, technicalReport schema 3, stable canonical hashing and existing D1 stored payloads remain unchanged. No D1 migration or stored-report rewrite is required.
- Trends are computed from the bounded set of reports successfully loaded by the frontend. Percentages are labeled loaded-submission share and never market/device/vendor share.
- Extension trend counts mean an exact extension token was enumerated in a loaded report. Absence from a report must never be labeled Unsupported.
- Trend UI bounds high-cardinality presentation: at most 25 rows per GPU/vendor/driver/API table and the top 50 exact enumerated extension tokens. This is a derived summary and never truncates canonical report data.
- Report permalinks accept only lowercase 64-hex report ids that already exist in the loaded report map. Detail-tab names are allow-listed.
- Compare permalinks accept exactly two valid loaded report ids. URL parameters never become HTML without existing escaping/safe value handling.
- Browser sharing uses the Web Share API when available and clipboard fallback otherwise. No third-party share, analytics or QR service is loaded.
- Frontend compare remains the existing normalized all-category comparison and URL sharing must not alter compare semantics or report payloads.
- Production API remains HTTPS-only with the existing same-origin allow-list, bounded 2 MiB request body, prepared/bound D1 statements and privacy-key rejection.
- Cloudflare observability is enabled with bounded sampling; no report payload or sensitive identifier is intentionally emitted to custom application logs.
- Worker compatibility date remains 2026-08-23 because it is the last deployment-verified non-future date in this project history; it may advance only after Cloudflare accepts a newer date.
- Browser-visible JavaScript is cache-busted as app.v0370.js. Existing site.v0362.css remains unchanged.
- Wrangler is pinned to 4.125.0 for the 0.37.0 release.

## Release 0.37.1 queue, Vulkan Video and query-state semantics
- Database version is 0.37.1 and remains independent from VulkanScope application versioning.
- Current producer/query baseline is VulkanScope 0.41.3 / versionCode 413 with Vulkan 1.4.360. Compatible producer floor remains VulkanScope 0.32.4+ with schema 2 / technicalReport 3.
- `VkQueueFlags == 0` must not be rendered as a fabricated generic `VK_NONE`; it is displayed as zero with an explicit no-queue-capability-bits description.
- Queue capability booleans such as Graphics, Compute, Transfer, Sparse, Protected, Video Decode, Video Encode, Optical Flow and Data Graph are direct queue-flag evidence and may be rendered Supported/Unsupported when their runtime boolean evidence is present.
- `VkQueueFamilyVideoPropertiesKHR::videoCodecOperations` requires separate query state. Successfully queried zero is `VK_VIDEO_CODEC_OPERATION_NONE_KHR`; absent `VK_KHR_video_queue` is Not applicable; failed/missing query evidence is Unavailable or Unknown.
- Missing video-codec query evidence must never be converted into zero, `VK_VIDEO_CODEC_OPERATION_NONE_KHR`, or Unsupported.
- Generic Properties and Limits availability is query availability, not feature support. A reported boolean property value of false may have Query available state and must not be visually presented as Supported/Unsupported unless that field is explicitly a capability-support boolean.
- Structured technicalReport queue evidence is authoritative for schema-v3 queue query-state fields. Compatibility fallbacks for older reports must preserve uncertainty rather than infer support.
- Worker normalizer version 14 corresponds to the 0.37.1 queue/video/query-state semantics.
- No D1 migration, stored-payload rewrite, report-hash rewrite or schema change is required.

## Release 0.38.0 statistics / hash routing / VulkanScope 0.41.4 requirements
- Database version is 0.38.0 and remains independent from VulkanScope application versioning.
- Current producer/query baseline is VulkanScope 0.41.4 / versionCode 414 with Vulkan 1.4.360. Compatible producer floor remains VulkanScope 0.32.4+ with submission schema 2 / technicalReport 3. Existing fail-closed identity rules for historical current-producer releases remain preserved.
- Submission schema 2, technicalReport schema 3, canonical report hashing and the existing D1 stored payloads remain unchanged. No D1 migration, stored-payload rewrite or report-hash rewrite is required.
- `report.schema.json` must describe the same complete-report contract enforced by the Worker: schema-2 submissions require a `technicalReport` object with technicalReport schemaVersion 3. A payload that the published JSON Schema accepts must not be rejected merely because the schema omitted this already-required complete-report member.
- Worker normalizer version 15 corresponds to the 0.38.0 VulkanScope 0.41.4 queue/video validation and presentation contract.
- VulkanScope 0.41.4 queue-family Vulkan Video query states are fail-closed: `available` may carry a numeric mask including genuine zero; `unavailable`, `not_applicable` and `unknown` must carry null numeric operation fields and must never be normalized into zero or Unsupported.
- VulkanScope 0.41.4 device-extension enumeration, extended feature/property query and Vulkan 1.4 query status/reason evidence must be preserved as first-class report diagnostics. Current-producer status tokens are fail-closed to `available`, `incomplete`, `unavailable`, `not_applicable` or `unknown`; reasons remain bounded text. These diagnostics must be visible in report detail and comparable without being reclassified as feature support.
- Every primary frontend view must have a canonical hash route. `trends` is presented canonically as `#statistics`; internal implementation names must not leak into new public URLs.
- Report-detail canonical routes use `#reports/<lowercase-64-hex-id>/<allow-listed-section>`. Report ids must already exist in the loaded report map. User-controlled route segments never become unescaped HTML.
- Two-report comparison canonical routes use exactly `#compare/<loaded-id-1>/<loaded-id-2>`. Browser back/forward and manual valid hash navigation must restore the corresponding view.
- Legacy `?view=`, `?report=&tab=` and `?compare=` links may be accepted only as compatibility inputs and must canonicalize to the hash form; newly generated links must use the canonical hash form.
- Statistics are computed only from successfully loaded reports matching the active frontend filters. Percentages must be labeled loaded-submission share and must never be described as global Vulkan, hardware, GPU, vendor, driver or market share.
- Donut/pie distribution charts are permitted only for mutually exclusive dimensions. Overlapping extension membership must remain a frequency/ranking table and must not be shown as slices of one whole.
- High-cardinality donut presentation is bounded by retaining leading categories and combining the remaining loaded-report counts into an explicit `Other` slice. This is presentation-only and must not truncate canonical reports or alter aggregate totals.
- Distribution graphics must use local first-party SVG/CSS only. No third-party JavaScript chart library, remote font, analytics, ad or chart-generation service is permitted.
- Static HTTP error pages must reference an asset that exists in the same release package; release verification must fail on broken local stylesheet/script references.
- Browser-visible JS/CSS/config changes use cache-busted `app.v0380.js`, `site.v0380.css` and `config.js?v=0380`.
- Worker compatibility date remains 2026-08-23 because it is the last project deployment-verified date; advance it only after a real Cloudflare deploy/test accepts and validates a newer date.
- Wrangler remains pinned to 4.125.0 for 0.38.0 unless a newer version is separately verified before release.


## Release 0.39.0 filter architecture and interactive statistics requirements
- Database version is 0.39.0 and remains independent from VulkanScope application versioning. Current producer/query baseline remains VulkanScope 0.41.4 / versionCode 414 with Vulkan 1.4.360; submission schema 2, technicalReport schema 3 and Worker normalizer 15 remain unchanged.
- Filtering is presentation-only. It must not mutate stored payloads, canonical report hashing, D1 rows, normalized evidence, support/availability semantics or raw reports.
- Cohort filters are view-scoped. A hidden filter must not continue suppressing rows in a view where that filter is not applicable.
- Global report-cohort filters may include exact GPU vendor, GPU model, device Vulkan API, loader/instance API where relevant, driver mode, driver version, exact enumerated device-extension cohort, physical-device type, Android version/device model, application ABI/version and bounded submission-age ranges.
- The exact device-extension cohort filter means that token was enumerated in the report. Absence remains Unknown/not listed and must never be rewritten as Unsupported.
- Display & HDR must never apply GPU vendor, GPU model, device/loader Vulkan API, driver, extension, Vulkan device type, ABI, application version or generic Vulkan capability-state filters. Display & HDR may filter only directly reported display/device evidence such as Android version/device model, submission age/order, HDR availability/type, wide-gamut state, preferred wide-gamut color space, resolution, refresh rate and display mode. Global search on this view is likewise restricted to Android device/display evidence and must not match hidden GPU/driver/Vulkan fields.
- Properties and Limits expose query-state filtering only: Query available, Query unavailable and Unknown/not reported. They must not expose generic Supported/Unsupported filters or columns because boolean false/zero property values are valid queried values, not feature-support conclusions.
- Queue generic Supported/Unsupported/Unknown filtering is enabled only after a concrete queue capability is selected. The unscoped All-capabilities view must not use an “any field matches” state filter.
- Surface generic state filtering is enabled only for a concrete Surface subgroup. Each subgroup uses its own meaningful state vocabulary and may expose an exact subgroup value/token filter; the unscoped All-surface view must not apply one mixed generic state filter.
- Properties and Limits may filter by value behavior: varying, uniform where reported, or missing from at least one loaded report. Missing evidence remains Unknown.
- Features, Formats, Extensions and Profiles may filter by coverage computed over every filtered loaded report. Coverage filters must use the same denominator and Unknown accounting as the visible aggregate rows.
- Format feature-bit filtering must use canonical VkFormatFeatureFlags2 tokens without converting 64-bit masks through unsafe JavaScript Number precision.
- Format subgroup filtering must preserve an explicitly reported zero feature mask as direct evidence: zero means no bits in that queried mask, not Missing/Unknown. When a required format-feature bit is selected, Supported/Unsupported counts describe that exact bit; absent or unavailable masks remain Unknown and must not be converted to zero.
- Memory flag filtering must use exact canonical memory-property or memory-heap flag evidence. Memory-type combination absence is Unavailable only when that report successfully enumerated memory types; reports without memory data remain Unknown.
- Queue filters may include exact queue-family index, canonical VkQueueFlagBits, presentation support state, Vulkan Video query state, exact successfully queried Vulkan Video codec-operation bits and minimum queue count. Missing/unavailable/not-applicable video query evidence must never match a codec-operation token filter.
- Extension and instance-extension namespace filters distinguish KHR, EXT and vendor/other namespaces without inferring support from prefixes.
- Compare may filter visible normalized differences by exact section and text without modifying either report or the underlying comparison universe used outside the filter.
- A visible Clear filters action clears both applicable cohort filters and view-local filters and restores default sorting/grouping for the active view. Non-default subgroup selections themselves count as active view-local filtering and must make Clear filters available.
- Statistics donut charts are limited to mutually exclusive per-report dimensions and use only the currently filtered loaded submissions. Extension membership remains an overlapping frequency ranking, never a donut/pie whole.
- Statistics donuts are locally rendered SVG/CSS, keyboard accessible, expose exact counts and filtered-submission percentages, support exact slice-to-filter interaction, and group high-cardinality trailing categories into an explicit Other slice without changing totals.
- Interactive donut slices and equivalent legend controls expose active filter state accessibly (for example `aria-pressed`) and selecting the already-active exact slice clears that cohort filter without changing report data.
- Statistics must clearly state that all percentages are filtered/loaded-submission shares, not Vulkan ecosystem, market, hardware, GPU, vendor or driver share.
- Extension statistics may be filtered independently by device/instance/both scope, namespace, minimum filtered-submission enumeration coverage and exact text search; absence from a report remains Unknown/not listed.
- Browser-visible JS/CSS/config changes use cache-busted `app.v0390.js`, `site.v0390.css` and `config.js?v=0390`.
- Worker compatibility date remains the last deployment-verified project date, 2026-08-23. No compatibility-date advance, Wrangler upgrade, schema migration, D1 migration or normalizer bump is implied by this frontend/filter release.

## Release 0.39.1 VulkanScope 0.41.5 compatibility hardening requirements
- Database version is 0.39.1 and remains independent from VulkanScope application versioning. Current producer/query baseline is VulkanScope 0.41.5 / versionCode 415 with Vulkan 1.4.360.
- Compatible producer floor remains VulkanScope 0.32.4+ with submission schema 2 / technicalReport 3. Normalizer remains 15 because this release changes validation range/metadata, not normalized output semantics.
- The strict query-diagnostic and queue/Vulkan Video contract introduced for VulkanScope 0.41.4 applies to every compatible producer version at 0.41.4 or newer. It must never be guarded by equality to one exact current version string.
- For 0.41.4+ producers, deviceExtensionStatus, extendedQueryStatus and vulkan14Status remain fail-closed to available/incomplete/unavailable/not_applicable/unknown with bounded reasons.
- For 0.41.4+ producers, queue videoCodecQueryStatus remains fail-closed to available/unavailable/not_applicable/unknown. Available may contain a genuine numeric zero mask; every non-available state requires null numeric mask fields.
- Current producer identity requires VulkanScope 0.41.5 to use versionCode 415. Historical 0.41.4/414, 0.41.3/413 and other schema-compatible supported producers remain accepted under their existing identity rules.
- No D1 migration, report-id/hash rewrite, stored-payload rewrite, schema migration, automatic upload, analytics or capability inference is introduced.
- The complete 0.39.0 view-scoped filters, interactive statistics, canonical hash routes, accessibility and responsive-design contracts remain unchanged.
- Browser-visible producer metadata changes use cache-busted `app.v0391.js` and `config.js?v=0391`; unchanged CSS may remain `site.v0390.css`.
- Worker compatibility date remains the last deployment-verified project date until a real deployment validates a newer date.



## Release 0.39.2 CI checkout and Pages artifact hygiene requirements

- A normal Git source checkout may contain repository-owned top-level `.git` metadata; source verification must not misclassify that checkout metadata as a shipped release artifact.
- The deployable GitHub Pages artifact must be staged from an explicit public allow-list and must never contain `.git`, `.github`, `worker`, `tools`, `rules`, build caches, local dependencies, native binaries, or other repository-only material.
- Source-tree auditing and staged Pages-artifact auditing are separate release gates. The staged artifact audit remains fail-closed for forbidden VCS/build/development material.
- GitHub Pages deployment must upload the staged `_site` tree, not the repository root.
- Every local stylesheet/script/image reference in staged HTML must resolve inside that staged artifact.
- Database schema, D1 data, report IDs, normalizer semantics, producer validation, filter/statistics semantics, and VulkanScope 0.41.5 compatibility are unchanged by this CI/deployment-hygiene patch.


## Release 0.39.3 GitHub Actions / source-audit hardening requirements
- Database version is 0.39.3; data/schema/normalizer/producer semantics remain unchanged from 0.39.2.
- Source auditing prunes repository-owned top-level `.git` before traversal and must never emit artifact errors for normal checkout metadata. Nested `.git` remains forbidden.
- CI invokes the audit with explicit `--source-tree .` and logs `--version` before the audit so stale scripts are diagnosable.
- Pages deployment remains allow-list staged to `_site`, and artifact audit remains fail-closed for VCS/development/build content.
- GitHub Actions use current verified major releases for August 2026: checkout v7, setup-python v7, configure-pages v6, upload-pages-artifact v5 and deploy-pages v5.
- `persist-credentials: false` is used for checkout; Pages/id-token write permission is restricted to the deploy job.
- `.nojekyll` is intentionally included through upload-pages-artifact v5 `include-hidden-files: true`; no other source dotfiles are staged.
- Source audit requires `pages.yml` to be the only workflow YAML under `.github/workflows`; stale deployment workflows are forbidden.
- 0.39.3 distribution archive entries start at repository root so an in-place extraction replaces current `.github` and `tools` files rather than creating a nested version directory.

## Release 0.39.4 tracked-source audit / repository repair requirements
- Database version is 0.39.4; data/schema/normalizer/producer semantics remain unchanged from 0.39.3.
- In a Git checkout, source packaging hygiene is derived from Git-tracked paths (`git ls-files`) rather than recursive traversal of repository-owned `.git` internals.
- Root `.git` metadata is never release content. Nested `.git` entries, `.git` symlinks and tracked VCS metadata remain invalid.
- Every normal audit invocation identifies itself as VulkanScope Database audit tool 0.39.4 in CI logs.
- `.github/workflows/pages.yml` must exactly match `tools/pages.workflow.yml`; additional workflow files are stale and invalid.
- `tools/repair_repository.py --apply` must be able to replace the hidden workflow directory and remove stale `assets/app.v*.js` versions left by in-place ZIP extraction while preserving `.git`.
- Exactly one current versioned frontend app JavaScript asset is allowed in the source tree.
- GitHub Pages staging copies an explicit public-asset allow-list and generated JSON only; it never copies the entire source assets directory blindly.
- Pages artifact validation rejects stale/unexpected assets even when their extension would otherwise be allowed.
- Existing VulkanScope 0.41.5 / Vulkan 1.4.360, schema 2 / technicalReport 3, normalizer 15 and D1/report identity semantics remain unchanged.

## Release 0.39.5 cross-producer comparison / VulkanScope 0.41.7 requirements
- Database release identity is 0.39.5 and the current producer/query baseline is VulkanScope 0.41.7 / versionCode 417 with Vulkan 1.4.360; schema 2, technicalReport 3, normalizer 15, compatibility floor 0.32.4+ and D1 storage remain unchanged.
- Compare must expose cross-producer comparisons when VulkanScope version or versionCode differs. One-sided fields must not be presented as direct driver-regression evidence because collector/query coverage and evaluator behavior may differ between producers.
- Compare must provide a presentation-only `Common evidence only` filter that restricts visible rows to keys present in both reports without rewriting, deleting or reclassifying stored evidence.
- Canonical profile comparison uses the normalized `profiles` collection when available. Legacy `VULKAN PROFILES` capability rows are fallback input only and must not create a second duplicate compare section.
- Profile identity is the canonical profile name; revision belongs to the compared value. Different profile revisions must be called out because results evaluated against different profile definitions are not direct driver-regression evidence.
- `Unknown`, `Unavailable`, `Unsupported`, `Supported` and query-availability semantics remain distinct. Compare filtering must never convert one-sided or missing evidence into unsupported capability.
- Browser-visible JavaScript changes require a new cache-busted `app.v0395.js`; Pages staging remains explicit allow-list only.
- VulkanScope 0.41.7 reports remain schema-compatible and 0.41.4+ strict query/queue fail-closed validation continues to apply to all future compatible producers.


## Release 0.39.6 Image Format Properties2 tuple-state / VulkanScope 0.41.8 requirements
- Database release identity is 0.39.6 and the current producer/query baseline is VulkanScope 0.41.8 / versionCode 418 with Vulkan 1.4.360; schema 2, technicalReport 3, normalizer 15, compatibility floor 0.32.4+ and D1 storage remain unchanged.
- Image Format Properties2 tuple values reported as `Unsupported: VK_ERROR_FORMAT_NOT_SUPPORTED` are direct Unsupported capability evidence in Compare while remaining a successfully completed query for aggregate Properties query-coverage accounting.
- Image Format Properties2 tuple values beginning `Unavailable: VkResult=` remain Unavailable. They must never be converted to Unsupported.
- `Unknown / Not reported` is reserved for a tuple not present in that submission; a concrete negative tuple result must not collapse into missing evidence.
- Historical successful Image Format Properties2 rows compare under the same canonical tuple key against 0.41.8 negative rows, so AVAILABLE -> UNSUPPORTED/UNAVAILABLE is visible without rewriting stored payloads.
- Worker validation for 0.41.8+ rejects fabricated Image Format Properties2 `Unsupported:` text that is not the exact `VK_ERROR_FORMAT_NOT_SUPPORTED` result form and rejects malformed tuple-level `Unavailable:` result strings.
- Browser-visible JavaScript changes use cache-busted `app.v0396.js`. Pages staging remains explicit allow-list only.
- No D1 migration, stored-report rewrite, report-hash rewrite or capability inference is permitted.


## Release 0.39.7 Image Format Properties2 query-outcome separation / VulkanScope 0.41.9 requirements
- Database release identity is 0.39.7 and current producer/query baseline is VulkanScope 0.41.9 / versionCode 419 with Vulkan 1.4.360.
- VulkanScope 0.41.9 successful Image Format Properties2 property payloads remain normal detailed-property evidence. Its non-success tuple outcomes are consumed from the dedicated bounded `technicalReport.devices[].imageFormatQueryResults` dataset and must not be inserted into Properties/Limit property counts.
- Dedicated tuple results preserve canonical tuple identity, semantic state and exact numeric VkResult. `unsupported` is valid only for `VK_ERROR_FORMAT_NOT_SUPPORTED` (-11); other non-zero results are `unavailable`; duplicate tuple names, success code 0 or fabricated statuses are rejected for 0.41.9+ producers.
- Compare merges historical successful Image Format Properties2 rows and the separate 0.41.9 non-success tuple dataset under the same canonical tuple identity, so AVAILABLE ↔ UNSUPPORTED/UNAVAILABLE remains directly comparable without rewriting stored reports.
- Report detail Formats exposes non-success tuple outcomes separately and explicitly states that they are excluded from Properties & Limits totals.
- Historical 0.41.8 embedded negative tuple rows remain readable and valid under their historical producer contract.
- Filtering, report hashing, D1 storage, normalizer version 15, schema 2 / technicalReport 3, compatibility floor 0.32.4+, privacy/security and Vulkan 1.4.360 semantics remain unchanged.

## Release 0.39.8 Image Format Properties2 complete tuple-state / VulkanScope 0.41.10 requirements
- Database release identity is 0.39.8 and the current producer/query baseline is VulkanScope 0.41.10 / versionCode 420 with Vulkan 1.4.360; schema 2, technicalReport 3, normalizer 15, compatibility floor 0.32.4+ and D1 storage remain unchanged.
- VulkanScope 0.41.10 `technicalReport.devices[].imageFormatQueryResults` is a bounded complete state ledger for every scheduled Image Format Properties2 format/tiling tuple and its base, OPAQUE_FD and ANDROID_HARDWARE_BUFFER variants. The ledger remains separate from Properties & Limits totals.
- `available` requires `VkResult=0` and a matching successful full `detailedProperties` Image Format Properties2 payload. `unsupported` is valid only for `VK_ERROR_FORMAT_NOT_SUPPORTED` (-11). Another non-zero `VkResult` is `unavailable`.
- An external-handle variant may be `not_applicable` only when its prerequisite device extension was not enumerated. Its `VkResult` is null and its exact prerequisite reason is retained. Base image-format queries are never Not applicable.
- For 0.41.10+ producers, every scheduled format group has exactly six canonical ledger slots: LINEAR/OPTIMAL × base/OPAQUE_FD/ANDROID_HARDWARE_BUFFER. Missing, duplicated, malformed or contradictory tuple identities fail closed.
- Worker validation cross-checks the complete ledger against the fixed query recipe and aggregate attempted/success/format-not-supported/other-error diagnostics, so a scheduled AHB or OPAQUE_FD tuple cannot silently collapse to Unknown / Not reported.
- Compare ignores `available` ledger rows when a successful detailed-property payload exists, preserving the full successful value. Non-available ledger states overlay the same canonical tuple identity as historical successful/negative evidence.
- Formats detail may summarize all tuple states but must not add the ledger to Properties & Limits counts. Not applicable remains distinct from Unsupported, Unavailable and Unknown.
- Historical VulkanScope 0.41.9 separated non-success datasets and 0.41.8 embedded negative tuple rows remain accepted under their historical producer contracts.
- No D1 migration, stored-report rewrite, report-hash rewrite, capability inference, automatic upload or normalizer/schema bump is permitted.

## Release 0.39.9 / VulkanScope 0.41.11 reporting-state requirements

- The normalizer preserves `Available`, `Unsupported`, `Unavailable`, `Not applicable`, and `Unknown / not reported` as distinct evidence states.
- Generic zero Vulkan masks are rendered as numeric `0`; the Database must not invent an unqualified `VK_NONE`.
- Format support is a whole-format statement derived from the submitted format record. Linear/optimal/buffer feature masks are separately queried values and must not inherit the whole-format Supported/Unsupported badge.
- A zero format feature mask is valid available query evidence and remains `0`; it does not by itself prove that the entire format is unsupported.
- Image Format Properties2 keeps exact tuple semantics: Available only for `VkResult=0` with matching full property payload, Unsupported only for `VK_ERROR_FORMAT_NOT_SUPPORTED` (-11), other non-zero results Unavailable, and absent external-memory prerequisites Not applicable.
- One-sided historical evidence remains Unknown / Not reported. Current explicit Unknown profile rows are retained rather than treated as Unsupported.
- Source release ZIPs exclude root `README.md`, root `release.md`, packaged Fastlane/store metadata, dependency caches, generated Pages staging, and transient build artifacts.
