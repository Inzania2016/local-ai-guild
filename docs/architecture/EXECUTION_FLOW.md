# Execution Flow

The full target flow below is planned. R1 implements only the separate validation flow documented afterward and always stops before execution.

1. Accept a bounded task and assign a trace identifier.
2. Classify the task and retrieve scoped evidence using deterministic facilities where possible.
3. Obtain a route or tool proposal from deterministic logic or an evaluated model candidate.
4. Validate the proposal against its discriminated typed argument schema. R1 produces a typed refusal for malformed input.
5. Refuse, request human approval, or invoke one bounded tool through the gateway.
6. Capture redacted inputs, decisions, outputs, and verification evidence.
7. Validate claims deterministically and return a result with evidence references.

No step may silently escalate to cloud execution or unrestricted shell access.

## Implemented R1 flow

1. Validate untrusted input as a strict `UserRequest`.
2. Trim the complete text and match the documented case-sensitive command grammar exactly.
3. Build the matching tool-specific argument model and discriminated proposal.
4. Return a typed success or refusal with a stable rule evidence reference.
5. Stop. No tool execution facility exists.
