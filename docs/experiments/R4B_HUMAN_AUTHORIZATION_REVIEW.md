# Human R4B Authorization Review

## Status and authority boundary

Codex recommendation: `recommend_defer`

Decision: pending

Authorization status: not_authorized

This is an evidence-backed advisory review, not the human authorization record. Codex
does not make or impersonate the human decision, check authorization items, authorize
installation or execution, select OpenClaw, or create the R4C adoption decision.
Repository publication is not a human signature.

## Decision question

> May Local AI Guild conduct the bounded R4B experiment comparing OpenClaw with a
> smaller custom dispatcher under the documented isolation, tool, data, credential,
> model, budget, evidence, stop, and teardown controls?

## Entry evidence

- `docs/PUBLICATION_INDEX.md`
- `docs/experiments/R4B_ENTRY_GATE_REVIEW.md`
- `docs/experiments/R4B_AUTHORIZATION_PACKET.md`
- `docs/security/R4B_THREAT_MODEL.md`
- `docs/experiments/R4B_EXPERIMENT_RUNBOOK.md`
- `docs/experiments/R4B_TEARDOWN_AND_RESIDUE_PLAN.md`
- `docs/experiments/R4B_DATA_BUNDLE_MANIFEST.md`
- `docs/research/R4B_OPENCLAW_LICENSE_REVIEW.md`
- `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md`
- `docs/architecture/COUNCIL_RUNTIME_REQUIREMENTS.md`
- `docs/experiments/OPENCLAW_REFERENCE_RUNTIME_POC.md`
- accepted portable Council contracts, fixture, validator, and tests
- repository verification evidence

## Recommendation summary

Installation recommendation: **defer both environment creation and candidate
installation until the exact local-model route is qualified and the named
license/component conditions receive human or authorized legal acceptance**.

Execution recommendation: **defer**. Even after installation is later authorized,
execution must remain separately blocked until installed controls, network behavior,
model routing, adapter behavior, event export, deterministic verification, termination,
and teardown are independently inspected and pass.

Conditions:

1. Reconcile the local model inventory into one exact runtime-listed, locally available
   identifier and immutable artifact identity without loading or invoking it.
2. Confirm that the selected model can be transferred or acquired into the dedicated
   WSL2 boundary under an authorized provenance process without using a floating tag.
3. Obtain human or authorized legal acceptance of the OpenClaw dependency exceptions,
   exact Node distribution, model license, and either no-container operation or one
   pinned container image.
4. Produce an implementable external enforcement design for egress, process/resource
   limits, worker depth, budgets, artifact freezing, event observation, and stop.
5. Implement and inspect the adapter, event exporter, deterministic verifier, and
   teardown controls only under later separately authorized work packets.

Validity period: this defer recommendation remains current until the local-model
qualification evidence changes or any candidate, dependency, Node, model, isolation,
tool, budget, or event requirement changes. Any later approval should expire no later
than 30 days after signature and immediately on such a change.

## Candidate provenance review

### Observed official-source facts

| Field | Reconfirmed value |
| --- | --- |
| Project | OpenClaw, official `openclaw/openclaw` repository |
| Release | `v2026.7.1` |
| Package | `openclaw@2026.7.1` |
| Immutable external commit | `openclaw/openclaw/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4` |
| Release date | 2026-07-13 |
| Core license | MIT |
| Integrity | Official npm SHA-512 integrity is recorded in the release; commit signature is GitHub-verified; official release evidence and closeout artifacts are linked |
| Lock surfaces | Source `pnpm-lock.yaml` lockfile version 9.0; published `npm-shrinkwrap.json` lockfile version 3 |
| Notices | Official `THIRD_PARTY_NOTICES.md` records incorporated/adapted Pi/pi-mono code under MIT |
| Upstream trust model | One trusted operator; plugins are trusted code; host execution can occur when sandboxing is inactive; loopback is recommended |
| Supported installation | Official npm, pnpm, or bun distribution; R4B proposes only the exact npm package and integrity, never a floating version |

### Repository design decisions

