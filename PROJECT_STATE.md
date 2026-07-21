# Project State

Last updated: 2026-07-21

## Confirmed current facts

- R0 established the repository control plane and minimal Python skeleton at commit `14f90483279b2739ea41739bdabae882666f48de`.
- R1 implements strict, frozen Pydantic v2 contracts for untrusted user requests, three tool-specific proposals, successful and refused decisions, stable evidence references, and structured validation issues.
- R1 implements a case-sensitive deterministic mock router for `status`, `search docs: <query>`, and `read doc: <repository-relative-markdown-path>`.
- The three R1 tool identifiers are harmless test contracts, not production tools. The router stops at a validated proposal or typed refusal.
- The repository path is `C:\dev\source\Repos\local-ai-guild`.
- Python is pinned to 3.12 for project work.
- The CLI remains a harmless project `status` command and now reports the R1 stage.
- Example configuration files contain no live provider or model connection details.
- Pydantic 2.13.4 is the sole runtime dependency and is confined to validation, serialization, and JSON Schema generation at untrusted boundaries.
- R1 validation issues retain stable error codes, bounded generic messages, and sanitized schema-owned locations; rejected values and attacker-chosen field names are not serialized.
- No AI SDK, web framework, vector database, runtime-specific dependency, MCP implementation, HTTP API, dispatcher, executor, filesystem reader, retrieval implementation, cloud integration, training pipeline, audit persistence, or Docker configuration is present.
- The repository-local environment uses Python 3.12.6 with Ruff 0.15.22 and pytest 8.4.2.
- R1 closeout verification, Ruff, formatting, 62 pytest tests, CLI status, diff checks, and execution-surface audits pass as recorded in `VERIFICATION.md`.
- The authority documents establish an explicit public-repository data boundary: public or synthetic fixtures are the default, and work-derived material requires sanitization, explicit repository approval, and independent pre-commit review.
- Model, dataset, and adapter licenses require review before adoption; R0 selects no project license and approves no candidate license.

## Planned, not implemented

- `E:\AI` will hold active models, runtimes, caches, and active workspace assets.
- `D:\AI` will hold archives, datasets, experiments, benchmark history, and backups.
- Candidate components and model hypotheses are described in `VISION.md` and architecture documents.

## Not validated

- No local or cloud model candidate has been evaluated.
- LM Studio, Ollama, OpenCode, llama.cpp, and cloud agents have not been configured or invoked by R0.
- The planned storage layout has not been provisioned or validated by R0.
- No project, model, dataset, or adapter license has been selected or approved.

## Current stage gate

R1 is complete in the working tree and remains uncommitted. This does not validate a model, tool executor, retrieval service, runtime integration, or cloud adapter. The next proposed scope is R2 in `NEXT_WORK_PACKET.md`; R2 has not begun.
