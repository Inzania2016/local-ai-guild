# R4B Experiment Runbook

## Status

Authorization status: `not_authorized`

Every phase in this document is proposed only. Nothing here authorizes installation,
configuration, model invocation, provider access, environment changes, or execution.
The runbook may be used only after the human decision in
`R4B_AUTHORIZATION_PACKET.md` explicitly authorizes the named actions.

The human operator has unconditional stop authority. A stop does not authorize a retry,
repair, budget increase, new route, new tool, or broader access.

## Common phase rules

- Use only the authorized immutable OpenClaw candidate and the predeclared custom
  dispatcher baseline.
- Use identical approved Council inputs, roles, model routes, budgets, tools, events,
  checks, and teardown standards for both paths.
- Keep cloud routing disabled unless the authorization record separately names and
  approves the exact route.
- Keep every role workspace separate and every durable Council artifact outside
  runtime-native state.
- Emit the required bounded event and obtain the required independent corroboration at
  every phase transition.
- Stop on any condition in the authorization packet or threat model, any failed entry
  condition, any missing required event, or any evidence conflict that cannot be
  resolved without widening scope.

## Proposed phases

| # | Phase | Entry conditions and authorized operator | Inputs | Outputs | Required evidence | Stop conditions |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Human confirms authorization record | Human operator; every checklist item needed for the requested actions is completed, exact actions are approved, decision is not pending | Reviewed authorization packet, threat model, runbook, teardown plan | External immutable authorization or rejection record | Identity, candidate, actions, environment, model/routes, tools, budgets, dates, stop authority | Missing, ambiguous, runtime-created, expired, or mismatched approval |
| 2 | Pre-run host inspection | Human or independent security operator after Phase 1 | Approved clean-state checklist | Signed pre-run inventory | Processes, listeners, mounts, routes, environment, credential stores, Git status, ignored files, WSL2/VM/container inventory | Unexpected sensitive data, listener, mount, credential, state, or inability to establish baseline |
| 3 | Isolated environment creation | Named infrastructure operator; environment creation explicitly authorized | Approved dedicated-WSL2 design and resource budget | Dedicated experiment-only WSL2 boundary | Distribution identity, mounts, users, resources, network posture, no-home proof | Different isolation mechanism, host/home exposure, broad mount, LAN ingress, unrestricted egress, or unverifiable boundary |
| 4 | Candidate provenance verification | Independent supply-chain reviewer | Official release identity and authorized retrieval source | Candidate integrity record; no execution | Exact version/tag/commit, source, recomputed package/archive digest, signature result, package/lock/component inventory | Version, digest, signature, source, license, or component mismatch |
| 5 | Runtime installation | Named installer; exact installation action separately approved | Verified candidate and isolated environment | Installed but stopped candidate | Installed-file manifest, package manager record, no service/listener/process record | Floating version, unexpected dependency/script, service, listener, network access, or host write |
| 6 | Configuration inspection | Security operator; runtime remains stopped | Generated candidate configuration and allow/deny manifests | Approved effective configuration snapshot | Diff against design, disabled integrations, role/workspace map, no secrets | Undeclared tool, skill, memory, route, integration, startup, or mutation capability |
| 7 | Network-boundary inspection | Independent network operator | Approved endpoint and phase manifest | Verified loopback/egress policy | Listener and effective ingress/egress/DNS observations plus denial probes | LAN/public listener, general egress, unknown destination, or runtime-only enforcement |
| 8 | Synthetic data staging | Data owner and independent reviewer | Approved bundle manifest and immutable source | Read-only approved bundle in isolated environment | Provenance, classification, sanitization, repository approval, digest reconciliation | Sensitive, private, work-derived, unclear-provenance, mutated, or extra material |
| 9 | Credential staging, only when separately approved | Human and credential custodian; optional cloud subtest explicitly authorized | Dedicated credential record, quota, route, endpoint, expiry | Time-bounded secret available only to route boundary | Provider-side scope/quota, injection audit, role-denial check, no Git/artifact copy | Personal/production credential, broad scope, role visibility, missing quota, or no revocation path |
| 10 | Work packet delivery | Human-controlled dispatcher | Valid packet, roles, approved evidence manifest | Identical packet delivered to isolated roles | Packet digest and `packet_delivered` per role | Unknown role, digest mismatch, extra context, peer disclosure, or delivery omission |
| 11 | Independent positions | Two member roles under external counters | Identical authorized packet/evidence; no peer position | One candidate position from each member | Session, role, evidence, model-route, budget, tool, and position events | Cross-session leakage, route/tool/budget violation, missing event, or peer knowledge |
| 12 | External freezing | External verifier, not candidate runtime | Two validated initial positions | Canonical frozen positions and digests in Council storage | Validation, canonical bytes, digest, append-only record, `position_frozen` | Invalid position, runtime-only format, overwrite, mismatch, or disclosure before both freezes |
| 13 | Cross-review | Two members after both freezes | Immutable peer bundle with both frozen positions | One review by each member targeting the other position | Bundle delivery, target validation, no-self-review, one-round/message budgets | Early/mutable bundle, self-review, wrong target, second round, or frozen-position mutation |
| 14 | Security-adversary review | Isolated security role | Approved bundle, threat model, sanitized effective-control evidence | Bounded adversarial report | Route, tool, worker, denial, budget, and report events; external control observations | New tool/route, sensitive data, permission escape, unbounded testing, or unsupported security pass claim |
| 15 | Evidence-auditor review | Isolated auditor role | Council artifacts, provenance manifest, sanitized runtime evidence | Bounded evidence report | Claim-to-evidence matrix, omission list, source classification, report event | Runtime log treated as sole proof, unsupported claim, provenance gap, or sensitive export |
| 16 | Deterministic verification | External verifier with read-only inputs | Frozen Council bundle, event export, independent observations, budgets | Deterministic result set | Two matching runs, contract/digest/event/route/tool/isolation/budget results | Nondeterminism, missing input, failed required check, runtime dependence, or unknown correlation |
| 17 | Dispatcher comparison | Human-controlled comparison operator | Same verified inputs and criteria from both runtime paths | Bounded side-by-side comparison | Manifest-equality result, criteria scores with evidence, deviations and costs | Asymmetric inputs/controls, feature-count scoring, unverified path, or hidden deviation |
| 18 | Dissent-preserving synthesis | Human-controlled synthesis step or approved bounded role | Frozen positions, reviews, reports, verification, comparison | Synthesis retaining disagreements and uncertainty | Trace to immutable source IDs; explicit dissent and failed criteria | Overwrite, omission, false consensus, runtime authority, or unsupported conclusion |
| 19 | Human decision | Named human operator only | Complete bounded evidence package | Approve, reject, or defer experiment conclusion | External decision with rationale, dissent, limitations, and follow-up conditions | Missing evidence, unresolved failure, runtime-created approval, or pressure to decide |
| 20 | Durable external record | Council record custodian | Human decision and approved evidence manifest | Runtime-independent R4C input package | Contract validation, digests, readability, retention/redaction approval | Runtime-native dependency, secret, mutable source, missing dissent, or unreadable artifact |
| 21 | Runtime termination | Human or infrastructure operator immediately after Phase 20 or any stop | Process/session/container inventory | All experiment execution stopped | Termination events plus independent process/listener inspection | Surviving process, worker, session, listener, retry, or auto-restart |
| 22 | Teardown | Infrastructure and credential operators | Teardown manifest and retained-evidence allowlist | Removed or invalidated runtime environment and credentials | Item-by-item disposition, credential revocation, environment destruction/quarantine | Unapproved retention, inability to revoke/remove, evidence at risk, or unsafe deletion ambiguity |
| 23 | Residue inspection | Independent reviewer not relying on runtime logs | Pre-run baseline, teardown record, retained-evidence manifest | Residue report | Windows, dedicated WSL2, containers, files, stores, environment, processes, listeners, routes, Git, ignored-file comparison | Any unapproved process, file, secret, route, mount, listener, config, cache, or unknown residue |
| 24 | Evidence closeout | Human operator and evidence custodian | Complete evidence and residue report | Closed or failed experiment record | Final manifest, scan results, cost/route report, failure status, decision, R4C eligibility | Missing evidence, incomplete teardown, secret/private detail, unresolved mismatch, or premature success claim |

