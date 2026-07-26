# Next Work Packet

## Proposed R4B entry-gate review

This is proposed documentation-only work. It is not authorized by the portable
contract checkpoint, does not authorize R4B, and requires a separate approved packet.

### Goal

Compare the human-accepted minimum portable Council contracts with the six
runtime-adoption gates and determine whether an OpenClaw proof-of-concept packet may be
proposed for explicit human authorization.

### In scope

- Review the accepted role, work-packet, frozen-position, cross-review, evidence,
  verification, approval-request, decision-record, knowledge-promotion, and
  runtime-event contracts against each adoption gate.
- Confirm that the minimum Council flow remains representable without runtime-native
  authority or reciprocal relationship edges.
- Inventory the experiment-specific threat model, isolation design, teardown procedure,
  license review, bounded event requirements, and explicit human authorization still
  required before any runtime installation or execution.
- Record each gate as satisfied by current evidence, blocked, or requiring a separately
  authorized R4B experiment.
- Produce documentation findings and a recommendation only.

### Six gates to review

1. Minimum Council flow can be represented.
2. Isolation and permissions are acceptable.
3. Execution records are complete and inspectable.
4. Local and cloud routing and costs are visible.
5. Council artifacts remain runtime-independent.
6. Runtime value exceeds security and operational cost.

### Out of scope

- Authorizing or implementing R4B.
- Installing, downloading, configuring, or executing OpenClaw or another runtime.
- Adding a runtime adapter, model, provider, tool, worker, session, or workspace.
- Running an OpenClaw capability or security experiment.
- Selecting or adopting a runtime.
- Creating a runtime-selection ADR.
- Changing the accepted portable Council contracts.

### Acceptance evidence

- Every gate cites current repository evidence and states its remaining evidence gap.
- Contract coverage is distinguished from runtime capability evidence.
- OpenClaw remains a candidate reference runtime, not a selected or adopted runtime.
- The review explicitly states that no installation or execution is authorized.
- Any future R4B proposal names its threat model, isolation, teardown, license, data,
  credential, model, tool, budget, and human-approval boundaries.
- Documentation verification, sensitive-data scans, diff checks, and human review pass.

### Deferred

- OpenClaw POC implementation and custom-dispatcher comparison.
- Runtime installation, model configuration, adapter code, and event ingestion.
- R4C runtime adoption decision and runtime-selection ADR.

## R4B remains blocked

The portable contracts are not a runtime entry authorization. R4B remains blocked until
the contracts are accepted by a human, this documentation-only entry-gate review is
completed and accepted, and a later packet explicitly authorizes the bounded runtime
experiment, installation, and execution.