- The only eligible OpenClaw candidate is `v2026.7.1` at the external commit above.
- Local AI Guild commit identities are governed separately by
  `docs/PUBLICATION_INDEX.md`.
- Node.js `24.15.0` is the proposed exact runtime if later accepted.
- Cloud routing, automatic model pull, marketplace discovery, and floating update paths
  remain disabled.
- No container image is selected; a pinned image review or an explicit no-container
  decision is required.

### Inferences

- The candidate is sufficiently immutable and documented for a later bounded
  installation review.
- Its upstream single-operator assumptions do not satisfy the Council boundary by
  themselves; external controls remain necessary.
- MIT core licensing is technically compatible with further review but is not legal or
  intended-use approval.

### Human or legal judgments

- Accept the core, dependency, Node, model, and any container obligations.
- Accept the candidate's supply-chain and native-component residual risk.
- Accept a dedicated WSL2 boundary as proportionate for public/synthetic data.
- Decide whether the later installation and execution actions are worth the operational
  burden.

## Dependency and component review

The bounded static review is recorded in
`docs/research/R4B_OPENCLAW_LICENSE_REVIEW.md`.

Key results:

- 56 direct runtime dependency declarations in `package.json`;
- 55 external direct roots in the published shrinkwrap plus internal
  `@openclaw/ai@2026.7.1`, whose official package manifest is MIT;
- one optional dependency and no declared `bundledDependencies`;
- 308 shrinkwrap package records, all with visible license identifiers;
- mostly MIT, ISC, BSD, Apache-2.0, and other permissive metadata;
- manual review required for `web-push` MPL-2.0, `jszip`'s MIT/GPL election, `pako`'s
  MIT-and-Zlib terms, `fast-sha256` Unlicense, BlueOak entries, internal packaged code,
  native/install-script surfaces, and full notice retention;
- no visible AGPL, LGPL, CDDL, EPL, SSPL, BUSL, source-available, proprietary, or unknown
  shrinkwrap identifier;
- Node.js `24.15.0` begins with MIT terms but carries its own third-party license bundle;
- no container image, digest, base image, SBOM, signature, or license bundle is yet
  selected.

Classification: `accept_with_named_condition`.

The metadata closure is adequate for human review, but Codex cannot grant legal
acceptance. An authorized human or legal reviewer must accept the exception list before
installation.

## Read-only local model inventory

No model was downloaded, loaded, converted, quantized, or invoked. No inference request
was made.

### Inventory behavior and limitation

- `ollama list`, explicitly permitted by the packet, returned no model rows but
  auto-launched Ollama background processes. Those newly started processes were
  immediately terminated. Direct manifest inspection found one complete model artifact
  and stale incomplete manifests.
- `lms ls --json` did not return within the bounded timeout. The remaining CLI process
  was terminated. Direct inspection of the configured model directory found one GGUF
  file.
- No Ollama, LM Studio, or model process remained after cleanup.

This behavior means file/manifest presence and runtime registration disagree. Model
quality and operational availability remain unverified.

### Inventory records

| Exact local identity | Runtime | Artifact identity | Quantization | Apparent size | License source and intended use | Availability | R4B assessment |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| `registry.ollama.ai/library/qwen2.5-coder:7b` | Ollama | model blob `sha256:60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463`; config `sha256:d9bb33f2786931fea42f50936a2424818aa2f14500638af2f01861eb2c8fb446` | Q4_K_M; metadata says 7.6B | 4,683,074,048 bytes, about 4.36 GiB, plus runtime and context memory | Local license layer is Apache-2.0 and matches the official Qwen2.5-Coder-7B-Instruct Apache-2.0 source; official card describes instruction-tuned coding, code-agent, and general competency use | Complete manifest/blob set is present, but `ollama list` returned no row; runtime registration is unconfirmed | Best provisional candidate; not yet an approved or executable route |
| `registry.ollama.ai/library/qwen2.5-coder:latest` | Ollama | same model and config digests as the `7b` row | Q4_K_M | same | same | complete alias present | ineligible because `latest` is floating |
| `registry.ollama.ai/library/qwen2.5-coder:14b` | Ollama | manifest declares model digest `sha256:ac9bc7a69dab38da1c790838955f1293420b55ab555ef6b4615efa1c1507b1ed` | not confirmed locally | manifest declares 8,988,110,784 bytes | manifest points to the same Apache-2.0 license layer | two required blobs missing | not locally available |
| `registry.ollama.ai/library/qwen3-coder:30b` | Ollama | manifest declares model digest `sha256:1194192cf2a187eb02722edcc3f77b11d21f537048ce04b67ccf8ba78863006a` | not confirmed locally | manifest declares 18,556,688,736 bytes | license layer is absent locally; no bounded license conclusion | four required blobs missing | not locally available |
| `apto-as/Qwen2.5-Coder-7B-Instruct-Q5_K_M-GGUF` | LM Studio model directory | `qwen2.5-coder-7b-instruct-q5_k_m.gguf`; final file digest not computed | Q5_K_M | 5,444,831,744 bytes, about 5.07 GiB, plus runtime and context memory | Derivative model card declares Apache-2.0 and links the official Qwen license; exact local file provenance still requires pre-run digest/source reconciliation | file is present; LM Studio CLI listing timed out; served model identifier is unconfirmed | inventory evidence only; not selected |

