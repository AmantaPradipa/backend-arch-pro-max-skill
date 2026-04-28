# CLAUDE.md
 
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
 
## Project Overview
 
Backend Arch Pro Max is an AI-powered backend architecture toolkit providing searchable databases of API patterns, database designs, caching strategies, resilience patterns, security standards, async processing, and observability guidelines.
 
## Search Command
 
```bash
python scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```
 
**Domain search:**
- `api` - API contracts and patterns
- `database` - Database architecture and persistence
- `caching` - Caching strategies and Redis patterns
- `resilience` - Error handling, retries, and circuit breakers
- `security` - Auth, encryption, and security standards
- `async` - Queues, events, and background processing
- `observability` - Logging, tracing, and metrics
- `anti-patterns` - Common backend failure modes
- `stacks` - Framework-specific implementation guidelines
 
**Architecture Generation:**
```bash
python scripts/search.py "<query>" --architecture -p "<project-name>"
```
 
## Architecture
 
```
backend-arch-pro-max-skill/
├── SKILL.md                      # Agent entry point
├── README.md                     # Public documentation
├── cli/                          # CLI installer
├── docs/                         # Additional documentation
├── examples/                     # Generated & use-case examples
├── scripts/
│   ├── search.py                 # CLI entry point & search engine
│   └── generate_platform_templates.py # Template generator
├── src/backend-arch-pro-max/
│   └── data/                     # Canonical CSV databases
└── templates/platforms/          # Platform-specific configurations
```
 
## Development Workflow
 
1. **Data Updates**: Edit CSV files in `src/backend-arch-pro-max/data/`.
2. **Validation**: Run `python src/backend-arch-pro-max/data/_sync_all.py` to validate row counts and CSV integrity.
3. **Template Updates**: Edit `templates/platforms/source.json` and run `python scripts/generate_platform_templates.py`.
4. **Testing**: Run `python -m unittest tests/test_search.py`.
 
## Git Workflow
 
1. Create branch: `git checkout -b feat/your-feature`
2. Commit changes: `git commit -m "feat: description"`
3. Push and PR: `git push -u origin feat/...` then `gh pr create`
