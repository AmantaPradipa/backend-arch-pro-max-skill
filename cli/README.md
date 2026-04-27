# Backend Arch Pro Max CLI

Installer CLI for copying the skill into an agent platform folder.

Run directly from npm:

```powershell
npx backend-arch-pro-max-cli init --ai codex --target . --dry-run
```

```powershell
node cli\bin\backend-arch-pro-max.js list
node cli\bin\backend-arch-pro-max.js init --ai codex --target . --dry-run
node cli\bin\backend-arch-pro-max.js init --ai codex --target . --force
```

Supported platforms come from generated `templates/platforms/*.json` files.

The CLI intentionally has no runtime dependencies. It copies the skill files into the selected platform folder and refuses to overwrite an existing destination unless `--force` is provided.
