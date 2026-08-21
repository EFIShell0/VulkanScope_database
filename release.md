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
