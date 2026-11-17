# VulkanScope Database 4.0.7

- Added Samsung Internet, Xiaomi Mi Browser, TapTap Browser and known Firefox/Chromium derivative identification. Browser product versions no longer override engine versions (Samsung Internet 24 / Chrome 117 now passes the engine check).
- Removed any Edge-specific denial: a real first-party DOM JPEG XL image, including compatible extension-transformed images, is the admission test. If JPEG XL fails, a descriptive warning remains on the current page rather than redirecting. Network, MIME, and timeout errors are reported separately.
- Added Edge help and JXL-RS Edge links for Android and PC supplied by the project owner. **Platform association is assumed from link order; the Drive contents could not be verified.** Follow the files' own installation instructions and browser extension-permission process; reload the page to retest.
- Kept the private-data policy, producer 4.0.15/4015 admission contract, D1 schema, Vulkan metadata and snapshot pipeline unchanged. Local validation does not imply published deployment.