Presence does not establish model quality, tool reliability, security-review competence,
or evidence-audit competence.

## Proposed model and routing plan

Model selection status: `unresolved`

The deterministic dispatcher and verifier use no model. Cloud routing and the optional
cloud subtest remain excluded.

The only provisional local candidate is
`ollama/qwen2.5-coder:7b` pinned to model digest
`sha256:60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463`.
If a later prerequisite review confirms exact runtime registration and isolated-WSL2
availability, the same exact route must be used for all four model roles and both
runtime paths:

| Role | Provisional exact route | Location | License | Allowed data | Max context | Max output | Max invocations per path | Static memory posture | Current state | Capability risk |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| Council member A | `ollama/qwen2.5-coder:7b` at pinned model digest | local only | Apache-2.0, pending human acceptance | approved public/synthetic bundle only | 24,000 tokens | 4,000 tokens | 3 | 4.36 GiB weights plus runtime and KV cache; exact RAM/VRAM unverified | complete artifact present; route registration unresolved; transfer into WSL2 not authorized | unverified structured reasoning and tool-call reliability |
| Council member B | same | local only | same | same | 24,000 | 4,000 | 3 | same | same | same |
| Security adversary | same | local only | same | approved bundle and sanitized control evidence | 24,000 | 4,000 | 2 | same | same | security competence unverified; no model conclusion is security proof |
| Evidence auditor | same | local only | same | approved bundle and sanitized exports | 24,000 | 4,000 | 2 | same | same | citation and evidence competence unverified |
| Deterministic verifier | no model | local deterministic process | repository implementation terms | Council artifacts and bounded evidence | not applicable | not applicable | 0 | ordinary Python process | implementation prerequisite | deterministic results require external implementation and two-run comparison |
| Custom dispatcher | same role routes as above | local only | same | identical data | identical | identical | included above | identical | route unresolved | any route difference invalidates comparison |

Two additional invocations per path remain reserved within the existing 12-invocation
cap; they cannot be used unless the human authorization names their role and purpose.

Because the exact runtime-visible local route is not confirmed, this table is not an
approved model plan. The packet's `unselected` model state remains authoritative and,
under the work-packet rule, the Codex recommendation is `recommend_defer`.

## Data-bundle review

The exact proposed source inventory is
`docs/experiments/R4B_DATA_BUNDLE_MANIFEST.md`.

Classification:

- public repository architecture, policy, review, and source files;
- one repository-authored public synthetic Council fixture;
- a later derived strict packet containing no new private facts;
- no corporate, government, work-derived, personal, health, financial, email, message,
  browser, home-directory, secret, production, credential, or private-network material.

Every digest remains `TBD_PRE_RUN_SHA256` because the bundle must be frozen only after a
human selects the exact published repository revision. Data owner approval,
independent sanitization review, derived-packet validation, final content scans, and
read-only staging remain pending.

Classification: `accept_with_named_condition`.

## Dedicated-WSL2 isolation and residual-risk review