## Required runtime-event envelope

Each event must contain:

- one Council-owned correlation ID for the experiment, packet, role, artifact, or
  operation as applicable;
- a fixed `event_kind`;
- `outcome` from a bounded success, denied, failed, stopped, or completed set;
- a bounded registry-owned `detail_code`, never free-form secrets or host details;
- the declared producer;
- a reference to required external corroboration;
- a monotonically ordered sequence within the producing stream and declared
  happens-before references across streams.

Runtime identifiers may appear only as bounded non-authoritative correlation metadata.
Unknown Council correlations, duplicate event identities, contradictory outcomes,
unbounded detail, and secret-bearing events fail validation.

## Required event inventory

| Event kind | Required producer | Required external corroboration | Required ordering relationship | Absence stops? |
| --- | --- | --- | --- | --- |
| `experiment_started` | external controller | Human authorization and pre-run baseline IDs | First execution event; after approval and boundary inspection | yes |
| `session_created` | adapter or dispatcher | Independent session/process inventory | After experiment start; before role assignment | yes |
| `role_assigned` | adapter or dispatcher | Council role contract and workspace mapping | After its session creation; before packet delivery | yes |
| `packet_delivered` | adapter or dispatcher | Packet digest in role workspace | After role assignment; before any position | yes |
| `evidence_delivered` | adapter or dispatcher | Evidence manifest and role-visible file digest | After packet delivery; before dependent output | yes |
| `position_submitted` | member adapter | Valid exported position bytes | After authorized input; before position freeze | yes |
| `position_frozen` | external freezer | Canonical digest and append-only storage record | After submit; both freezes before peer delivery | yes |
| `peer_bundle_delivered` | adapter or dispatcher | Bundle digest and both frozen-position IDs | After both freezes; before cross-review | yes |
| `cross_review_submitted` | member adapter | Valid review and non-self target result | After peer bundle; before synthesis | yes |
| `worker_requested` | requesting role adapter | External worker-budget/depth decision | After role assignment; before create or deny | yes when a worker path is tested |
| `worker_created` | adapter or dispatcher | Independent session/process and depth inventory | After allowed request; before worker output | yes for an allowed request |
| `worker_denied` | adapter or dispatcher | External denial and unchanged session inventory | After disallowed request; no child may follow | yes for depth-two and over-budget tests |
| `tool_requested` | role adapter | Schema-valid request captured at external gate | Before exactly one allow or deny | yes for every tool attempt |
| `tool_allowed` | external tool gate | Effective role/phase policy and operation result | After request; before side effect and completion | yes for allowed operations |
| `tool_denied` | external tool gate | Denial reason and no-side-effect observation | After request; no operation result may follow | yes for required negative tests |
| `model_route_selected` | external route gate | Exact approved model/provider/route and usage record | Before every model invocation | yes for every invocation |
| `cloud_route_denied` | external route gate | Network/provider observation and no invocation | After unauthorized test request; no cloud call follows | yes for required denial test |
| `budget_threshold_reached` | external budget controller | Independent counter at 80 percent | Before exhaustion or completion | yes when threshold is reached |
| `budget_exhausted` | external budget controller | Counter and forced denial/termination | After threshold; before stopped operation | yes when a limit is tested or reached |
| `approval_gate_reached` | external controller | Pending external human decision record | After complete evidence; before human decision-dependent continuation | yes |
| `session_terminated` | adapter or dispatcher | Independent process/session inventory | After role completion or stop; before teardown complete | yes |
| `teardown_started` | external controller | Teardown manifest and runtime termination evidence | After termination or stop; before deletion/invalidation | yes |
| `teardown_completed` | external controller | Item-by-item disposition and credential revocation | After teardown start; before residue completion | yes |
| `residue_inspection_completed` | independent reviewer | Signed residue report and retained-evidence manifest | After teardown completion; before closeout | yes |
| `experiment_stopped` | external controller | Stop reason, termination, and preserved-evidence record | Final execution event on stop; may precede teardown lifecycle events in a separate teardown stream | yes on any stop |

