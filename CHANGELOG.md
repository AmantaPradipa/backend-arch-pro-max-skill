# Changelog

All notable changes to this project will be documented in this file.

## 0.2.0 - 2026-05-04

- **Rich Metadata Expansion**: Added 7 new columns to all CSV databases (Source URL, Source Type, Last Updated, Throughput/Latency/Cost/Complexity Tiers).
- **Decision Intelligence**: Enhanced search engine with confidence scores (High/Medium/Low) and improved domain detection.
- **Compare Mode**: New `compare` command for side-by-side analysis of architectural patterns (e.g., `compare "RabbitMQ vs Kafka"`).
- **Data Maintenance**: Added `--stale` flag to identify outdated records based on `last_updated` date.
- **Code Polish**: Major cleanup of `scripts/search.py`, removing duplicate logic and implementing a robust subcommand-based CLI.
- **Validation**: Updated `_sync_all.py` with strict schema validation for the new metadata columns.

## 0.1.0 - 2026-05-02

- Official Initial Release: Launching the Backend Arch Pro Max ecosystem.
- 333 Architecture Rules: Comprehensive dataset covering API design, database architecture, resilience, security, and observability.
- BM25 Search Engine: Lightweight reasoning engine for architectural recommendations.
- CLI Installer: One-command installation for Cursor, Claude, Windsurf, and Codex.