The design uses one dedicated experiment-only WSL2 distribution. WSL2 is not treated as
a complete adversarial security boundary. Windows, WSL2, the container/process layer,
and independent observers must jointly enforce and evidence the controls.

| Control | Required external mechanism | Runtime role | Evidence before execution | Residual risk and reasonableness | Classification |
| --- | --- | --- | --- | --- | --- |
| No Windows home mount | Disable automatic Windows-drive mounting and interop for the dedicated distribution; deny host paths with Windows ACLs; inspect effective mounts | OpenClaw receives no host path and cannot weaken the boundary | mount inventory, negative home/drive probes, Windows file-access observation | WSL integration or administrator error can reintroduce host paths; reasonable only for public/synthetic data with negative tests | `accept_with_named_condition` |
| Sanitized read-only repository copy | Stage a manifest-checked copy outside the user profile; mount only that copy read-only into the experiment | runtime reads approved IDs only | source commit, bundle digests, mount flags, mutation-denial test | mount or staging errors remain; reasonable with external digest and write-denial evidence | `accept_with_named_condition` |
| Separate role workspaces | Separate OS identities or container volumes and ACLs; no shared writable parent; append-only external export | runtime session separation is defense in depth | role access matrix, cross-read/write denials, file-access observation | roles share the WSL kernel and possibly runtime services; acceptable for synthetic data only if tests pass | `accept_with_named_condition` |
| Loopback-only ingress | Bind candidate services to loopback and enforce no inbound Windows/LAN path with Windows/WSL firewall boundaries | runtime configuration narrows exposure only | listener inventory from Windows and WSL, LAN-negative probe, port-forward inventory | WSL networking modes and forwarding can drift; reasonable only after effective-state inspection | `accept_with_named_condition` |
| Outbound deny-by-default | Windows/WSL egress control or an externally governed filtering proxy; no general DNS; offline execution phase | runtime network policy is not trusted | effective rules, DNS/connection log, unknown-destination denial, no-cloud reconciliation | WSL virtual networking can make process/distro attribution difficult; exact mechanism must be demonstrated | `defer` until mechanism is fixed and evidenced |
| Endpoint allowlisting by phase | Distinct time-bounded provenance/install phase allowlist; execution returns to zero egress | runtime cannot add destinations | approved endpoint manifest, phase transitions, independent connection record | encrypted approved endpoints can conceal behavior; acceptable only for installation, not execution, without further need | `accept_with_named_condition` |
| Process and resource limits | Windows VM resource envelope plus WSL/container cgroups and external wall-clock controller | runtime limits are defense in depth | CPU/RAM/process/session baseline, exhaustion/termination tests | shared-kernel accounting and child processes may evade one counter | `accept_with_named_condition` |
| No unrestricted shell | Do not expose shell/exec tools; external process allowlist and process observation; read-only runtime identity | OpenClaw tool policy is secondary | effective tool export, denied shell/interpreter cases, no-new-process result | upstream host-first defaults are dangerous if misconfigured | `accept_with_named_condition` |
| Depth-one workers | External controller owns parent/depth/session registry and denies child spawn permission | runtime may request but not decide | depth-one acceptance, depth-two denial, independent process/session graph | hidden runtime/provider delegation may remain opaque | `accept_with_named_condition` |
| Credential containment | Local-only plan uses no provider credential; package retrieval phase has no model credential | runtime sees no secret | empty credential manifest, environment/store/log scans | local marker behavior and accidental inherited credentials remain possible | `accept_as_proposed` |
| Event export | Bounded adapter export plus independent phase/control observer and completeness verifier | runtime events are supporting observations only | all 25 events, ordering, corroboration, omissions, redaction, repeated result | adapter and exporter are not implemented; execution cannot proceed | `defer` |
| Teardown and residue | Stop processes, destroy distribution/state, revoke exceptions, inspect Windows/WSL/files/network/Git against baseline | runtime teardown event is non-authoritative | item dispositions, process/listener/mount/network scans, retained-evidence digests | host/provider logs and opaque caches may persist | `accept_with_named_condition` |

