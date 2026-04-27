# Backend Arch Pro Max

Backend Arch Pro Max is an AI coding-agent skill for backend architecture decisions, API design, database design, caching, async processing, resilience, security, observability, and anti-pattern review.

It follows the same broad pattern as UI/UX Pro Max: searchable rules, a lightweight reasoning engine, structured recommendations, and a pre-delivery checklist.

## What It Covers

- API contracts: REST, GraphQL, gRPC, tRPC, pagination, versioning, webhooks, streaming, and error envelopes.
- Database architecture: service layer, repository pattern, transactions, indexing, tenancy, migrations, locking, backups, and CDC.
- Caching: Redis, cache-aside, write-through, invalidation, cache stampede control, tenant-scoped keys, and cache observability.
- Resilience: timeouts, retries, circuit breakers, bulkheads, sagas, quotas, canaries, reconciliation, and graceful degradation.
- Security: OAuth2/OIDC, JWT, RBAC, ABAC, password hashing, webhook verification, CSRF, CORS, SSRF, encryption, and audit events.
- Async systems: queues, outbox, inbox, Kafka, RabbitMQ, DLQ, idempotency, workflows, delayed retries, and job progress.
- Observability: structured logs, correlation IDs, traces, metrics, SLOs, audit logs, queue metrics, and deployment markers.
- Anti-patterns: N+1 queries, hardcoded secrets, cross-tenant leaks, unsafe retries, exposed stack traces, missing transactions, and more.

## Dataset

Current dataset size: **302 rows**.

| File | Rows |
| --- | ---: |
| `api_patterns.csv` | 40 |
| `database_patterns.csv` | 40 |
| `caching_strategies.csv` | 25 |
| `resilience_patterns.csv` | 25 |
| `security_patterns.csv` | 40 |
| `async_patterns.csv` | 30 |
| `observability_patterns.csv` | 25 |
| `anti_patterns.csv` | 50 |
| `stacks.csv` | 27 |

Validate the CSV files:

```powershell
python src\backend-arch-pro-max\data\_sync_all.py
```

## Usage

Generate a full backend architecture recommendation:

```powershell
python scripts\search.py "multi tenant saas auth payment webhook postgres redis" --architecture -p "Multi Tenant SaaS"
```

Search one domain:

```powershell
python scripts\search.py "jwt refresh token rbac tenant" --domain security -n 3
```

Search stack-specific guidance:

```powershell
python scripts\search.py "nestjs service repository transaction" --stack nestjs -n 3
```

Persist an architecture decision record:

```powershell
python scripts\search.py "billing webhook payments idempotency postgres queue" --architecture --persist -p "Billing API" --service "Webhook Worker" -o examples\generated
```

This creates:

```text
examples/generated/architecture/billing-api/MASTER.md
examples/generated/architecture/billing-api/services/webhook-worker.md
```

## CLI Installer

Install and run from npm:

```powershell
npx backend-arch-pro-max-cli init --ai codex --target . --dry-run
npx backend-arch-pro-max-cli init --ai antigravity --target . --dry-run
```

List supported platforms:

```powershell
node cli\bin\backend-arch-pro-max.js list
```

Preview an install:

```powershell
node cli\bin\backend-arch-pro-max.js init --ai codex --target . --dry-run
```

Install into a project:

```powershell
node cli\bin\backend-arch-pro-max.js init --ai codex --target . --force
```

Supported platform templates currently include Codex, Claude, Cursor, Windsurf, and Antigravity.

## Platform Template Generator

Platform templates are generated from a single source file and should not be edited manually.

Generate templates:

```powershell
python scripts\generate_platform_templates.py
```

Validate generated templates without writing changes:

```powershell
python scripts\generate_platform_templates.py --check
```

## Skill Structure

```text
backend-arch-pro-max-skill/
|-- SKILL.md
|-- README.md
|-- skill.json
|-- agents/openai.yaml
|-- cli/
|-- docs/REFERENCE.md
|-- examples/
|-- scripts/search.py
|-- templates/platforms/
|-- tests/test_search.py
`-- src/backend-arch-pro-max/data/
```

## Validation

```powershell
python C:\Users\USER\.codex\skills\.system\skill-creator\scripts\quick_validate.py .
$env:PYTHONDONTWRITEBYTECODE='1'; python src\backend-arch-pro-max\data\_sync_all.py
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests\test_search.py
node cli\bin\backend-arch-pro-max.js list
node cli\bin\backend-arch-pro-max.js init --ai codex --target . --dry-run
npm --prefix cli pack --dry-run
```

## Release

- Current release version: `0.3.0`.
- Tag format: `v*` (example: `v0.3.0`).
- CI release workflow file: `.github/workflows/release.yml`.
- npm publish requires repository secret `NPM_TOKEN`.
- GitHub Release notes are sourced from `RELEASE_NOTES.md`.

## Roadmap

- Add more platform templates from `templates/platforms/source.json`.
- Add integration guidance with UI/UX Pro Max, DevOps Pro Max, QA Pro Max, and AppSec Pro Max.
- Add more realistic generated architecture examples.
