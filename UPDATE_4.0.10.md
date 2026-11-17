# VulkanScope Database 4.0.10 — JPEG XL setup guidance

- Keep the strict JPEG XL startup decoder/rendering check from 4.0.9.
- Edge desktop: guide ONLY Developer mode + Load unpacked from the extracted PC extension directory containing manifest.json; no CRX/Load package instruction.
- Edge Android: remove the Android archive link and explain that the currently provided unpacked-extension installation method is not available; do not imply a supported installation method exists.
- Other Chromium-family browsers: explain built-in jxl-rs with `enable-jxl-image-format` only when a browser exposes it and ships the decoder; platform forks/Android support differ. No speculative installation link.
- Firefox/Gecko family: `about:config` -> `image.jxl.enabled` = true if supported, with optional Firefox Labs JPEG XL toggle. Newer Firefox releases may be default enabled.
- Keep separate network/MIME/timeout/decoder failure diagnoses; never mistake a missing flag for an installable decoder.
- No change to D1 data, migrations, report submission gate, GPU/Vulkan catalog, JPEG XL image bytes, or extension itself.
