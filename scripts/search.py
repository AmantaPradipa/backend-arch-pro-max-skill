#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend Arch Pro Max Search - BM25 search engine for backend architecture rules.

Usage:
  python scripts/search.py "<query>" --architecture [-p "Project Name"]
  python scripts/search.py "<query>" --domain api
  python scripts/search.py "<query>" --stack nestjs
"""

import argparse
import csv
import io
import re
import sys
from collections import defaultdict
from datetime import datetime
from math import log
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "src" / "backend-arch-pro-max" / "data"
MAX_RESULTS = 3

CSV_CONFIG = {
    "api": {
        "file": "api_patterns.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "database": {
        "file": "database_patterns.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "caching": {
        "file": "caching_strategies.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "resilience": {
        "file": "resilience_patterns.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "security": {
        "file": "security_patterns.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "async": {
        "file": "async_patterns.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "observability": {
        "file": "observability_patterns.csv",
        "search_cols": ["category", "name", "description", "when_to_use", "trade_offs", "keywords"],
        "output_cols": ["category", "name", "description", "when_to_use", "trade_offs", "implementation_notes", "references"],
    },
    "anti-patterns": {
        "file": "anti_patterns.csv",
        "search_cols": ["severity", "name", "bad_example", "why_bad", "good_example", "keywords"],
        "output_cols": ["severity", "name", "bad_example", "why_bad", "good_example", "references"],
    },
}

STACK_CONFIG = {
    "node-express": "stacks.csv",
    "nestjs": "stacks.csv",
    "nextjs-api": "stacks.csv",
    "laravel": "stacks.csv",
    "django": "stacks.csv",
    "fastapi": "stacks.csv",
    "spring-boot": "stacks.csv",
    "go": "stacks.csv",
    "dotnet": "stacks.csv",
    "rails": "stacks.csv",
    "phoenix": "stacks.csv",
    "hono": "stacks.csv",
    "bun": "stacks.csv",
    "actix": "stacks.csv",
    "axum": "stacks.csv",
    "ktor": "stacks.csv",
}


class BM25:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.n = 0

    def tokenize(self, text):
        text = re.sub(r"[^\w\s]", " ", str(text).lower())
        return [word for word in text.split() if len(word) > 2]

    def fit(self, documents):
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.n = len(self.corpus)
        if self.n == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.n
        for doc in self.corpus:
            for word in set(doc):
                self.doc_freqs[word] += 1
        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.n - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query):
        query_tokens = self.tokenize(query)
        ranked = []
        for index, doc in enumerate(self.corpus):
            term_freqs = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1
            score = 0
            for token in query_tokens:
                if token not in self.idf:
                    continue
                tf = term_freqs[token]
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * self.doc_lengths[index] / self.avgdl)
                score += self.idf[token] * numerator / denominator
            ranked.append((index, score))
        return sorted(ranked, key=lambda item: item[1], reverse=True)


def load_csv(filepath):
    with open(filepath, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def search_csv(filepath, search_cols, output_cols, query, max_results, row_filter=None):
    if not filepath.exists():
        return []
    rows = load_csv(filepath)
    if row_filter:
        rows = [row for row in rows if row_filter(row)]
    documents = [" ".join(str(row.get(col, "")) for col in search_cols) for row in rows]
    bm25 = BM25()
    bm25.fit(documents)
    ranked = bm25.score(query)
    results = []
    for index, score in ranked[:max_results]:
        if score > 0:
            row = rows[index]
            results.append({col: row.get(col, "") for col in output_cols if col in row})
    if not results and rows:
        for row in rows[:max_results]:
            results.append({col: row.get(col, "") for col in output_cols if col in row})
    return results


def detect_domain(query):
    query_lower = query.lower()
    keywords = {
        "api": ["api", "rest", "graphql", "grpc", "trpc", "endpoint", "pagination", "versioning", "contract"],
        "database": ["database", "postgres", "mysql", "schema", "index", "transaction", "tenant", "n+1", "query", "sharding"],
        "caching": ["cache", "redis", "ttl", "invalidation", "session", "lock", "pubsub"],
        "resilience": ["retry", "timeout", "circuit", "breaker", "bulkhead", "saga", "fallback", "resilience"],
        "security": ["auth", "jwt", "oauth", "password", "rbac", "rate limit", "secret", "csrf", "cors"],
        "async": ["queue", "kafka", "rabbitmq", "sqs", "worker", "webhook", "event", "idempotency", "email", "pdf"],
        "observability": ["log", "metrics", "trace", "slo", "monitor", "audit", "correlation", "observability"],
        "anti-patterns": ["anti", "bad", "review", "bug", "risk", "avoid", "smell"],
    }
    scores = {
        domain: sum(1 for word in words if re.search(r"\b" + re.escape(word) + r"\b", query_lower))
        for domain, words in keywords.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "api"


def search(query, domain=None, max_results=MAX_RESULTS):
    domain = domain or detect_domain(query)
    config = CSV_CONFIG.get(domain)
    if not config:
        return {"error": f"Unknown domain: {domain}"}
    results = search_csv(
        DATA_DIR / config["file"],
        config["search_cols"],
        config["output_cols"],
        query,
        max_results,
    )
    return {"domain": domain, "query": query, "file": config["file"], "count": len(results), "results": results}


def search_stack(query, stack, max_results=MAX_RESULTS):
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack: {stack}. Available: {', '.join(STACK_CONFIG)}"}
    output_cols = ["stack", "category", "guideline", "do", "dont", "notes"]
    results = search_csv(
        DATA_DIR / STACK_CONFIG[stack],
        ["stack", "category", "guideline", "do", "dont", "keywords"],
        output_cols,
        query,
        max_results,
        row_filter=lambda row: row.get("stack") == stack,
    )
    return {"domain": "stack", "stack": stack, "query": query, "file": STACK_CONFIG[stack], "count": len(results), "results": results}


def format_results(result):
    if "error" in result:
        return f"Error: {result['error']}"
    title = "Backend Arch Pro Max Stack Guidelines" if result.get("stack") else "Backend Arch Pro Max Search Results"
    lines = [
        f"## {title}",
        f"**Domain:** {result.get('domain')} | **Query:** {result.get('query')}",
        f"**Source:** {result.get('file')} | **Found:** {result.get('count')} results",
        "",
    ]
    for index, row in enumerate(result.get("results", []), 1):
        lines.append(f"### Result {index}")
        for key, value in row.items():
            value = str(value)
            if len(value) > 360:
                value = value[:360] + "..."
            lines.append(f"- **{key}:** {value}")
        lines.append("")
    return "\n".join(lines)


def first_result(query, domain):
    result = search(query, domain, 1)
    return result.get("results", [{}])[0] if result.get("results") else {}


def domain_query(query, domain):
    query_lower = query.lower()
    explicit_terms = {
        "api": ["rest", "graphql", "grpc", "trpc", "endpoint", "pagination", "openapi"],
        "database": ["postgres", "mysql", "schema", "index", "transaction", "tenant", "n+1", "shard"],
        "caching": ["cache", "redis", "ttl", "session", "invalidation"],
        "async": ["queue", "kafka", "rabbitmq", "webhook", "worker", "event", "idempotency"],
        "security": ["auth", "jwt", "oauth", "oidc", "rbac", "password", "rate limit", "secret"],
        "resilience": ["retry", "timeout", "circuit", "bulkhead", "saga", "fallback"],
        "observability": ["log", "metric", "trace", "audit", "slo", "monitor"],
    }
    defaults = {
        "api": "REST resource API cursor pagination endpoint",
        "database": "service layer repository transaction indexing",
        "caching": "cache-aside TTL invalidation Redis",
        "async": "background job queue idempotency outbox",
        "security": "OAuth2 OIDC JWT RBAC validation secrets",
        "resilience": "timeout retry backoff circuit breaker",
        "observability": "structured logs correlation id metrics tracing",
    }
    if any(term in query_lower for term in explicit_terms.get(domain, [])):
        return query
    return f"{query} {defaults.get(domain, '')}"


def box_line(label, value, width=72):
    label_text = f"{label}:" if label else ""
    content_width = width - 19
    value = str(value or "")[:content_width]
    return f"| {label_text:<14} {value:<{content_width}} |"


def generate_architecture(query, project_name=None):
    api = first_result(domain_query(query, "api"), "api")
    database = first_result(domain_query(query, "database"), "database")
    caching = first_result(domain_query(query, "caching"), "caching")
    async_pattern = first_result(domain_query(query, "async"), "async")
    security = first_result(domain_query(query, "security"), "security")
    resilience = first_result(domain_query(query, "resilience"), "resilience")
    observability = first_result(domain_query(query, "observability"), "observability")
    anti = search(query, "anti-patterns", 3).get("results", [])

    target = project_name or query
    avoid = "; ".join(item.get("name", "") for item in anti if item.get("name")) or "N+1 queries; exposed internals; missing transaction"

    width = 72
    lines = [
        "+" + "-" * (width - 2) + "+",
        box_line("TARGET", target, width),
        "+" + "-" * (width - 2) + "+",
        box_line("ARCHITECTURE", database.get("name", "Service Layer + Repository"), width),
        box_line("API", api.get("name", "REST + cursor pagination"), width),
        box_line("DB", database.get("implementation_notes", "Transactions and indexes"), width),
        box_line("CACHE", caching.get("name", "Cache-aside with TTL"), width),
        box_line("ASYNC", async_pattern.get("name", "Queue workers + idempotency"), width),
        box_line("SECURITY", security.get("name", "OAuth2/JWT + RBAC"), width),
        box_line("RESILIENCE", resilience.get("name", "Timeouts + retries"), width),
        box_line("OBSERVABILITY", observability.get("name", "Structured logs + tracing"), width),
        box_line("AVOID", avoid, width),
        box_line("CHECKLIST", "[ ] validate request boundary", width),
        box_line("", "[ ] transaction for multi-write", width),
        box_line("", "[ ] no unbounded list queries", width),
        box_line("", "[ ] async for slow external work", width),
        box_line("", "[ ] sanitized errors + trace id", width),
        "+" + "-" * (width - 2) + "+",
        "",
        "## Rationale",
        f"- **API:** {api.get('description', '')}",
        f"- **Database:** {database.get('description', '')}",
        f"- **Caching:** {caching.get('description', '')}",
        f"- **Async:** {async_pattern.get('description', '')}",
        f"- **Security:** {security.get('description', '')}",
        f"- **Observability:** {observability.get('description', '')}",
    ]
    return "\n".join(lines)


def slugify(value):
    value = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).strip().lower())
    return value.strip("-") or "backend-architecture"


def persist_architecture(query, project_name=None, service=None, output_dir=None):
    architecture = generate_architecture(query, project_name)
    root = Path(output_dir) if output_dir else Path.cwd()
    project_slug = slugify(project_name or query)
    arch_dir = root / "architecture" / project_slug
    arch_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = [
        f"# Backend Architecture: {project_name or query}",
        "",
        f"> Generated: {timestamp}",
        f"> Query: {query}",
        "",
        "```text",
        architecture,
        "```",
        "",
        "## Usage Notes",
        "",
        "- Treat this file as the backend architecture source of truth.",
        "- Check `services/` for service-specific overrides before implementing a specific service.",
        "- Keep controllers thin and place business rules in services.",
        "- Re-run anti-pattern search before delivery.",
        "",
    ]
    master_path = arch_dir / "MASTER.md"
    master_path.write_text("\n".join(header), encoding="utf-8")

    service_path = None
    if service:
        services_dir = arch_dir / "services"
        services_dir.mkdir(parents=True, exist_ok=True)
        service_slug = slugify(service)
        service_path = services_dir / f"{service_slug}.md"
        service_lines = [
            f"# {service} Service Overrides",
            "",
            f"> Project: {project_name or query}",
            f"> Generated: {timestamp}",
            "",
            "Rules in this file override `../MASTER.md` only for this service.",
            "",
            "## Service Scope",
            "",
            "- Define owned routes or events before implementation.",
            "- Define owned tables or collections before implementation.",
            "- Define queue topics or jobs before implementation.",
            "",
            "## Required Checks",
            "",
            "- [ ] Request validation at boundary",
            "- [ ] Authorization checked in service layer",
            "- [ ] Transaction boundary documented",
            "- [ ] Idempotency for external writes or retries",
            "- [ ] Structured logs with correlation ID",
            "",
        ]
        service_path.write_text("\n".join(service_lines), encoding="utf-8")

    lines = [architecture, "", "## Persisted Files", f"- {master_path}"]
    if service_path:
        lines.append(f"- {service_path}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Backend Arch Pro Max Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Search domain")
    parser.add_argument("--stack", "-s", choices=list(STACK_CONFIG.keys()), help="Stack-specific search")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max results")
    parser.add_argument("--architecture", "-a", action="store_true", help="Generate full backend architecture recommendation")
    parser.add_argument("--project-name", "-p", default=None, help="Project name")
    parser.add_argument("--persist", action="store_true", help="Save architecture to architecture/<project>/MASTER.md")
    parser.add_argument("--service", default=None, help="Create service-specific override under architecture/<project>/services/")
    parser.add_argument("--output-dir", "-o", default=None, help="Output directory for persisted architecture files")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.architecture:
        if args.persist:
            print(persist_architecture(args.query, args.project_name, args.service, args.output_dir))
        else:
            print(generate_architecture(args.query, args.project_name))
        return
    if args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
    else:
        result = search(args.query, args.domain, args.max_results)
    if args.json:
        import json

        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_results(result))


if __name__ == "__main__":
    main()
