# Updating an existing GitHub repository to 0.39.4

ZIP extraction and web file uploads do not delete stale files, and some update methods fail to replace hidden `.github` content. 0.39.4 includes a repository repair tool specifically for this.

After extracting the 0.39.4 ZIP over the repository root, run:

```bash
python tools/repair_repository.py --apply
python tools/audit_database.py --source-tree .
```

On Windows the same commands work from PowerShell when Python is installed.

A correct Actions run prints:

```text
VulkanScope Database audit tool 0.39.4
VulkanScope Database 0.39.4 repository state: PASS
```

If a log still runs `assets/app.v0391.js`, `actions/checkout@v6`, or prints `forbidden release artifact .git/...`, that run is executing pre-0.39.4 repository files rather than this release.
