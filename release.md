# VulkanScope Database 0.35.3

Coverage emphasis correction based on 0.35.2.

## Fix

- Non-dominant coverage percentages no longer inherit the global Supported / Unsupported / Available / Unavailable / Unknown background across the full coverage cell.
- Their semantic color is confined to the progress-bar fill and their percentage text stays neutral.
- Only the unique dominant percentage may use the wider semantic background/text emphasis.
- Count badges are intentionally unchanged.
