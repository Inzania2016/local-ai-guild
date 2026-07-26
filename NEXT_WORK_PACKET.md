# Next Work Packet

## Proposed checkpoint — Minimum portable Council contracts

This is proposed work only. It is not authorized by O3, does not authorize R4B, and
requires a separate approved work packet before implementation.

### Goal

Define the smallest runtime-neutral contracts required to preserve Council authority
across a replaceable runtime adapter and to make a later R4B proposal reviewable.

### Candidate contract set

- Role
- Work packet
- Frozen position
- Cross-review
- Evidence
- Verification
- Approval request
- Decision record
- Knowledge promotion
- Runtime event

### In scope

- Define strict, frozen, extra-forbid portable contracts for the candidate set.
- Keep Council identifiers and durable state independent of runtime-native objects.
- Define bounded relationships, authority fields, lifecycle states, and redaction-safe
  serialization needed by a future adapter boundary.
- Add focused public or synthetic tests for construction, corruption resistance,
  deterministic serialization, and cross-contract consistency.
- Record unresolved choices rather than selecting a runtime-specific representation.

### Out of scope

- OpenClaw installation, configuration, download, execution, or adoption.
- A runtime adapter, dispatcher, executor, worker, session, tool, or model integration.
- R4B implementation or authorization.
- Retrieval, embeddings, vector databases, graph infrastructure, or persistence.
- Automatic approval, decision, knowledge promotion, commit, or publication.
- Project-license selection or model, dataset, and adapter license approval.

### Acceptance evidence

- Every contract has a documented portable purpose and Council/runtime owner.
- No contract embeds OpenClaw or another runtime's identifiers, objects, permissions,
  sessions, memory, or configuration as authoritative Council state.
- Trusted construction and deterministic serialization boundaries are tested.
- Public or synthetic fixtures are used exclusively.
- Ruff, formatting, pytest, CLI status, repository verification, security scans, and
  diff checks pass.
- Human review explicitly accepts the minimum contracts before any R4B packet may be
  proposed.

### Deferred

- Runtime selection and the runtime-selection ADR.
- OpenClaw reference-runtime evaluation and custom-dispatcher comparison.
- Adapter implementation, runtime events ingestion, and external isolation testing.
- Persistent Council records, retrieval, and generalized ontology or graph design.

## R4B remains blocked

R4A is documentation-only and OpenClaw remains a candidate reference runtime, not a
selected or adopted dependency. O3 supplies synthetic handoff evidence but does not
itself satisfy the minimum portable-contract gate. R4B cannot begin until O3 is
accepted, the portable contracts above are separately implemented and accepted, and a
new packet explicitly authorizes the runtime experiment.
