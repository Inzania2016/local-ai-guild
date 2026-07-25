# Execution Flow

The full target flow below is planned. R3 implements the separate deterministic routing, evidence, policy, and evaluation flow documented afterward and always stops before execution.

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

## Implemented R2 flow

1. Accept an already validated R1 successful or refused routing decision; never accept raw request text.
2. Resolve every R1 evidence string through the immutable typed routing-evidence registry.
3. Build a strict routing-decision envelope from registry-owned evidence without adding timestamps, machine identifiers, persistence metadata, or the original request.
4. Evaluate explicit deny-by-default policy precedence against the validated envelope and exact immutable profile.
5. Return a combined envelope containing the routing envelope, the exact in-memory profile evaluated, and a non-executing policy decision. Direct construction rechecks their consistency.
6. Stop. `allow` does not invoke a tool, and human approval has no workflow in R2.

## Implemented R3 flow

1. Accept one exact validated versioned evaluation case containing only public or synthetic input, an immutable policy profile, and a strict expected result.
2. Pass the authorized case input to the existing R1 router.
3. Pass the validated R1 decision and case profile to the existing R2 combined helper.
4. Compare stable routing and policy fields in the documented fixed order, suppressing refusal-reason or routed-tool comparison when routing outcomes differ.
5. Build a bounded case result bound privately to its case identifier and expected result, without copying command text, query text, document paths, proposal arguments, exceptions, timing, or execution state.
6. Aggregate a non-empty exact case tuple into an evaluator-built ordered in-memory summary that rechecks result bindings, order, and counts.
7. Stop. No tool, model, retrieval service, approval workflow, persistence layer, or ontology component is invoked.
