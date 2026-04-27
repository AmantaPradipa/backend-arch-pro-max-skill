# Changelog

All notable changes to this project will be documented in this file.

## 0.3.0 - 2026-04-27

- Added npm-ready packaging metadata for `backend-arch-pro-max-cli` and aligned versions to `0.3.0`.
- Added release documentation: `RELEASE_NOTES.md` and updated README release guidance.
- Added GitHub Actions tag-based release workflow (`v*`) with validation, tests, npm publish, and GitHub Release creation.
- Added generated platform template source-of-truth workflow via `templates/platforms/source.json` and `scripts/generate_platform_templates.py`.
- Added framework stack guidance for `rails`, `phoenix`, `hono`, `bun`, `actix`, `axum`, and `ktor`.
- Added `.gitignore` and npm packaging exclusions (`cli/.npmignore`).
