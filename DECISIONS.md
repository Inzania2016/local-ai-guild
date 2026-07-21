# Decisions

## R0 decisions — 2026-07-21

- Use Python 3.12 with a conventional `src` package layout; R0 verification used Python 3.12.6.
- Keep runtime dependencies empty in R0; use Ruff and pytest as development dependencies.
- Expose only a harmless `status` CLI command in R0.
- Treat deterministic scripts as sources of facts and model output as proposals requiring validation.
- Prohibit unrestricted shell tools, automatic cloud delegation, and automatic commits or pushes.
- Keep tracked configuration limited to `.example.yaml` files; ignore real local configuration.
- Keep generated evidence, traces, benchmark results, model files, runtime state, caches, and virtual environments out of Git.
- Keep the repository at `C:\dev\source\Repos\local-ai-guild`; plan `E:\AI` for active assets and `D:\AI` for archival assets.
- Defer every model and runtime choice until project-specific local evaluation exists.
- Make R1 only typed tool contracts plus a deterministic mock router, with no model connection.
- Treat the repository and its published artifacts as public; prohibit non-public or sensitive work material from commits, logs, traces, and publications.
- Use public or synthetic fixtures by default. Require sanitization, explicit repository approval, and independent review before committing any work-derived material.
- Require model, dataset, and adapter license review before adoption, with heightened attention to commercial, corporate, government, and contract-related use. Do not select a project license or approve a candidate license in R0.

Future durable architecture decisions should receive focused records under `docs/decisions/` and be summarized here.

## R1 decisions — 2026-07-21

- Use Pydantic v2 `BaseModel` contracts for validation and serialization at untrusted proposal and routing boundaries.
- Configure boundary models for strict validation, forbidden unknown fields, and frozen instances. Use discriminated unions so each tool identifier accepts only its own argument contract.
- Confine Pydantic to external validation and serialization boundaries. Deterministic routing remains ordinary typed Python, avoiding a custom general-purpose validation framework and keeping domain logic independent from validation machinery.
- Generate JSON Schema in memory from Pydantic contracts when requested; do not add a schema registry or persist generated schemas in R1.
- Define `project_status`, `search_public_docs`, and `read_public_doc` as harmless R1-only mock contracts, not production tools.
- Require every success and refusal to carry at least one stable rule evidence reference.
- Keep proposals untrusted and non-executable. R1 has no dispatcher, executor, filesystem read, network access, subprocess, or tool invocation path.
- Convert validation failures to bounded generic messages and schema-owned locations only. Do not serialize Pydantic messages or attacker-chosen location components because they may contain rejected input.
