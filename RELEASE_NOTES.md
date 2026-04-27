# Backend Arch Pro Max Release Notes

## Version

- Release: `0.3.0`
- Date: `2026-04-27`
- Tag: `v0.3.0`

## Highlights

- Dataset expanded with additional framework stack rules.
- CLI package is now npm-ready as `backend-arch-pro-max-cli`.
- Installer templates are now generated from one source-of-truth file.
- Automated release workflow added for validation, packaging, npm publishing, and GitHub Release publishing.

## Dataset Updates

- Added stack guidance for:
  - Rails
  - Phoenix
  - Hono
  - Bun
  - Actix
  - Axum
  - Ktor

## CLI and Packaging

- `cli/package.json` updated with release metadata:
  - repository
  - bugs
  - homepage
  - keywords
  - files
  - engines
  - publishConfig
- Package remains runtime dependency-free.
- Supports direct execution through:

```powershell
npx backend-arch-pro-max-cli init --ai codex
```

## Template Generator

- Added source file: `templates/platforms/source.json`.
- Added generator: `scripts/generate_platform_templates.py`.
- Platform templates (`codex`, `claude`, `cursor`, `windsurf`) are generated and validated from this source.

## Release Workflow

- Added `.github/workflows/release.yml`.
- Triggered by:
  - `push` tags matching `v*`
  - `workflow_dispatch`
- Validation and release pipeline includes:
  - skill metadata validation (quick_validate equivalent checks)
  - CSV validation via `_sync_all.py`
  - unit tests via `python -m unittest`
  - Node syntax check for CLI entrypoint
  - CLI smoke tests (`list`, `init --dry-run`)
  - npm package dry-run
  - npm publish from `cli/` on tag runs
  - GitHub Release from this file on tag runs

## Testing

Run before release:

```powershell
python C:\Users\USER\.codex\skills\.system\skill-creator\scripts\quick_validate.py backend-arch-pro-max-skill
$env:PYTHONDONTWRITEBYTECODE='1'; python backend-arch-pro-max-skill\src\backend-arch-pro-max\data\_sync_all.py
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest backend-arch-pro-max-skill\tests\test_search.py
$env:PYTHONDONTWRITEBYTECODE='1'; python backend-arch-pro-max-skill\scripts\generate_platform_templates.py --check
node -c backend-arch-pro-max-skill\cli\bin\backend-arch-pro-max.js
node backend-arch-pro-max-skill\cli\bin\backend-arch-pro-max.js list
node backend-arch-pro-max-skill\cli\bin\backend-arch-pro-max.js init --ai codex --target . --dry-run
npm --prefix backend-arch-pro-max-skill\cli pack --dry-run
```

## Known Requirements

- Add repository secret `NPM_TOKEN` before publishing tags.
- Configure GitHub authentication before pushing to `AmantaPradipa/backend-arch-pro-max-skill`.
- GitHub repository should remain private as requested.