Event absence is a stop condition where marked. An event emitted without required
corroboration remains incomplete. A runtime log line with a similar label does not
satisfy the contract by itself.

## Deterministic verification plan

These checks are specifications only; this packet implements no verifier.

| Check | Input | Expected evidence | Pass condition | Failure condition | Runtime contribution | Independent evidence required |
| --- | --- | --- | --- | --- | --- | --- |
| Council contract validation | Complete Council bundle | Deterministic issue list from two runs | Both runs valid and byte-identical | Any issue, difference, or runtime-native authority field | May export candidate artifacts | External schema implementation and read-only bytes |
| Frozen-position digest comparison | Submitted and frozen position bytes | Canonical bytes and SHA-256 records | Submit/freeze/post-review digests match | Any mismatch or missing bytes | May emit submit metadata | External canonicalizer, digest, and storage record |
| Cross-review target validation | Frozen positions and reviews | Target/member mapping | Each member reviews the other frozen position exactly once | Self-review, unknown target, duplicate, or wrong round | May export review | External contract and identity mapping |
| No self-review | Roles, positions, reviews | Role-to-target matrix | No author targets own position | Any self target or ambiguous identity | None authoritative | Council IDs and external verifier |
| Human approval separation | Approval request, runtime events, human record | Authority comparison | Only external human record authorizes action | Runtime/session/publication treated as approval | May report gate reached | External identity-bound approval record |
| Dissent preservation | Positions, reviews, synthesis, decision | Claim/source mapping | Material disagreement remains explicit and immutable | Dissent removed, rewritten, or falsely resolved | May propose synthesis | Frozen sources and human review |
| Runtime-event completeness | Declared inventory and export | Expected/observed matrix | Every applicable event and corroboration present | Missing, extra unknown, secret-bearing, or unsupported event | Supplies supporting export | External phase and control observations |
| Event ordering | Valid events | Happens-before graph and stream sequences | All declared relations hold without cycle | Reversal, duplicate, gap, contradiction, or cycle | Supplies timestamps/sequences | External phase records and canonical ordering rules |
| Unknown correlation detection | Events and Council registry | Unknown-ID issue list | No unknown or runtime-authoritative correlation | Any unresolved ID or authority substitution | Supplies correlation fields | Council-owned ID registry |
| Unauthorized cloud-route detection | Route events, network and provider records | Reconciled per-invocation route table | Exact approved route or independently proven denial | Unknown model/provider/endpoint or unrecorded connection | May report route | Network observation and provider-side usage |
| Tool-denial evidence | Tool requests/decisions and side-effect observation | Required denial matrix | Every denied action fails with no side effect | Missing denial, success, partial side effect, or runtime-only claim | May report policy result | External gate, filesystem/process/network observations |
| Subagent-depth enforcement | Worker events and session inventory | Depth graph | Maximum depth 1; depth-two request denied | Hidden, recursive, uncorrelated, or depth-two worker | May report worker tree | External controller and process/session inventory |
| Budget enforcement | Counters, events, termination records | Per-role/path aggregate table | All usage within limits; tested exhaustion stops | Overrun, silent expansion, missing metric, or continuation | May export usage | External clock, process, tool, route, and billing counters |
| Cross-role filesystem isolation | Workspace manifests and negative tests | Access decisions and file audit | Roles access only authorized roots and immutable deliveries | Cross-role read/write or shared mutable state | May report denial | OS/mount policy and file-access observation |
| Cross-session memory isolation | Canary inputs and outputs | Canary visibility matrix | Canary appears only in owning session until explicit delivery | Undisclosed canary leakage or global memory | May export memory/session metadata | Controlled canaries and external transcript comparison |
| Credential residue inspection | Injection manifest, stores, files, logs, provider | Secret-scan and revocation records | No secret outside gate; credential invalidated | Secret exposure, active credential, or uninspectable store | May export redacted state | Provider revocation and independent scans |
| Network-boundary inspection | Endpoint manifest and connection/DNS/listener records | Destination and denial table | Loopback ingress and only phase-approved egress | LAN/public listener or unknown/silent destination | May export network status | External network controls and observations |
| Teardown completion | Pre-run baseline, teardown manifest, post-run inventory | Item disposition and residue report | Only approved durable evidence remains | Any unexplained process, listener, file, mount, rule, secret, config, cache, or state | May emit teardown events | Independent host/environment inspection |
| Runtime-free readability | Retained evidence after runtime removal | Schema and digest results | All durable evidence reads and validates without candidate runtime | Runtime dependency, missing field, changed digest, or opaque format | None required | Council formats and external verifier |
| Comparison equivalence | Both path manifests and results | Input/control equality report | Same packet, roles, evidence, routes, budgets, tools, events, checks, stops, teardown | Material asymmetry or undocumented deviation | Each path exports observations | External manifest comparison |

