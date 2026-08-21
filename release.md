# VulkanScope Database 0.35.9

Display/HDR, ABI and home-metric presentation parity release aligned with the existing VulkanScope schema-v3 contract.

## Changes
- Renames the user-facing `Display / HDR` section to `Display & HDR` across primary/detail presentation.
- Lists producer-reported supported device ABIs beneath the installed application ABI in Reports.
- Displays numeric minimum, average and maximum Android luminance values with `cd/m²` in aggregate and detail views.
- Adds separate home cards for the current producer/query baseline and compatible producer contract.
- Keeps Vulkan support-state semantics, schema-v3 authority, raw report access and D1 storage unchanged.
- Active frontend JavaScript is cache-busted as `app.v0359.js`; `site.v0357.css` is unchanged.
- No D1 migration is required.

---

# VulkanScope Database 0.35.8

Properties/Limits semantic-correctness release aligned with VulkanScope 0.33.10 structured reports.

## Changes

- Fixes the Database report-detail **Properties** count being inflated by TXT-normalized DEVICE/SURFACE and other non-property capability rows.
- Uses schema-v3 `technicalReport.devices[].detailedProperties` as the authoritative Properties dataset.
- Uses schema-v3 `technicalReport.devices[].limits` as the authoritative Limits dataset.
- Stops treating section names such as `Sparse Properties` as Limits merely because their label matched a heuristic.
- Keeps TXT parsing as a compatibility fallback: bracketed non-feature query-result rows are Properties and the literal `LIMITS` section is Limits.
- Updates aggregate Properties/Limits views and report-detail tabs to consume the separated datasets.
- Preserves Unknown denominators for loaded reports that do not contain a given property or limit.
- Bumps Worker normalizer to `11`.
- Versioned active frontend JavaScript to `app.v0358.js`; `site.v0357.css` is unchanged.
- No D1 migration and no stored-payload rewrite required.

---

# VulkanScope Database 0.35.7

Full producer-compatibility, data-semantics, specification, security and usability audit against VulkanScope 0.33.7.

## Changes

- Cross-validates schema-v3 primary-device identity, device API, loader/instance API, driver mode/version and registry/header/report baselines against top-level submission metadata.
- Validates the current VulkanScope TXT report identity and required technical sections before accepting new reports.
- Adds bounded browser API reads: 20-second timeout, 4 MiB response ceiling, repeated-cursor rejection and four-worker detail concurrency.
- Fixes property/limit/feature aggregate denominators so missing report fields remain Unknown instead of disappearing from coverage.
- Adds Unknown coverage to format aggregates when a loaded report lacks a format row.
- Uses explicit producer HDR state where available: missing HDR evidence is Unknown; an explicit empty HDR list is Unavailable.
- Extends Display/HDR semantic filtering to Supported, Unsupported, Available, Unavailable and Unknown evidence.
- Adds API CORP/COOP and restrictive CSP response headers.
- Exposes the currently published Khronos specification separately as Vulkan 1.4.359 (2026-08-07), while keeping VulkanScope's 1.4.360 producer/query staging baseline distinct.
- Worker normalizer version: `10`.
- No D1 migration required.

---

# VulkanScope Database 0.35.6

- Reworked the database background and interactive chrome to the OpenGLESScope-quality chromatic shell using Vulkan official red `#A41E22`.
- Vulkan-red-derived styling now covers the page glow, hero, navigation/detail tabs, filters, search focus, cards, scroll controls, pagination and action surfaces.
- Preserved supported/unsupported/available/unavailable/unknown semantic colors and 0.35.3 dominant-coverage rules unchanged.
- Versioned frontend assets to `site.v0357.css` and `app.v0357.js` for cache-safe GitHub Pages deployment.

# VulkanScope Database 0.35.5

Windows reliability fix for the fail-closed Cloudflare account guard introduced in 0.35.4. Correctly activated `vulkanscope` auth profiles now verify through the project-local Wrangler CLI, while wrong or unreadable accounts remain blocked. No database migration, report-schema or frontend-data change is required.

# VulkanScope Database 0.35.4

Cloudflare account-isolation hardening release. Production account and D1 bindings are pinned, project-local auth-profile commands are provided, and npm production operations verify the active Cloudflare account before execution. No database migration or report-schema change is required.

# VulkanScope Database 0.35.3

Coverage emphasis correction based on 0.35.2.

## Fix

- Non-dominant coverage percentages no longer inherit the global Supported / Unsupported / Available / Unavailable / Unknown background across the full coverage cell.
- Their semantic color is confined to the progress-bar fill and their percentage text stays neutral.
- Only the unique dominant percentage may use the wider semantic background/text emphasis.
- Count badges are intentionally unchanged.
