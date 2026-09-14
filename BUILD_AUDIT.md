# VulkanScope Database 1.3.2 build / regression audit

- Database/frontend/Worker release identity: **1.3.2**.
- Frontend identity: `assets/app.v1302.js`, browser gate `browser-compat.v1302.js`, startup freshness bootstrap `release-bootstrap.v1302.js`, cache key **1302**.
- Immutable predecessor: Database **1.3.1**, SHA-256 `ec60e0456f46427713db697e6bd0b8e7742dfad62843e9743befdc3576da84dc`; its versioned frontend triplet remains byte-identical and is retained as the CDN transition bridge.
- Freshness: publication is treated as a generation, not a single marker. Marker/index/app/browser-gate/bootstrap are no-store probed and must agree before automatic cache-busted navigation; early convergence retries plus visibility/pageshow/online checks remove the manual-refresh dependency.
- Pointer/filter repair: blank custom-scrollbar rail/gutter space is non-interactive; intended controls remain interactive; custom-select internal pointer/click completion no longer triggers the document outside-click closer.
- Pagination: filter Previous/Next use compact fixed icon columns around a flexible bounded page-jump control so narrow mobile and desktop filter cards remain contained.
- Independence notice: exact English Khronos independence wording is preserved and presented as a blue information note with an `i` icon in Settings and footer.
- Browser information UI remains otherwise unchanged from 1.3.1; no browser-logo bundle is added.
- Semantic invariants: schema 2, technical report 3, normalizer 16, Vulkan 1.4.362/header 362, VulkanScope 1.2.5 submission floor, report IDs/hashes and D1 migrations are unchanged.

# VulkanScope Database 1.3.1 build / regression audit

- Database/frontend/Worker release identity: **1.3.1**.
- Frontend identity: `assets/app.v1301.js`, browser gate `browser-compat.v1301.js`, startup freshness bootstrap `release-bootstrap.v1301.js`, cache key **1301**.
- Immutable predecessor: Database **1.3.0**, SHA-256 `f49ebdc98d776de7792ceafc31c433c855bb87be1415b75191a6599c4f21ebe0`.
- UI language: first-party Database UI copy remains English; the footer and Information disclosure reads “VulkanScope is not affiliated with the Khronos Group and is not an official Khronos Group project.”
- Pagination: shared direct page entry keeps digit/range enforcement and now disables **Go** for the current page, invalid/empty values and single-page datasets. Every searchable filter retains 50-option pagination and direct page entry, including one-page result sets.
- Filter repair: searchable selector menus now use separate fixed search/pager regions around a dedicated scrollable option region, with explicit filter-family stacking. This removes the mobile overlay/clipping failure seen in long filter lists.
- Freshness: a same-origin no-store startup bootstrap verifies the release marker, current HTML and marker-named app asset before cache-busted navigation; the app stays concealed only during a bounded startup check. The schema footer now derives its Database version from the current release constant instead of the stale hard-coded 1.2.0 value.
- Licensing: bundled Markdown license documents open in a same-origin in-site modal with bounded text size, Escape/backdrop/close handling and custom scrolling; no new tab or third-party fetch is used.
- Live synchronization: atomic reconciliation emits a green accessible popup only when one or more previously unseen report IDs are actually added, with the number of reports shown.
- Semantic invariants: schema 2, technical report 3, normalizer 16, Vulkan registry/spec baseline 1.4.362/header 362, VulkanScope 1.2.5 submission floor, canonical report IDs/hashes and D1 migrations are unchanged.

# VulkanScope Database 1.3.0 build / regression audit