The public/synthetic data boundary makes the residual risk potentially proportionate,
but two controls are not yet administratively ready: the exact external egress
mechanism and independently complete event export. Installation and execution therefore
remain deferred.

## Tool, budget, event, and teardown review

| Area | Classification | Evidence and named condition |
| --- | --- | --- |
| Minimal tool allowlist | `accept_with_named_condition` | Schema and role/phase checks are well bounded; implement an external gate and prove no arbitrary path or command argument passes. |
| Explicit denylist | `accept_with_named_condition` | Denies shell, filesystem, install, process, browser, messaging, finance, Git, mutation, skills, and unapproved network; inspect effective OpenClaw defaults and test every material denial. |
| Worker depth | `accept_with_named_condition` | Depth one and two-worker aggregate are conservative; external controller and depth-two denial required. |
| Four primary / six total sessions | `accept_as_proposed` | Conservative and equal across both paths. |
| Two rounds / one cross-review | `accept_as_proposed` | Preserves independent positions and bounds deliberation. |
| Two messages per role per round | `accept_as_proposed` | External counter must stop at the limit. |
| 12 model invocations per path | `accept_with_named_condition` | Role allocation is bounded; two reserved calls require explicit human purpose before use. |
| 160,000 input / 32,000 output tokens per path | `accept_with_named_condition` | External token accounting and 24,000/4,000 per-call limits required. |
| 120-minute wall clock / 90-minute local compute | `accept_with_named_condition` | Independent clock and forced termination required. |
| One retry; zero on boundary failure | `accept_as_proposed` | No automatic retry on security, integrity, route, data, or teardown failure. |
| 64 tool calls per path | `accept_with_named_condition` | External counter and no silent expansion. |
| Zero-dollar default cloud budget | `accept_as_proposed` | Cloud subtest remains excluded; any cloud route is a stop. |
| 25-event inventory | `accept_with_named_condition` | Event definitions are complete on paper; exporter, independent corroboration, and absence-stop behavior remain unimplemented. |
| 20 deterministic checks | `accept_with_named_condition` | Inputs and pass/fail rules are well specified; independent implementation and two matching runs remain prerequisites. |
| Human stop conditions | `accept_as_proposed` | Comprehensive and unconditional; actual named human remains pending. |
| Teardown and residue plan | `accept_with_named_condition` | Complete on paper; exact targets, baseline, destructive authority, and independent inspection must be approved later. |
| Equivalent custom-dispatcher comparison | `accept_as_proposed` | Same inputs, models, policies, limits, evidence, stops, and teardown; feature count is excluded. |

No proposed control is silently changed by this review. The unresolved model route,
egress mechanism, and event/verifier implementations are explicit blockers.

## Human stop authority

Proposed stop authority: repository maintainer and experiment operator

Named human: pending explicit human entry

The named human must be entered before any later action. The operator may stop for any
reason. A stop cannot authorize remediation, retry, wider access, additional tools,
budget expansion, or execution.

## Installation and execution separation

The later actions remain distinct:

1. create the dedicated isolation environment and install the exact pinned candidate,
   Node runtime, and approved local-model artifact;
2. inspect installed files, lifecycle effects, configuration, mounts, listeners,
   routes, tools, models, processes, controls, and teardown targets;
3. request a new human execution decision only if inspection passes.

This review recommends neither action 1 nor action 3 yet. Resolving the model-route
prerequisite may make action 1 eligible for a renewed human decision. Action 3 remains
blocked until action 2 and all external control implementations pass.

## Authorization-checklist assessment

No authoritative checklist item is checked.

