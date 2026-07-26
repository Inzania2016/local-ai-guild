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

## Implemented O2 trace-validation flow

1. Open only the fixed repository-owned `docs/traces/r2-closeout.toml`.
2. Parse it with Python 3.12 standard-library `tomllib`.
3. Convert the TOML boundary once into exact strict, frozen trace contracts.
4. Recheck the validated document, nested evidence, identifiers, statuses, private order binding, and explicit typed relationships.
5. Produce registry-owned bounded findings in fixed order and bind the result privately to the trace identifier and ordered record identifiers.
6. Report the known missing repository approval-evidence record without inferring that approval failed or did not occur.
7. Stop in memory. Do not resolve citations, inspect Git, run verification commands, read declared artifact paths, mutate approval, execute tools, persist a trace, or expose a trace CLI command.

## Planned portable Council flow

This R4A flow is conceptual and unimplemented:

1. Validate Council-owned role contracts and one bounded work packet.
2. Ask a replaceable adapter to create isolated member sessions under externally enforced permissions and budgets.
3. Run independent analysis without peer-position disclosure.
4. Export and freeze initial positions in Council-controlled storage.
5. Deliver the immutable review bundle and collect cross-review, security-adversary, and evidence-auditor reports.
6. Run deterministic verification outside runtime authority.
7. Produce a synthesis that preserves material disagreement and uncertainty.
8. Request a human decision through a Council-owned approval format.
9. Store the decision and any approved knowledge promotion in durable runtime-independent records.
10. Export bounded runtime events for independent inspection and tear down every session and workspace.

Runtime output, memory, status, or event records cannot approve a decision or promote knowledge. OpenClaw is only a candidate reference runtime for a future R4B experiment, which cannot begin until the minimum Council contracts are defined and accepted.