Every failure stops the affected path. Failures may be recorded as findings; they may
not be reclassified as passes because the runtime reports healthy status.

## Equivalent OpenClaw and dispatcher comparison

Both paths receive the same:

- work packet, roles, evidence, model identifiers and routes;
- role/session structure and phase ordering;
- tool allowlist/denylist and external boundaries;
- worker, message, token, time, compute, retry, tool, and cost limits;
- event inventory, schemas, ordering, omissions, and redaction rules;
- deterministic checks, stop conditions, teardown, and residue standard.

The comparison record must address:

| Dimension | Required measure |
| --- | --- |
| Council-flow representability | Valid artifacts and phase completion without semantic changes |
| Isolation | Negative-test results and independently enforced boundaries |
| Permission granularity | Smallest effective role/operation/path/lifetime policy |
| Event completeness | Required events, omissions, ordering stability, corroboration |
| Determinism | Repeatable serialization, validation, and boundary behavior |
| Frozen-artifact preservation | Digest stability before and after disclosure and teardown |
| Runtime replaceability | Runtime-free readability and absence of native authority |
| Recovery | Bounded failure handling without authority or scope expansion |
| Teardown | Time, completeness, residue, and retained-evidence portability |
| Operational complexity | Human steps, components, configuration surface, and failure modes |
| Attack surface | Enabled components, dependencies, listeners, tools, and trust assumptions |
| Maintenance burden | Update, vulnerability, compatibility, and operational work |
| Local resource usage | Attributed CPU, memory, storage, and duration |
| Cloud cost | Exact route, tokens/usage, provider record, and total spend |
| Human supervision burden | Review, approval, monitoring, intervention, and closeout effort |
| Demonstrated value | Material orchestration benefit over minimum dispatcher under equal controls |

Missing evidence is not neutral; it is a failed or unresolved dimension. Adoption cannot
follow directly from this comparison. R4B evidence may only become input to a separate
R4C human decision.

## Evidence closeout states

The final experiment record must be exactly one of:

- `completed_for_r4c_review`: all required phases and checks completed, teardown passed,
  and no unresolved stop condition remains;
- `stopped_with_preserved_evidence`: a stop occurred, safe evidence and teardown results
  are retained, and no retry is authorized;
- `failed_teardown`: teardown or residue inspection is incomplete; this is an experiment
  failure and blocks R4C;
- `rejected_before_execution`: the human or a prerequisite review declined the
  experiment and no installation or execution occurred.

The runtime cannot choose or change the closeout state.
