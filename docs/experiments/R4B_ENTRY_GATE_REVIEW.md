# R4B Entry-Gate Review

## Status and scope

This is a documentation-only review of repository evidence at published baseline
`9d0e2a225f4b9c41ac4f41a8ae125c4e9ad98e11`. It determines whether a separate bounded
R4B authorization-and-experiment-design packet is ready to be proposed.

This review does not authorize R4B, runtime installation, runtime execution, model
configuration, tool access, cloud routing, or OpenClaw adoption. OpenClaw remains one
candidate reference runtime. No external research was performed, so candidate version,
license, current capabilities, and compatibility remain unresolved.

The classifications are:

- `satisfied_by_current_repository_evidence`
- `partially_supported`
- `requires_r4b_experiment`
- `blocked_by_missing_prerequisite`

Contract evidence and synthetic proceedings establish only portable representation and
deterministic repository behavior. They do not establish candidate-runtime capability,
security, completeness, or value. Runtime self-claims would not close a gate without
independent evidence and human review.

## Evidence reviewed

- `SECURITY.md`
- `PROJECT_STATE.md`
- `DECISIONS.md`
- `OPEN_QUESTIONS.md`
- `ROADMAP.md`
- `VERIFICATION.md`
- `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md`
- `docs/architecture/COUNCIL_RUNTIME_REQUIREMENTS.md`
- `docs/architecture/SECURITY_BOUNDARIES.md`
- `docs/architecture/KNOWLEDGE_PROMOTION_POLICY.md`
- `docs/experiments/OPENCLAW_REFERENCE_RUNTIME_POC.md`
- `src/local_ai_guild/council_contracts.py`
- `src/local_ai_guild/council_fixture.py`
- `src/local_ai_guild/council_validation.py`
- `tests/test_council_contracts.py`

## Gate 1 — Minimum Council flow can be represented

**Current classification:** `partially_supported`

### Repository evidence

- Ten strict, frozen, extra-forbid portable contracts represent roles, one work packet,
  frozen positions, cross-reviews, evidence, verification, approval requests, decisions,
  knowledge-promotion requests, and bounded runtime events.
- The immutable public synthetic proceeding represents two independently produced and
  frozen positions, one cross-review, deterministic verification, a human approval
  request, dissent-preserving decision, proposed knowledge promotion, and three runtime
  events.
- The deterministic validator reports that the synthetic proceeding contains 19 Council
  records, is valid, and has no issues.
- `COUNCIL_RUNTIME_BOUNDARY.md` defines the planned adapter operations while keeping
  authority outside the runtime.

### Evidence limitations

The repository proves that the minimum Council flow can be represented and checked
without a runtime. It does not prove that OpenClaw or another runtime can host the flow,
preserve phase boundaries, export frozen artifacts, or avoid changing Council semantics.

### Required R4B test

Map one structured Council work packet and two independent member sessions through the
candidate adapter. Export positions before peer disclosure, perform one cross-review,
security review, evidence audit, external verification, human decision, and durable
decision record.

### Pass condition

Every required Council artifact validates in Council-owned form; phase order and frozen
digests are preserved; runtime-native identifiers remain non-authoritative; no Council
contract or meaning is changed to fit the runtime.

### Stop or rejection condition

Stop if the runtime cannot keep initial positions independent, cannot freeze them
externally, requires runtime-native state as Council authority, silently alters artifacts,
or requires a broader Council ontology or workflow to claim success.

## Gate 2 — Isolation and permissions are acceptable

**Current classification:** `blocked_by_missing_prerequisite`

### Repository evidence

- `SECURITY.md`, `SECURITY_BOUNDARIES.md`, and `COUNCIL_RUNTIME_REQUIREMENTS.md` require
  deny-by-default, bounded, allowlisted, and audited tools with no unrestricted shell.
- The planned POC uses a dedicated WSL2 distribution or VM, loopback-only access,
  role-specific workspaces, a sanitized read-only repository, dedicated test credentials,
  no Windows home mount, no global memory, depth-one workers, explicit budgets, and full
  teardown.
- Council contracts exclude session IDs, model names, workspace paths, provider
  configuration, and runtime-native objects from authority fields.

