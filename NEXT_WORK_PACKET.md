# Next Work Packet

## R3 — Deterministic evaluation harness

### Goal

Evaluate R1 routing, R2 evidence wrapping, and R2 policy outcomes against a small versioned set of public or synthetic cases before connecting any model runtime.

### In scope

- Define strict, typed evaluation-case and expected-result contracts.
- Store a small public or synthetic case set covering successful routes, refusals, evidence resolution, allowlist refusal, approval requirements, and allowed outcomes.
- Run each case deterministically through the existing R1 router and R2 envelope/policy helpers.
- Produce an in-memory evaluation summary with exact pass/fail counts and bounded mismatch codes.
- Add deterministic serialization and focused tests for the harness.
- Keep rejected inputs and marker values out of mismatch details and evidence.

### Out of scope

- Model runtimes, model downloads, inference, fine-tuning, retrieval, embeddings, vector databases, MCP, HTTP, cloud adapters, or automatic delegation.
- Tool execution, filesystem tool access, shell or subprocess calls, dispatcher implementation, or approval workflows.
- Benchmark history persistence, trace storage, audit databases, dashboards, Docker, CI, project-license selection, or model, dataset, and adapter license approval.

### Acceptance evidence

- Evaluation contracts are strict, frozen, and forbid extra fields.
- Cases use only public or synthetic content and stable expected identifiers.
- Results prove routing, typed evidence, and policy outcomes without claiming model quality.
- Mismatch output cannot contain rejected input, query text, paths, or arbitrary caller fields.
- Ruff, formatting, pytest, CLI status, repository verification, and diff checks pass.

### Deferred

- Model selection and model-backed evaluation.
- Persistent benchmark history and reporting.
- Executor, dispatcher, approval workflow, and runtime integrations.
