# VulkanScope Database 0.35.6

- Reworked the database background and interactive chrome to the OpenGLESScope-quality chromatic shell using Vulkan official red `#A41E22`.
- Vulkan-red-derived styling now covers the page glow, hero, navigation/detail tabs, filters, search focus, cards, scroll controls, pagination and action surfaces.
- Preserved supported/unsupported/available/unavailable/unknown semantic colors and 0.35.3 dominant-coverage rules unchanged.
- Versioned frontend assets to `site.v0356.css` and `app.v0356.js` for cache-safe GitHub Pages deployment.

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