### Evidence limitations

These are requirements and recommendations, not an approved experiment-specific threat
model, isolation design, or demonstrated enforcement. No host, network, filesystem,
credential, workspace, memory, permission, or teardown test has run.

### Required R4B test

After the threat model, isolation design, and teardown procedure receive human approval,
run negative tests for host access, network and cloud routing, cross-role workspace and
memory access, credential access, denied tools, depth-two spawning, budget exhaustion, and
post-teardown residue.

### Pass condition

Independent controls enforce the approved boundary; every prohibited action fails closed;
effective permissions are inspectable; roles cannot read one another's undisclosed state;
depth two is denied; teardown leaves only the explicitly retained Council artifacts.

### Stop or rejection condition

Stop on unauthorized network or cloud routing, permission escape, cross-role memory or
workspace exposure, credential exposure, broad host access, subagent-depth violation,
unenforced budgets, or incomplete teardown evidence.

## Gate 3 — Execution records are complete and inspectable

**Current classification:** `requires_r4b_experiment`

### Repository evidence

- `RuntimeEvent` is a bounded non-authoritative telemetry contract correlated through a
  Council-owned identifier.
- The synthetic proceeding contains deterministic portable runtime-event examples.
- Runtime requirements name inputs, outputs, permissions, tools, failures, lifecycle
  events, ordering, omissions, and deterministic serialization as required evidence.
- Durable Council artifacts remain separate from runtime-native event exports.

### Evidence limitations

Synthetic events prove only contract representation. The repository has no candidate
runtime export, completeness inventory, event ordering observation, omission analysis,
permission-decision record, failure record, or teardown event record.

### Required R4B test

Predeclare the required event inventory and schema, then reconcile the candidate runtime
export against independently observed session, disclosure, tool, permission, route,
budget, failure, termination, and teardown events. Repeat the bounded run to compare
schema and ordering stability.

### Pass condition

All required events are attributable to packet, role, phase, and operation; omissions are
explicit; ordering and serialization pass deterministic checks; runtime-native events are
retained only as supporting operational observations.

### Stop or rejection condition

Stop on a missing required event, unbounded or secret-bearing event content, unstable
identity or ordering that prevents verification, undocumented omission, or any attempt to
treat runtime telemetry as approval, correctness, or Council authority.

## Gate 4 — Local and cloud routing and costs are visible

**Current classification:** `requires_r4b_experiment`

### Repository evidence

- Runtime requirements demand an explicit model and route for every invocation, prior
  policy and human authorization for cloud use, and cost attribution by packet, role,
  round, worker, provider, model, tool, and operation.
- Existing R1-R3 policy outcomes are deterministic and non-executing; they demonstrate
  deny-by-default control-plane design but do not route a model.
- The POC design requires a routing and cost report.

### Evidence limitations

No model list, provider, local runtime, cloud adapter, pricing source, routing record,
token record, or cost record exists. No unauthorized-cloud denial has been tested.
Repository design cannot establish current OpenClaw routing or accounting behavior.

### Required R4B test

Use an explicitly approved model list and routing policy. Record the selected route and
attributable usage for every invocation, deny all unapproved cloud routes, and reconcile
the exported usage and cost report against independent observations.

### Pass condition

Every invocation has an attributable model, provider, local/cloud route, token or
equivalent usage, and material cost; unapproved cloud routing fails closed; totals
reconcile within a predeclared tolerance.

### Stop or rejection condition

Stop on an undeclared model or provider, unauthorized cloud route, missing route or cost
record, secret-bearing provider metadata, unexplained discrepancy, or inability to
disable cloud routing independently.

## Gate 5 — Council artifacts remain runtime-independent

**Current classification:** `partially_supported`

### Repository evidence

- Portable contracts use Council-owned durable identifiers and exclude runtime agent,
  session, model, workspace, provider, and OpenClaw fields.
- Frozen-position SHA-256 digests, canonical relationship direction, separate human
  approval, dissent preservation, and request-only knowledge promotion keep institutional
  meaning outside runtime state.
