# Component Model

All components below are planned unless explicitly listed in `PROJECT_STATE.md`.

- **Policy and dispatch layer:** accepts requests, applies policy, chooses a bounded route, and refuses unsupported work.
- **Tiny tool router:** proposes tool identifiers and arguments; it cannot execute tools directly.
- **Retrieval and reranking service:** gathers scoped evidence and ranks relevance.
- **Local coding worker:** performs bounded coding or documentation work inside an approved workspace.
- **Cloud escalation adapters:** expose explicit, separately authorized cloud calls.
- **Tool gateway:** validates arguments against typed schemas, checks allowlists, executes tools, and records results.
- **Evidence and audit subsystem:** connects claims to inputs, policy decisions, tool results, and verification records while applying secret-redaction rules.

R1 implements strict boundary contracts, redaction-safe validation issues, JSON Schema generation, and a deterministic mock router. The three mock tool contracts are test seams, not production tools. No dispatcher, executor, retrieval service, runtime adapter, or audit persistence exists.
