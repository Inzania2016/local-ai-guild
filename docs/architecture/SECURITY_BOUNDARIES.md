# Security Boundaries

This is a planned boundary model. R0 contains no model or tool execution path.

1. Human input enters an untrusted request boundary.
2. Retrieved content and model output remain untrusted data.
3. The policy layer may convert a proposal into a validated request only when its tool identifier is allowlisted and every argument satisfies a typed schema.
4. The tool gateway owns execution; models never receive unrestricted shell or direct credential access.
5. Cloud adapters require explicit approval and narrowly scoped credentials supplied outside repository content.
6. Audit output crosses a redaction boundary before being persisted.

Commits, pushes, destructive mutations, runtime installation, and cloud delegation remain human-controlled operations.
