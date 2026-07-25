# Project State

Last updated: 2026-07-25

## Confirmed current facts

- R0 established the repository control plane and minimal Python skeleton at commit `14f90483279b2739ea41739bdabae882666f48de`.
- R1 implements strict, frozen Pydantic v2 contracts for untrusted user requests, three tool-specific proposals, successful and refused decisions, stable evidence references, and structured validation issues.
- R1 implements a case-sensitive deterministic mock router for `status`, `search docs: <query>`, and `read doc: <repository-relative-markdown-path>`.
- The three R1 tool identifiers are harmless test contracts, not production tools. The router stops at a validated proposal or typed refusal.
- The repository path is `C:\dev\source\Repos\local-ai-guild`.
- Python is pinned to 3.12 for project work.
- The CLI remains a harmless project `status` command and now reports the R3 stage.
- Example configuration files contain no live provider or model connection details.
- Pydantic 2.13.4 is the sole runtime dependency and is confined to validation, serialization, and JSON Schema generation at untrusted boundaries.
- R1 validation issues retain stable error codes, bounded generic messages, and sanitized schema-owned locations; rejected values and attacker-chosen field names are not serialized.
- R2 implements strict typed routing and policy evidence references, immutable synthetic registries, namespace/kind separation, and a routing-decision envelope built only from exact validated R1 decision instances. Raw dictionaries, subclasses, unknown or cross-registry evidence, caller-created lookalike evidence, and semantically inconsistent rule evidence are rejected.
- R2 implements immutable allowlist profiles and explicit deny-by-default policy precedence. The default allows `project_status` and `search_public_docs`, requires human approval for `read_public_doc`, and refuses R1 refusals or unallowlisted tools. Combined envelopes include the exact immutable profile evaluated and validate the routing/profile/result relationship.
- Policy outcomes are non-executing metadata. R2 has no approval workflow, executor, raw-request storage, trace persistence, audit database, timestamping, or machine-identity fields.
- Evidence identifiers are deterministic references rather than proof of external truth; `public` and `synthetic` provenance values are metadata, not cryptographic authenticity.
- R3 implements five strict, frozen evaluation boundary models, exact-type single-case and batch runners, registry-owned bounded mismatch metadata, evaluator-built case results, and a deterministic evaluator-built in-memory summary. Trusted result and summary checks retain only private non-serialized identifier and expected-result bindings, never case input.
- The versioned R3 case set contains ten public or synthetic cases covering successful routing, routing refusals, default policy behavior, an empty allowlist, approval-free document reads, and allowlist exclusion.
- R3 comparisons use stable R1/R2 outcomes, reasons, tools, issue codes, and registered evidence identifiers. Results and summaries do not contain raw commands, queries, document paths, proposal arguments, exception text, timing, or execution state.
- R3 passing evaluations establish only conformance between the deterministic implementation and repository-owned synthetic expectations. No model was evaluated and no external correctness claim is supported.
- No AI SDK, web framework, vector database, runtime-specific dependency, MCP implementation, HTTP API, dispatcher, executor, filesystem reader, retrieval implementation, cloud integration, training pipeline, audit persistence, or Docker configuration is present.
- The repository-local environment uses Python 3.12.6 with Ruff 0.15.22 and pytest 8.4.2.
- R3 repository verification, Ruff, formatting, pytest, CLI status, deterministic case evaluation, redaction checks, and prohibited-surface scans pass as recorded in `VERIFICATION.md`.
- The authority documents establish an explicit public-repository data boundary: public or synthetic fixtures are the default, and work-derived material requires sanitization, explicit repository approval, and independent pre-commit review.
- Model, dataset, and adapter licenses require review before adoption; R0 through R3 select no project license and approve no candidate license.

## Planned, not implemented

- `E:\AI` will hold active models, runtimes, caches, and active workspace assets.
- `D:\AI` will hold archives, datasets, experiments, benchmark history, and backups.
- Candidate components and model hypotheses are described in `VISION.md` and architecture documents.

## Not validated

- No local or cloud model candidate has been evaluated.
- LM Studio, Ollama, OpenCode, llama.cpp, and cloud agents have not been configured or invoked by R0 through R3.
- The planned storage layout has not been provisioned or validated by R0.
- No project, model, dataset, or adapter license has been selected or approved.

## Current stage gate

R3 is complete in the working tree and remains uncommitted. This does not validate a model, external truth, executor, dispatcher, approval workflow, retrieval service, runtime integration, evidence authenticity, ontology, or cloud adapter. The next proposed scope is the analysis-only O1 packet in `NEXT_WORK_PACKET.md`; O1 has not begun.