- Database/frontend/Worker release identity: **1.3.0**.
- Frontend identity: `assets/app.v1300.js`, browser gate `browser-compat.v1300.js`, cache key **1300**.
- Immutable predecessor: Database **1.2.15**, SHA-256 `3e78a70f31bf92e7ea2024227ae2df7f8cae3656dbe5cdffecef805eee352523`.
- Trademark presentation: every standalone user-facing `Vulkan` label is presented as **Vulkan®**, while `VulkanScope` and canonical/raw evidence, schema/token names, URLs, filenames and stored report bytes remain untouched. The runtime presentation layer also covers dynamically inserted text and accessible labels without rewriting raw/canonical views.
- Khronos independence disclosure: the exact Turkish notice requested by the project owner is shown in red below the footer brand and at the start of Settings → Information, with narrow-screen wrapping and no horizontal overflow.
- Information / licensing: the Information category inventories the explicitly declared or referenced browser/tooling/runtime components, their purpose, version or resolution status, license and source. Official upstream license texts/notices are bundled as same-origin Markdown for Wrangler, sharp, esbuild, workerd, Node.js and Python, and each applicable inventory card provides a **Read license (.md)** action. Managed services/APIs are not mislabeled as bundled libraries.
- Existing 1.2.15 report JSON export, 1.2.14 direct page entry/browser information, 1.2.13 50-item selector pagination, Compare state direction, Settings blur ownership and report/data semantics remain protected.
- Full audit scope: source and staged Pages allow-lists, JavaScript syntax, route/compare/report-text contracts, browser compatibility floor, UTF-8 text I/O, registry lock, Worker contract, D1 migration replay, local license-link integrity, Settings/footer mobile containment, stale asset cleanup, immutable predecessor contract and deterministic strict-package generation.
- Chromium UI smoke: **PASS** at 360×800, 430×900 and 1440×900 using an in-memory release fixture; document width, all four Settings categories, Information cards, six license links, footer notice and dynamic Vulkan® presentation remained contained and error-free.
- Semantic invariants: schema 2, technical report 3, normalizer 16, Vulkan registry/spec baseline 1.4.362/header 362, VulkanScope 1.2.5 submission floor, canonical report IDs/hashes and all three existing D1 migrations are unchanged.

# VulkanScope Database 1.2.14 build / regression audit

- Database/frontend/Worker release identity: **1.2.14**.
- Frontend identity: `assets/app.v1214.js`, browser gate `browser-compat.v1214.js`, cache key **1214**.
- Immutable predecessor: Database 1.2.13, SHA-256 `92424276d6eb586d1d30035753f45d33d40e8f41e150cee5343f573f47e615cb`.
- Pagination scope: every user-visible pager family now keeps Previous/Next and adds a shared direct page field plus Go action. The field is digit-only, bounded to `1..pageCount`, rejects invalid keyboard/paste/input mutations, supports Enter/Escape/Arrow Up/Down, and tracks dynamic page-count changes.
- Filter scope: searchable enhanced selectors still search the complete authoritative native option set first, paginate results deterministically in 50-option pages, reset to page 1 on a new query, and now permit direct bounded page entry without altering filter values.
- Internet Settings scope: a separate **Browser information** section appears below **My internet information** and reports best-effort browser/version/engine, Client Hints where exposed, UA/platform/languages/privacy hints, device/runtime hints, viewport/screen/UI preferences and Web Platform capabilities. This information is local-only and is not attached to reports, sent to the Worker or stored in D1; canvas/GPU-renderer fingerprinting is forbidden.
- Responsive scope: direct-page controls are contained in selector, Reports, bounded-table and modal pagers on desktop and narrow/mobile layouts; long browser-information rows wrap without forcing document-level horizontal overflow.
- Semantic invariants: schema 2, technical report 3, normalizer 16, Vulkan 1.4.362/header 362, VulkanScope 1.2.5 submission floor, canonical report IDs/hashes and D1 schema/migrations are unchanged.
- Mandatory gates: 1.2.14 focused verifier + negative mutations, immutable 1.2.13 regression contract, source/Pages audits, JavaScript syntax checks, Worker transport contract, D1 migration replay and deterministic strict-package build.

# VulkanScope Database 1.2.13 build / regression audit

- Database/frontend/Worker release identity: **1.2.13**.
- Frontend identity: `assets/app.v1213.js`, browser gate `browser-compat.v1213.js`, cache key **1213**.
- Immutable predecessor: Database 1.2.12, SHA-256 `bfae0e9bff7b84d73e93dfe37208df2fe3052193eb90648e7f4e63699eb0bb0c`.
- Requested UI scope: searchable selector results are true deterministic 50-option pages with Previous/Next controls; Compare full state uses a down chevron and minimized state uses an up chevron.
- Additional audit hardening: global enhanced-selector width is capped to its container, mobile selectors remove the legacy 190 px minimum, pager controls collapse to icon-size controls on narrow screens, and long option labels cannot force horizontal overflow.
- Regression scope: non-Reports mobile filter containment, Compare identity flow, pinned-selector dock suppression, Settings dim/blur ownership, report semantics, routing and evidence state remain protected.
- Semantic invariants: schema 2, technical report 3, normalizer 16, Vulkan 1.4.362/header 362, VulkanScope 1.2.5 submission floor and canonical report identity unchanged.
- Local Chromium runtime smoke: **PASS** across Reports + 17 other primary views at 360×800, 430×900 and 1440×900; no document-level horizontal overflow or uncaught page errors, and 125-option selector pagination/search plus Compare arrow-state transitions were exercised.
- Mandatory gates: 1.2.13 focused verifier + negative mutations, immutable 1.2.12 regression contract, source/Pages audits, JS syntax, Worker transport contract, D1 migration replay and deterministic strict-package build.
