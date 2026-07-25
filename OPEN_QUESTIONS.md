# Open Questions

This file separates resolved design questions from questions deferred to later packets.

## Resolved in R1

- Use Pydantic v2 at untrusted validation and serialization boundaries; do not build a custom validation framework.
- Use three R1-only mock contracts: `project_status`, `search_public_docs`, and `read_public_doc`.
- Require at least one stable opaque rule identifier on every successful or refused routing decision.

## Deferred

- Which local runtime best satisfies the eventual adapter contract on available hardware?
- Which router, coding, embedding, and reranking candidates pass project-specific evaluations?
- What thresholds justify human-approved cloud escalation?
- What retention and redaction policy should govern local traces and benchmark history?
- How should active assets move between `E:\AI` and the `D:\AI` archive without breaking provenance?
- What evidence template and reviewer role should document future model, dataset, and adapter license decisions?
- What sanitization and independent-review checklist should govern exceptional work-derived fixtures?

## Resolved in R2

- Use typed `routing_rule` and `policy_rule` references with only `public` or `synthetic` provenance metadata.
- Use immutable registries for R1 routing evidence and deterministic policy evidence; never derive identifiers from user input.
- Use a deny-by-default profile with all three R1 mock tools allowlisted and `read_public_doc` requiring human approval.
- Keep evidence authenticity, approval workflows, execution, and persistence outside R2.

## Resolved in R3

- Use an immutable Python tuple for the first ten public or synthetic evaluation cases; do not add a data-file loader or dependency.
- Reject empty evaluation batches and preserve the declared case order in results.
- Compare independently stable fields while suppressing refusal-reason and routed-tool mismatches when routing outcomes differ.
- Keep mismatch output to registry-owned constant codes and messages and keep raw case input out of results and summaries.
- Treat a passing evaluation as deterministic contract conformance only, not model evaluation or external truth.
- Defer ontology discovery and evidence-trace design to the proposed analysis-only O1 packet.