| Checklist item | Evidence available | Remaining gap | Codex recommendation | Only human can decide? |
| --- | --- | --- | --- | --- |
| Entry-gate review accepted | Complete six-gate review and published recommendation | Human acceptance | technically supported | yes |
| Threat model accepted | 27 scenario rows with controls, evidence, stops, and residual risk | Human risk acceptance | accept with conditions | yes |
| Isolation design accepted | Dedicated-WSL2 design and this control review | Exact egress mechanism and installed-state evidence | defer | yes |
| Candidate version identified | Official `v2026.7.1`, package, external commit, date | Reconfirm immediately before retrieval | technically supported | final approval yes |
| Candidate provenance reviewed | Official release, signature state, integrity, metadata, notices | Recompute retrieved artifact digest later | accept with condition | final approval yes |
| License reviewed | Core, lock, exceptions, Node, container limits documented | Human/legal acceptance | requires external legal review | yes |
| Intended use reviewed | Public/synthetic, single-human bounded experiment | Human organizational/use judgment | requires human risk acceptance | yes |
| Data bundle approved | Exact proposed manifest | Final commit, derived packet, digests, owner and independent review | accept with conditions | yes |
| Sanitization approved | Public/synthetic-only boundary and scan plan | Final pre-run scan and independent reviewer | administratively incomplete | yes |
| Credential plan approved | Local-only and no-credential plan | Verify no inherited/local credential and no cloud path | accept as proposed | yes |
| Model plan approved | Complete provisional Ollama artifact and LM Studio file inventory | Runtime-visible exact route, WSL2 availability, capability risk acceptance | defer | yes |
| Cloud-routing policy approved | Cloud disabled and zero-dollar budget | Effective no-cloud evidence | accept as proposed | yes |
| Tool allowlist approved | Nine bounded operations | External implementation and denial tests | accept with conditions | yes |
| Tool denylist approved | Comprehensive prohibited surface | Installed effective-policy inspection | accept with conditions | yes |
| Budgets approved | Conservative explicit limits | Independent enforcement implementation | accept with conditions | yes |
| Event requirements approved | 25 events, ordering, corroboration, absence rules | Exporter and independent completeness evidence | defer execution | yes |
| Deterministic checks approved | 20 specified checks | Independent implementation and repeatability | defer execution | yes |
| Stop authority assigned | Role proposed | Actual person not named | administratively incomplete | yes |
| Teardown plan approved | Complete removal, retention, residue, and failure design | Exact environment targets and destructive authority | accept with conditions | yes |
| Human installation approval recorded | None | Explicit action-specific human record | blocked | yes |
| Human execution approval recorded | None | Separate approval after installed-state inspection | blocked | yes |

## Readiness classification

- **Technically supported:** candidate identity, core package metadata, portable Council
  contracts, bounded data classes, tool/budget/event specifications, and comparison
  design.
- **Administratively ready:** publication ledger and the review form; not installation
  or execution.
- **Requires human risk acceptance:** WSL2 residual risk, license exceptions, intended
  use, exact operators, data approval, and destructive teardown authority.
- **Requires external legal review:** dependency exceptions, Node/license bundle,
  model/license acceptance, and any later container image under organizational policy.
- **Unproven until experiment execution:** runtime representability, isolation results,
  event completeness, route and cost records, teardown, recovery, and value.

## Codex recommendation

`recommend_defer`

The candidate and dependency metadata are sufficiently bounded for human consideration,
and no clearly incompatible license was found. The review nevertheless cannot recommend
later installation while the only complete local model artifact is absent from the
runtime's read-only listing and the isolated-WSL2 route is not established. Execution
also lacks a fixed external egress mechanism and implemented adapter, event exporter,
deterministic verifier, and installed-state evidence.

The smallest next prerequisite is a read-only **R4B local-model route qualification**
packet. It should reconcile the complete Ollama manifest/blob identity with the
runtime-visible inventory, establish one exact local identifier for dedicated-WSL2 use,
confirm Apache-2.0 provenance and no acquisition need or define the exact later
acquisition artifact, and stop without loading or invoking the model. It must not
propose installation while the blocker remains.

Repository publication is not a human signature.

Human decision: pending

Disposition:
[ ] approve later bounded installation only
[ ] approve later bounded installation and conditional execution
[ ] defer
[ ] reject

Named operator:
Named stop authority:
Approved candidate:
Approved environment:
Approved models:
Approved routes:
Approved credentials:
Approved endpoints:
Approved tools:
Approved budgets:
Approved data bundle:
Installation action:
Execution action:
Conditions:
Validity period:
Human rationale:
Named stop authority:
Approved candidate:
Approved environment:
Approved models:
:
Decision date:
