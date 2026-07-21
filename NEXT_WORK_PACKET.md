# Next Work Packet

## R2 — Evidence envelopes and policy checks

### Goal

Wrap R1 routing decisions in a minimal typed evidence envelope and apply deterministic policy checks before any future execution boundary.

### In scope

- Define typed evidence references with stable identifiers, evidence kind, and a public-or-synthetic provenance classification.
- Define a minimal decision envelope that connects a validated R1 decision to its evidence references without storing raw request content.
- Define deterministic policy outcomes for allow, refuse, and require-human-approval.
- Apply policy only to already validated R1 proposals.
- Require an allowlisted mock tool identifier and an explicit policy outcome before a proposal could reach a future executor.
- Add structured, redaction-safe policy issues and focused unit tests.
- Use only public or synthetic examples and fixtures.

### Out of scope

- Tool execution, filesystem reads, network access, shell or subprocess calls, dispatcher implementation, model runtimes, model downloads, retrieval, vector databases, MCP, HTTP, cloud adapters, or automatic cloud delegation.
- Audit persistence, production logging, retention systems, full trace storage, or raw request-content logging.
- Commits, pushes, Docker, CI, project-license selection, or model, dataset, and adapter license approval.

### Acceptance evidence

- Evidence and policy contracts are strict, frozen, and reject unknown fields.
- Every R1 success and refusal can be wrapped without losing its stable evidence references.
- Policy checks cannot receive an unvalidated dictionary-shaped proposal.
- Tests prove deny-by-default behavior, allowlist enforcement, approval-required outcomes, and absence of raw input in serialized envelopes and issues.
- Ruff, formatting, pytest, CLI status, repository verification, and diff checks pass.

### Deferred

- Executor and dispatcher design.
- Evidence persistence, retention, redaction pipeline, and audit storage.
- Runtime, model, retrieval, and cloud integration decisions.
