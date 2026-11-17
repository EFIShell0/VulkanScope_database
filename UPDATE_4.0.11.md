# VulkanScope Database 4.0.11 — Silent, shorter JPEG XL startup check

- Remove the visible JPEG XL test image section. A tiny on-screen, ARIA-hidden probe is maintained outside the compatibility card solely to establish real native decode or first-frame JXL-RS Edge Canvas success.
- Keep the mandatory real JPEG XL decoding verification and no false extension detection. The probe timeout is shortened from 22,000 ms to 4,800 ms; error diagnostics still distinguish MIME, network and decoder failures.
- Never display the browser-incompatibility card while a supported Chromium/Gecko/WebKit engine is still undergoing JPEG XL verification. Edge uses the same Chromium >=84 version/required Web API criteria as other Chromium browsers, never a vendor block.
- Change the desktop JXL-RS Edge package link to the project owner's new Google Drive URL `1UO_q25AzDKSxGVOJhsv7d0H1TQAVNIox` in both main and standalone fallback. No Android installer link. The remote file contents were not independently verified.
- Preserve release source integrity: VulkanScope producer 4.0.15/4015, Vulkan 1.4.366, normalizer 16, 284 project JPEG XL asset bytes, D1, Cloudflare Worker admission, snapshot/Cron and report security.
- This changes only the web frontend compat UX and release metadata; not the JXL-RS Edge extension.
