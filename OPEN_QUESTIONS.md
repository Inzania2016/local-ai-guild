# Open Questions

Unresolved questions are not decisions or current facts.

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
