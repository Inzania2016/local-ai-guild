# Council Runtime Boundary

## Status and purpose

This document defines the design boundary between the portable AI Council and any runtime used to host it. R4A established the architecture; the portable contract checkpoint now implements the minimum institutional Python contracts. It does not implement a Council workflow, runtime adapter, adoption decision, or authorization to install or execute a runtime.

The Council is the portable institutional layer. OpenClaw is a candidate reference runtime only. The Council must remain representable without OpenClaw, and replacing a runtime must not change Council authority, semantics, or durable records.

## Ownership boundary

The Council owns:

- Ontology and terminology.
- Role contracts.
- Work-packet schemas.
- Deliberation procedures.
- Evidence requirements.
- Verification rules.
- Approval rules.
- Decision-record formats.
- Knowledge-promotion rules.
- Audit standards.

A runtime adapter owns:

- Agent creation.
- Session management.
- Model configuration.
- Tool wiring.
- Subagent spawning.
- Scheduling.
- Runtime permissions.
- Runtime events.
- Runtime-specific messaging.

Runtime identifiers, session objects, memory records, configuration files, event streams, and internal message formats are operational details. They cannot become authoritative Council state. A durable Council record may retain a bounded runtime correlation reference for audit purposes, but that reference conveys no institutional authority.

## Runtime-neutral Council concepts

These names define institutional responsibilities. The checkpoint implements the
minimum set in `council_contracts.py`; deliberation orchestration and runtime behavior
remain unimplemented.

| Concept | Council meaning |
| --- | --- |
| `RoleContract` | Durable role purpose, obligations, independence rules, evidence duties, permissions requested, and prohibited behavior. |
| `CouncilWorkPacket` | Bounded decision question, scope, constraints, required outputs, evidence standard, review plan, and approval conditions. |
| `DeliberationRound` | One ordered Council procedure with declared participants, inputs, outputs, limits, and completion conditions. |
| `FrozenPosition` | A member's initial analysis produced without access to peer positions and represented by an immutable Council-owned content digest before cross-review. |
| `CrossReview` | A review of frozen positions that identifies agreements, disagreements, missing evidence, and invalid reasoning without rewriting the originals. |
| `CouncilEvidence` | A bounded evidence declaration with locator, provenance, and epistemic classification kept separate. |
| `VerificationRecord` | A deterministic or explicitly human verification record with method, subject, result, limitations, and evidence. It has no approval authority. |
| `ApprovalRequest` | A request for a named human decision with scope, alternatives, evidence, consequences, and a durable response requirement. |
| `DecisionRecord` | The durable external statement of the human decision, rationale, dissent, evidence considered, authority, and effective scope. |
| `KnowledgePromotionRequest` | A proposal to move non-authoritative material into a more authoritative knowledge class under the knowledge-promotion policy. |
| `RuntimeEvent` | A bounded runtime-reported operational observation, such as session creation or tool denial. It is not evidence of Council approval, correctness, or authority by itself. |

`CouncilProceeding` groups one exact in-memory packet and its related contracts for
deterministic validation. It is not a persistent record store or workflow engine.

## Canonical relationship direction

Each relationship is stored once on the contract that makes the assertion:

- A packet names participant roles.
- A frozen position names its packet and author role.
- A cross-review names one frozen position, its reviewer role, and supporting evidence.
- Verification, approval, decision, and promotion records name their required inputs.
- A runtime event names only its Council correlation target.

Reverse navigation is derived and non-authoritative. The contracts do not require
reciprocal duplicate edges. This prevents reciprocal-edge drift and resolves the
manual-only publication-reciprocity question identified by O3.

## Conceptual adapter operations

The following operations describe the minimum boundary a future adapter may need to satisfy. They are design concepts only:

```text
create_member_session
deliver_work_packet
run_independent_round
freeze_submission
deliver_review_bundle
spawn_bounded_worker
collect_runtime_events
terminate_session
```

- `create_member_session` creates an isolated runtime session from a Council-owned `RoleContract` and bounded runtime policy.
- `deliver_work_packet` transmits an immutable Council packet representation without transferring authority to the runtime.
- `run_independent_round` permits only the inputs authorized for the independent phase.
- `freeze_submission` exports a position to Council-controlled durable storage and prevents later runtime mutation from replacing it.
- `deliver_review_bundle` provides frozen positions and bounded evidence for cross-review.
- `spawn_bounded_worker` creates a temporary worker with narrower permissions, depth, budget, lifetime, and output contract than its parent.
- `collect_runtime_events` exports bounded operational events for independent inspection; the runtime cannot certify its own compliance.
- `terminate_session` ends the runtime session and triggers cleanup under an external teardown procedure.

No operation authorizes tool execution, cloud use, publication, knowledge promotion, or acceptance of a decision unless the applicable Council rule and human gate independently permit it.

## Minimum portable flow

A runtime must be able to represent this sequence without redefining it:

1. Validate a Council-owned work packet and role contracts.
2. Create isolated member sessions under externally supplied limits.
3. Deliver identical authorized packet content to independent members.
4. Collect and freeze initial positions before peer disclosure.
5. Deliver a review bundle containing immutable initial positions.
6. Collect cross-reviews, security review, and evidence audit.
7. Run deterministic verification outside the runtime's authority boundary.
8. Produce a disagreement-preserving synthesis.
9. Request a human decision without treating runtime output as approval.
10. Store the decision and any promoted knowledge in durable Council-controlled records.
11. Collect bounded runtime events and tear down the experiment.

## Portability invariants

- Council identifiers are generated and interpreted by Council contracts, not by a runtime.
- Council artifacts remain readable and reviewable without a running runtime.
- Runtime events are observations subject to external verification.
- A runtime may cache working context but cannot promote it to durable Council knowledge.
- Independent positions are frozen in Council-controlled storage before review.
- Tool and model permissions are derived from Council policy and enforced again outside the model.
- Human approval authenticity cannot be delegated to the runtime.
- Runtime replacement must not require rewriting Council decisions, evidence, roles, or work packets.

## R4B entry condition

The checkpoint defines the minimum Council contracts needed for the portable flow.
R4B still cannot begin until a human accepts them and a separate documentation-only
entry-gate review determines whether a bounded runtime experiment may be proposed.

## Non-goals

R4A does not select OpenClaw, define a runtime-selection ADR, install a runtime, implement an adapter, configure a model, execute an agent, grant tool access, or move Council authority into runtime state.
