# Component Model

All components below are planned unless explicitly listed in `PROJECT_STATE.md`.

- **Policy and dispatch layer:** accepts requests, applies policy, chooses a bounded route, and refuses unsupported work.
- **Tiny tool router:** proposes tool identifiers and arguments; it cannot execute tools directly.
- **Retrieval and reranking service:** gathers scoped evidence and ranks relevance.
- **Local coding worker:** performs bounded coding or documentation work inside an approved workspace.
- **Cloud escalation adapters:** expose explicit, separately authorized cloud calls.
- **Tool gateway:** validates arguments against typed schemas, checks allowlists, executes tools, and records results.
- **Evidence and audit subsystem:** connects claims to inputs, policy decisions, tool results, and verification records while applying secret-redaction rules.

R2 adds immutable typed evidence registries, a routing-decision envelope, immutable policy profiles, profile-bound combined evaluation envelopes, and deterministic policy outcomes. R3 adds strict evaluation contracts, ten immutable public or synthetic cases, fixed-order comparison, evaluator-built bounded case results, and an evaluator-built in-memory summary. Private result bindings contain only non-serialized identifiers and expected results, not case input. Evidence, provenance, expected results, and passing evaluations are metadata or assertions rather than external proof. Exact-type trusted boundaries reject subclasses and implicit parsing. The implemented flow stops after evaluation; it does not execute or persist anything. No dispatcher, executor, approval workflow, retrieval service, runtime adapter, ontology infrastructure, or audit persistence exists.
