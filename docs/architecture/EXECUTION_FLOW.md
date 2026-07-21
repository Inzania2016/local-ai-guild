# Execution Flow

The target flow is planned and not implemented in R0.

1. Accept a bounded task and assign a trace identifier.
2. Classify the task and retrieve scoped evidence using deterministic facilities where possible.
3. Obtain a route or tool proposal from deterministic logic or an evaluated model candidate.
4. Validate the proposal against policy, allowlists, typed argument schemas, and authority limits.
5. Refuse, request human approval, or invoke one bounded tool through the gateway.
6. Capture redacted inputs, decisions, outputs, and verification evidence.
7. Validate claims deterministically and return a result with evidence references.

No step may silently escalate to cloud execution or unrestricted shell access.
