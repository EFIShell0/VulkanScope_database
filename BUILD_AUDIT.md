# VulkanScope Database 0.35.6 build audit

## Scope
Presentation-only Vulkan brand-surface parity update based on the existing 0.35.5 database and the OpenGLESScope Database chromatic-shell treatment. No report schema, D1 schema, normalizer, capability-state inference, Cloudflare account isolation or stored report behavior was changed.

## Checks
- Official Vulkan primary brand color in frontend theme: `#A41E22`: PASS.
- Page ambient background uses Vulkan-red radial treatment: PASS.
- Hero, navigation/detail tabs, filters, search focus, cards and control chrome receive Vulkan-red-derived surfaces: PASS.
- Semantic state palette preserved (supported green / unsupported red / available blue / unavailable amber / unknown gray): PASS.
- 0.35.3 dominant coverage rules unchanged: PASS.
- Versioned CSS and JS references use v0356: PASS.
- Error pages reference v0356 CSS: PASS.
- Worker account pin and D1 pin unchanged: PASS.
- Worker JavaScript syntax check: PASS.
- Frontend JavaScript syntax check: PASS.
- JSON parse checks: PASS.
- ZIP integrity: PASS.
