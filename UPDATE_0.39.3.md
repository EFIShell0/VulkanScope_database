# Updating a GitHub repository to 0.39.3

The 0.39.3 ZIP is intentionally laid out as the repository root. Extract its contents directly over the repository root so `.github/workflows/pages.yml`, `tools/audit_database.py`, and the versioned frontend asset are replaced in place.

After replacement, `.github/workflows` must contain only `pages.yml`. Delete/commit any obsolete workflow YAML left by older versions; GitHub executes every workflow file independently, so a stale workflow can continue producing old errors even when the new workflow succeeds.

A correct 0.39.3 Actions run prints this before the source audit:

`VulkanScope Database audit tool 0.39.3`

If the log still contains the exact old message `forbidden release artifact .git/...`, GitHub is running an older `tools/audit_database.py`; that string is not present in the 0.39.3 executable audit script.
