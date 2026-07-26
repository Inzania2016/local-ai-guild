# Council Runtime Requirements

## Status

These are objective evaluation requirements for a future Council runtime adapter. They do not approve, adopt, install, or configure OpenClaw or any other runtime. OpenClaw remains a candidate reference runtime.

## Evaluation requirements

| Requirement | Required property | Minimum review evidence |
| --- | --- | --- |
| Role isolation | Each member receives only its authorized role, packet, evidence, tools, workspace, and peer disclosures. | Negative isolation tests and exported permission records. |
| Session isolation | Session state, messages, files, and credentials do not cross role or experiment boundaries unintentionally. | Cross-session access tests and teardown inspection. |
| Local and cloud model routing | The selected model and route are explicit for every invocation; cloud use requires prior Council policy and human authorization. | Per-call route records and denied unauthorized-cloud tests. |
| Tool-permission granularity | Permissions can be narrowed per role, session, operation, path, and lifetime with deny-by-default behavior. | Effective permission export and denied-action tests. |
| Auditability | Inputs, outputs, permission decisions, tool requests, failures, and lifecycle events can be exported for independent review. | Complete bounded event export with documented omissions. |
| Deterministic event records | Event schemas, ordering rules, identifiers, and serialization are stable enough for repeatable validation. | Repeated-run schema and ordering comparison. |
| Human approval gates | Runtime continuation can stop at a named gate, but approval identity and authority are verified outside the runtime. | Stop/resume test using a synthetic external approval record. |
| Context preservation | Authorized context survives required phase transitions without silently altering frozen Council artifacts. | Hash or canonical-content comparison across phases. |
| Cost attribution | Token, model, provider, tool, and runtime costs can be attributed to a packet, role, round, and worker. | Reconciled per-operation cost report. |
| Working-memory isolation | Runtime memory is scoped, erasable, non-authoritative, and excluded from other roles unless explicitly delivered. | Memory-boundary and teardown tests. |
| Runtime replaceability | Council contracts and durable artifacts do not depend on runtime-native identifiers, objects, memory, or configuration. | Adapter mapping review and runtime-free artifact inspection. |
| Windows and WSL2 compatibility | The evaluation can run in a documented isolated Windows/WSL2 arrangement without requiring broad host access. | Reproducible environment design and boundary inspection. |
| Bounded subagent depth | Worker spawning has an externally enforced maximum depth and cannot recursively broaden authority. | Depth-one acceptance and depth-two denial tests. |
| Bounded message loops | Per-round message count, token budget, wall-clock limit, and termination conditions are explicit and enforced. | Limit-exhaustion and forced-termination tests. |

Runtime claims require independent evidence. A runtime's own logs or status screens may contribute operational observations, but they cannot alone establish isolation, approval authenticity, completeness, or security.

## Adoption gates

All six gates require recorded evidence and human review:

1. **Minimum Council flow can be represented.** The runtime can host the portable flow without changing Council semantics.
2. **Isolation and permissions are acceptable.** Role, session, workspace, memory, credential, tool, and host boundaries pass the approved adversarial tests.
3. **Execution records are complete and inspectable.** Bounded records cover required lifecycle and permission events, with omissions documented.
4. **Local and cloud routing and costs are visible.** Every route and material cost is attributable, and unauthorized cloud use fails closed.
5. **Council artifacts remain runtime-independent.** Durable roles, packets, positions, evidence, decisions, and promoted knowledge remain externally readable and authoritative.
6. **Runtime value exceeds security and operational cost.** Measured orchestration value justifies deployment, maintenance, attack surface, and recovery burden.

Failure or uncertainty at any gate blocks adoption. Passing an early gate does not waive a later gate.

## Initial proof-of-concept isolation recommendation

If R4B is separately authorized, begin with:

- A dedicated WSL2 distribution or VM.
- Container-backed runtime services where practical.
- A loopback-only gateway.
- A separate workspace for each role.
- No Windows home-directory mount.
- A read-only sanitized repository copy.
- Dedicated test credentials.
- No unrestricted shell.
- No browser, email, financial, or personal-account access.
- No third-party marketplace skills.
- No global shared memory.
- Subagent depth of one.
- Explicit token, runtime, and message limits.
- Full teardown after the experiment.

The runtime is untrusted and cannot serve as its own security boundary. Host, network, credential, filesystem, and approval controls must be independently enforced and inspected.

## R4B readiness

The portable contract checkpoint defines the minimum Council contracts in
`COUNCIL_RUNTIME_BOUNDARY.md`; they remain pending human acceptance. R4B remains
blocked until a documentation-only entry-gate review covers all six adoption gates, an
experiment-specific threat model and teardown procedure exist, license and use
restrictions are reviewed, and a human explicitly authorizes runtime installation and
execution.
