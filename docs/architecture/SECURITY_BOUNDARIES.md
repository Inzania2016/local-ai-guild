# Security Boundaries

This combines the implemented R1 through R3 trust boundaries with later planned boundaries. R3 contains no model or tool execution path.

1. Human input enters an untrusted request boundary.
2. Retrieved content and model output remain untrusted data.
3. R1 treats external proposals as untrusted and accepts them only through strict Pydantic discriminated unions that forbid unknown fields and mismatched argument shapes.
4. Deterministic routing produces either a validated mock proposal or a typed refusal with a stable evidence reference. Validation failures are converted to structured issues without retaining rejected input.
5. R2 policy checks occur after validation and before any future execution boundary.
6. R2 accepts only exact validated R1 decision, routing-envelope, and policy-profile instances; subclasses are rejected deliberately. It does not implicitly parse raw dictionaries or standalone proposals.
7. R2 separates `rule:` routing evidence from `policy:` policy evidence, resolves both through immutable registries, and rejects URL-like identifiers, cross-registry references, caller-created lookalikes, unknown or duplicate evidence, and inconsistent decision/evidence pairs.
8. R2 policy is deny-by-default. Combined envelopes bind the result to the exact immutable profile evaluated and reject contradictory direct construction. Outcomes express permission state only and cannot execute or approve an action.
9. R3 accepts only exact validated evaluation cases and exact non-empty tuples. It revalidates unchecked case, expected-result, and policy-profile instances and rejects raw dictionaries, subclasses, mutable collections, duplicate identifiers, contradictory expectations, and caller-written mismatch metadata.
10. R3 case results and summaries are evaluator-built and recheck private, non-serialized bindings before they are trusted. Their public data retains only stable case identifiers, typed outcomes, registered evidence identifiers, bounded issue codes, and registry-owned mismatch constants; it excludes raw input, proposal arguments, exception text, timing, execution state, and machine metadata.
11. O2 parses one fixed repository TOML trace into strict exact models. The loader exposes no path parameter, and bounded errors exclude source text, parser details, resolved machine paths, and arbitrary field names.
12. O2 trusted validation rejects raw dictionaries, subclasses, and unchecked corruption. Findings and results are evaluator-built, registry-owned, deterministic, and contain no TOML source, cited content, timestamps, machine identity, or arbitrary caller prose.
13. O2 citation locators are declarations with syntax validation only. The validator does not read cited documents, inspect Git, authenticate evidence or approval, establish external truth, or turn a commit into authorization or correctness.
14. A future tool gateway would own execution; models never receive unrestricted shell or direct credential access.
15. Cloud adapters require explicit approval and narrowly scoped credentials supplied outside repository content.
16. Audit output would cross a redaction boundary before being persisted.

O2 stops after one fixed TOML read and in-memory deterministic validation. It has no model connection, executor, approval workflow, raw-request result storage, benchmark-history persistence, graph database, or generalized ontology implementation. Commits, pushes, destructive mutations, runtime installation, and cloud delegation remain human-controlled operations.

## Planned Council/runtime boundary

R4A treats every candidate runtime, including OpenClaw, as untrusted:

- Council authority, approvals, decisions, evidence rules, and promoted knowledge remain in Council-controlled durable records.
- Runtime sessions, memory, identifiers, configuration, messages, and events are non-authoritative operational state.
- Runtime permission controls are defense in depth and must be backed by independent host, network, filesystem, credential, and human-approval controls.
- Frozen independent positions must be exported before peer disclosure.
- Role workspaces and working memory must be isolated; no global shared memory is permitted for the initial POC.
- A future POC should use a dedicated WSL2 distribution or VM, loopback-only services, sanitized read-only repository content, dedicated test credentials, no Windows home mount, no unrestricted shell, no personal-account access, depth-one workers, explicit limits, and full teardown.

This design does not authorize a runtime installation or create a security boundary in software. OpenClaw remains a candidate reference runtime, not a selected, approved, or adopted runtime.
