# Security Boundaries

This combines the implemented R1 validation boundary with later planned boundaries. R1 contains no model or tool execution path.

1. Human input enters an untrusted request boundary.
2. Retrieved content and model output remain untrusted data.
3. R1 treats external proposals as untrusted and accepts them only through strict Pydantic discriminated unions that forbid unknown fields and mismatched argument shapes.
4. Deterministic routing produces either a validated mock proposal or a typed refusal with a stable evidence reference. Validation failures are converted to structured issues without retaining rejected input.
5. Future policy checks must occur after validation and before any execution.
6. A future tool gateway would own execution; models never receive unrestricted shell or direct credential access.
7. Cloud adapters require explicit approval and narrowly scoped credentials supplied outside repository content.
8. Audit output would cross a redaction boundary before being persisted.

R1 stops after validated proposal or refusal. It has no executor. Commits, pushes, destructive mutations, runtime installation, and cloud delegation remain human-controlled operations.
