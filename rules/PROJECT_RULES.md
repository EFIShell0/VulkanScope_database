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
- The published Khronos Registry version and the VulkanScope producer/query baseline are distinct. As of this audit the public Khronos latest specification is 1.4.358 (2026-07-31); the database keeps VulkanScope's independently pinned producer/query baseline 1.4.360 labeled as such and does not call it Khronos latest.
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