- Tests verify runtime-neutral contract fields, deterministic serialization, external
  frozen-position identity, and rejection of runtime authority leaks.
- The synthetic proceeding and validator require no runtime, filesystem, network,
  persistence, or OpenClaw component.

### Evidence limitations

This is strong portability evidence for current contracts and synthetic artifacts. It
does not prove that a future adapter will export complete Council-owned artifacts, avoid
runtime-only fields, preserve hashes, or leave usable durable records after teardown.

### Required R4B test

Export the complete proceeding to Council-controlled storage at each required boundary,
validate it independently, remove the candidate runtime, and verify that the artifacts
remain readable, hash-stable, authoritative, and sufficient for the human decision.

### Pass condition

All durable artifacts validate without the runtime; replacing or removing the runtime
does not require rewriting roles, packets, positions, evidence, approvals, decisions,
dissent, or promotion requests; runtime correlations remain bounded non-authoritative
references.

### Stop or rejection condition

Stop if a durable artifact depends on runtime-native identity, memory, configuration, or
object formats; if hashes or meaning change on export; or if teardown removes information
required to review the decision.

## Gate 6 — Runtime value exceeds security and operational cost

**Current classification:** `requires_r4b_experiment`

### Repository evidence

- The POC decision question explicitly compares OpenClaw with a smaller custom dispatcher.
- Required comparison dimensions include demonstrated capability, isolation,
  auditability, replaceability, complexity, attack surface, recovery, maintenance, and
  attributable cost.
- Feature count alone is excluded as a success criterion.

### Evidence limitations

No candidate version, license review, installation effort, operating cost, model cost,
maintenance burden, recovery result, teardown cost, security finding, or dispatcher
baseline has been measured. Architecture documents cannot establish net value.

### Required R4B test

Measure the bounded Council procedure against a predeclared smaller-dispatcher baseline.
Record setup, execution, review, recovery, teardown, maintenance assumptions, attack
surface, failures, human effort, and attributable runtime/model/tool cost.

### Pass condition

The candidate produces a material, reviewable orchestration benefit under predeclared
criteria while meeting every earlier gate, and the benefit justifies its measured
security, maintenance, recovery, and operational burden.

### Stop or rejection condition

Reject the candidate if it fails an earlier gate, adds authority coupling, cannot be
recovered or removed cleanly, costs cannot be attributed, operational burden is
disproportionate, or it provides no material benefit over the bounded dispatcher.

## Gate summary

| Gate | Classification | What current evidence establishes | What remains |
| --- | --- | --- | --- |
| 1. Minimum flow | `partially_supported` | Portable representation and a valid synthetic proceeding | Candidate hosting and phase behavior |
| 2. Isolation and permissions | `blocked_by_missing_prerequisite` | Required boundary and initial isolation recommendation | Approved threat model, isolation, teardown, and adversarial execution |
| 3. Execution records | `requires_r4b_experiment` | Bounded runtime-event contract and required evidence categories | Candidate export completeness and repeatability |
| 4. Routing and cost | `requires_r4b_experiment` | Explicit policy and attribution requirements | Per-invocation route, denial, usage, and cost evidence |
| 5. Runtime independence | `partially_supported` | Strong runtime-neutral contract and serialization evidence | Adapter export and post-teardown portability |
| 6. Net value | `requires_r4b_experiment` | Defined comparison question and criteria | Measured value, burden, cost, recovery, and alternative comparison |

No gate authorizes adoption. No candidate has passed a runtime-capability gate.

## Prerequisite inventory

Each prerequisite has one current disposition. Design support means the repository
already states the boundary; it does not prove implementation or enforcement.

