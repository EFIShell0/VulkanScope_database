# VulkanScope Database 0.30.0

GitHub Pages frontend plus a Cloudflare Worker + D1 submission API. The site remains suitable for `*.github.io`; only live report storage/querying uses the Worker.

## Deploy the API

1. Create a Cloudflare D1 database named `vulkanscope-database`.
2. Put its database ID in `worker/wrangler.jsonc`.
3. Set `ALLOWED_ORIGIN` to the exact GitHub Pages origin.
4. In `worker/`, run `npm install`, `npx wrangler d1 migrations apply vulkanscope-database --remote`, then `npx wrangler deploy`.
5. Copy the resulting HTTPS Worker origin into `config.js` and into VulkanScope Settings → Database API endpoint.

D1 is bound directly to the Worker. No secret is embedded in the APK. The API validates schema and payload size, rejects fields matching personal-identifier classes, deduplicates reports by SHA-256, and does not persist the request IP address.

## Publish the frontend

Push the repository contents to GitHub and enable GitHub Pages with the included workflow. If `config.js` has an API origin, the site reads live reports from D1. If it is empty, the original static `data/index.json` mode remains available.

## Submission semantics

Submission is explicit and user initiated. There is no per-capability selection. The complete technical TXT-equivalent report plus structured device/GPU/driver/Vulkan metadata is submitted as one payload. IMEI, Android ID, device serial, MAC address, account data, authentication tokens and private file paths are excluded. No automatic/background upload exists.

The database keeps unavailable/unknown/unsupported semantics distinct and keeps loader API, device API and driver version separate.
