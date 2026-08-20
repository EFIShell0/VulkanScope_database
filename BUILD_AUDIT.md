# VulkanScope Database 0.35.5 build audit

## Scope
Windows reliability correction for the Cloudflare account-isolation guard introduced in 0.35.4. No report schema, D1 migration, public frontend technical semantics, Worker route or production binding changes.

## Production identity
- Cloudflare account ID: `ccf3de9d3f2a4394af2fb7be7fd5bbf4`
- Worker: `vulkanscope-database-api`
- D1 binding: `DB`
- D1 database: `vulkanscope-database`
- D1 UUID: `8fa65ef5-701d-4110-993d-87381f9763ab`
- Wrangler auth profile: `vulkanscope`

## Fix
The 0.35.4 verifier used direct `npx.cmd` execution through `execFileSync` on Windows. A valid active profile could therefore fail before Wrangler returned identity data. 0.35.5 executes the project-local pinned Wrangler JavaScript CLI via `process.execPath` when installed, with a Windows-safe `npx` fallback. JSON `whoami` is preferred; exact account-ID text verification is fallback-only. Debug log variables are removed from the verifier subprocess.

## Checks
- Account pin unchanged: PASS.
- D1 UUID/binding unchanged: PASS.
- Verifier JavaScript syntax: PASS.
- Local-Wrangler direct execution path present: PASS.
- Windows-safe fallback path present: PASS.
- Exact pinned-account comparison remains fail closed: PASS.
- No D1 migration added: PASS.
- No report schema change: PASS.
- Frontend release identity updated to 0.35.5: PASS.
