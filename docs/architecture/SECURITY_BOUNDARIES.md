# Security Boundaries

This combines the implemented R1 and R2 trust boundaries with later planned boundaries. R2 contains no model or tool execution path.

1. Human input enters an untrusted request boundary.
2. Retrieved content and model output remain untrusted data.
3. R1 treats external proposals as untrusted and accepts them only through strict Pydantic discriminated unions that forbid unknown fields and mismatched argument shapes.
4. Deterministic routing produces either a validated mock proposal or a typed refusal with a stable evidence reference. Validation failures are converted to structured issues without retaining rejected input.
5. R2 policy checks occur after validation and before any future execution boundary.
6. R2 accepts only exact validated R1 decision, routing-envelope, and policy-profile instances; subclasses are rejected deliberately. It does not implicitly parse raw dictionaries or standalone proposals.
7. R2 separates `rule:` routing evidence from `policy:` policy evidence, resolves both through immutable registries, and rejects URL-like identifiers, cross-registry references, caller-created lookalikes, unknown or duplicate evidence, and inconsistent decision/evidence pairs.
8. R2 policy is deny-by-default. Combined envelopes bind the result to the exact immutable profile evaluated and reject contradictory direct construction. Outcomes express permission state only and cannot execute or approve an action.
9. A future tool gateway would own execution; models never receive unrestricted shell or direct credential access.
10. Cloud adapters require explicit approval and narrowly scoped credentials supplied outside repository content.
11. Audit output would cross a redaction boundary before being persisted.

R2 stops after a typed policy outcome. It has no executor, approval workflow, raw-request storage, or persistence. Commits, pushes, destructive mutations, runtime installation, and cloud delegation remain human-controlled operations.