| Prerequisite | Current disposition | Remaining evidence or action |
| --- | --- | --- |
| Approved experiment-specific threat model | requires documentation | Define assets, actors, trust boundaries, attacks, consequences, controls, and residual risk; obtain approval later. |
| Approved WSL2 or VM isolation design | requires documentation | Select one method and define independently enforced boundaries. |
| Host, network, filesystem, credential, and approval controls | requires documentation | Specify effective controls and independent inspection steps. |
| Teardown and residue-inspection procedure | requires documentation | Define termination, deletion, retained artifacts, residue scan, and failure handling. |
| Eligible OpenClaw version identified | requires external review | Identify a precise eligible version using authorized current research. |
| License and intended-use review | requires external review | Review version-specific license and use restrictions before adoption or installation authorization. |
| Public or synthetic data bundle | already supported by repository design | Prepare a bounded bundle from intentionally public or repository-authored synthetic material. |
| No sensitive or work-derived data | already supported by repository design | Apply `SECURITY.md`; exclude unclear provenance. |
| Dedicated test credentials, if needed | requires explicit human authorization | Prefer no credentials; otherwise authorize isolated, revocable test credentials only. |
| Explicit model list | requires documentation | Name exact approved models and their roles after license/use review. |
| Explicit local/cloud routing policy | requires documentation | Default to local or denied; enumerate any separately approved cloud route. |
| Explicit tool allowlist and denylist | requires documentation | Define least-privilege tools and the excluded surfaces in this review. |
| Subagent depth of one | already supported by repository design | Preserve the existing maximum and add depth-two denial verification. |
| Message, token, time, and cost budgets | requires documentation | Set per-packet, role, round, worker, and aggregate limits. |
| Required runtime-event export | requires documentation | Freeze the event inventory, schema, ordering, redaction, and omission rules. |
| Deterministic verification scripts | requires documentation | Specify checks before any implementation packet adds them. |
| Human stop authority | requires explicit human authorization | Name the authorized human and stop/resume boundary. |
| Installation and execution approval | requires explicit human authorization | A later packet must request this explicitly; this review grants none. |

## Minimum later R4B experiment boundary

The later decision question remains:

> Should the AI Council use OpenClaw as its initial reference runtime, or should it build
> a smaller custom dispatcher?

The smallest admissible experiment contains:

1. One Council-owned structured work packet using only an approved public or synthetic
   bundle.
2. Two independently isolated Council-member sessions with identical authorized inputs
   and no peer disclosure.
3. External export and freezing of both initial positions before disclosure.
4. One cross-review round over the immutable positions.
5. One isolated security-adversary review.
6. One isolated evidence-auditor review.
7. External deterministic checks over artifacts, events, permissions, routes, budgets,
   limits, and teardown.
8. A disagreement-preserving synthesis that cannot overwrite frozen positions.
9. An external human decision under named stop authority.
10. A durable Council-owned decision record outside OpenClaw.
11. Full runtime, workspace, credential, cache, memory, and isolation-environment teardown
    followed by residue inspection.
12. Comparison against the predeclared minimum custom-dispatcher baseline.

The experiment excludes autonomous coding, email, messaging channels, browser access,
personal or financial accounts, broad shell access, scheduling, persistent institutional
memory, third-party marketplace skills, unrestricted host access, and unapproved cloud
routing.

## Consolidated stop conditions

Stop immediately on:

- unauthorized network or cloud routing;
- permission escape or broad host access;
- cross-role workspace, session, or memory exposure;
- a missing required event record or undocumented omission;
- unbounded message or agent loops;
- subagent depth greater than one;
- credential or secret exposure;
- failure to freeze positions in Council-controlled storage before disclosure;
- runtime state represented as Council approval, decision, evidence authenticity, or
  institutional authority;
- a durable artifact that cannot be validated without the runtime;
- budget or termination-control failure;
- incomplete teardown or residue-inspection evidence.

Stopping preserves available sanitized evidence but grants no authority to retry with a
broader boundary.

## Recommendation

`ready_to_propose_bounded_r4b_packet`

The accepted portable contracts, deterministic synthetic proceeding, runtime-neutral
authority boundary, objective requirements, and bounded POC design are sufficient to
draft a separate R4B authorization-and-experiment-design packet. They are not evidence
that OpenClaw is suitable and do not authorize installation or execution.

The next packet must finish and obtain review of the threat model, isolation method,
independent controls, teardown procedure, candidate version, license and intended-use
review, data bundle, credentials, models, routing policy, tool policy, budgets, event
export, deterministic checks, and human stop authority. Runtime installation and
execution remain blocked until a human explicitly authorizes those actions in a later
packet.
