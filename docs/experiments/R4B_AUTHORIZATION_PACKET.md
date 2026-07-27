# R4B Authorization Packet

## Status

Authorization status: `not_authorized`

This document is a proposal for human review. It does not authorize downloading,
installing, configuring, starting, or testing OpenClaw; creating agents or sessions;
downloading or invoking models; connecting a provider; creating or injecting
credentials; changing WSL2, virtual-machine, container, host, firewall, or network
configuration; executing the proof of concept; selecting or adopting OpenClaw; or
creating the R4C runtime-selection ADR.

Repository publication is not runtime authorization. Only a later explicit human
decision may authorize the separately identified installation and execution actions.

## Decision requested

> May Local AI Guild conduct the bounded R4B experiment comparing OpenClaw with a
> smaller custom dispatcher under the documented isolation, tool, data, credential,
> model, budget, evidence, stop, and teardown controls?

The decision is whether to authorize one bounded experiment, not whether to adopt a
runtime. R4C remains the only runtime-selection stage.

## Experiment question and alternatives

The experiment asks whether OpenClaw can represent the accepted portable Council flow
with adequate isolation, permission granularity, event evidence, artifact portability,
cost visibility, teardown, and demonstrated value compared with a smaller dispatcher.

The equivalent alternatives are:

1. OpenClaw `v2026.7.1` behind a bounded Council adapter.
2. A smaller custom dispatcher implementing only the portable operations required by
   the same proceeding.
3. Reject or defer both when a required boundary cannot be enforced or evidenced.

Feature count is not a success metric. The same packet, roles, evidence, model routes,
budgets, tool policy, events, deterministic checks, stop conditions, and teardown
standard apply to both runtime paths.

## Scope

The proposed experiment contains one public or synthetic Council packet, two isolated
Council-member sessions, externally frozen initial positions, one cross-review round,
one security-adversary session, one evidence-auditor session, deterministic external
verification, a dissent-preserving synthesis, an external human decision, a durable
Council-owned record, and teardown with residue inspection.

It may evaluate only the minimum operations defined in
`../architecture/COUNCIL_RUNTIME_BOUNDARY.md`. It must not change the accepted portable
contracts to fit either runtime.

## Explicit exclusions

The experiment excludes autonomous coding, unrestricted shell or filesystem access,
host configuration, package-management tools, browser automation, email, messaging,
calendar or scheduling, financial systems, personal accounts, private connectors,
third-party marketplace skills, global memory, Git publication, production services,
production or personal credentials, broad network access, runtime self-modification,
and runtime-native approval or institutional authority.

This packet does not implement the adapter, dispatcher, controls, event exporter,
deterministic verifier, or teardown automation.

## Proposed environment

The selected design for human review is:

```text
Windows 11 host
└─ Dedicated experiment-only WSL2 distribution
   └─ Container-backed runtime services where practical
      └─ Loopback-only gateway
```

A dedicated VM is a rejected fallback for this packet because changing isolation
mechanisms would require a revised threat and teardown review. The proposed WSL2
boundary must provide:

- no Windows home-directory mount and no broad host mount;
- one sanitized read-only repository copy;
- a distinct writable workspace for each role and no shared writable role workspace;
- loopback-only exposure with no inbound LAN access;
- outbound deny-by-default with explicit endpoint allowlisting only when separately
  approved;
- no unrestricted shell, browser, email, messaging, financial, personal-account,
  scheduling, marketplace-skill, or global-memory capability;
- dedicated disposable credentials only after separate authorization;
- subagent depth exactly one, with depth two denied independently;
- full environment teardown after the experiment.

Filesystem boundaries, network denial, credential containment, process limits, resource
budgets, workspace separation, and termination must be enforced outside OpenClaw where
practical. OpenClaw, models, agents, sessions, tools, skills, memory, and logs are
untrusted.

The complete proposed controls are in
`../security/R4B_THREAT_MODEL.md`; no host-configuration procedure or command is
authorized by this document.

## Candidate runtime identity

### Proposed candidate

| Field | Record |
| --- | --- |
| Project | OpenClaw, official `openclaw/openclaw` repository |
| Candidate | `v2026.7.1` / package `openclaw@2026.7.1` |
| Immutable commit | `2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4` |
| Release date | 2026-07-13 |
| Source | [Official release](https://github.com/openclaw/openclaw/releases/tag/v2026.7.1) and [immutable commit](https://github.com/openclaw/openclaw/commit/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4) |
| Runtime description | Upstream describes OpenClaw as a personal AI assistant and local-first agent infrastructure for one trusted operator. |
| Core license | MIT |
| License-review status | Official core and incorporated-code facts recorded; dependency, model, provider, intended-use, and legal approval remain pending human review. |
| License files | [LICENSE](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/LICENSE) and [THIRD_PARTY_NOTICES.md](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/THIRD_PARTY_NOTICES.md) |
| Intended-use status | The proposed single-human isolated evaluation appears technically aligned with upstream's stated one-operator posture; this is an inference, not approval for commercial, corporate, government, client, or contract use. |
| Package metadata | [package.json](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/package.json) identifies version `2026.7.1`, license `MIT`, and supported Node ranges. |
| Security source | [SECURITY.md](https://github.com/openclaw/openclaw/blob/2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4/SECURITY.md) |
| Known distribution | Official npm package, with npm, pnpm, and bun described as supported installation mechanisms. |
| Integrity metadata | The official release records npm integrity `sha512-ge/Xss99CHAjPL/ikmH/UFoiOrjcxDB4sW3y9mhyCD+dYW3wzV7TKbAVdkrXFgAG2d2BjpJofP97zUZ+umxo8g==`, the immutable commit above, and a GitHub-verified commit signature. |
| Release evidence | The release links an [official CI evidence report](https://github.com/openclaw/releases/blob/main/evidence/2026.7.1/release-evidence.md) and publishes a closeout manifest whose GitHub asset digest is `sha256:6008256adcfcf7d3e181a91840123597284dbf5fb78fba28949bd9f2024360ed`. |

No candidate artifact was downloaded, so no package, archive, or asset digest has been
independently recalculated by this repository.

### Fact, decision, inference, and unresolved status

- **Observed official-source facts:** the official release, tag, commit, release date,
  package version, core MIT license text, package metadata, upstream security posture,
  distribution mechanism, signature state, and published integrity metadata above.
- **Repository design decision:** propose only the immutable stable `v2026.7.1`
  candidate; reject floating `latest` and prerelease tags for R4B.
- **Inference, not approval:** MIT contains no field-of-use restriction, and the proposed
  one-human isolated evaluation is closer to upstream's stated one-operator trust model
  than a shared gateway. This does not establish legal, security, commercial,
  corporate, government, or contract-use suitability.
- **Unresolved human-review items:** verify the candidate identity and integrity before
  any installation; review the npm lock and all shipped dependency/component licenses;
  decide whether the observed core and third-party notices are sufficient for this
  experiment; review any model, dataset, adapter, provider, container image, Node
  runtime, and custom-dispatcher licenses separately.

The official package metadata visibly lists 56 direct runtime dependencies, one
optional dependency, and no declared `bundledDependencies`. The official third-party
notice covers incorporated or adapted Pi/pi-mono code under MIT but explicitly does not
replace normal package-manager dependency metadata. This packet therefore records the
core license without approving the dependency closure.

## Data classification and approved bundle

Only `public` and `synthetic` data classifications are eligible.

The proposed bundle contains:

- the accepted portable Council contract schemas and public synthetic proceeding;
- one repository-authored synthetic R4B decision packet;
- synthetic evidence with explicit provenance and no external-truth claim;
- a sanitized read-only source snapshot limited to explicitly approved repository
  files;
- synthetic credentials, or dedicated disposable credentials only if a separately
  approved cloud subtest cannot be avoided.

The repository maintainer is the data owner. Each bundle manifest must record source,
provenance, SHA-256 digest, data classification, sanitization reviewer, repository
approval, and pre-run inspection result. A second person must independently review any
work-derived material after sanitization and before it enters the bundle.

The bundle must exclude government, military, client, contract, corporate, proprietary,
work-derived, health, financial, personal, private-email, private-message, browser-
history, home-directory, production, and local-secret material. Unclear provenance
means exclusion. The post-run inspection must reconcile every staged file and retained
artifact against the approved manifest.

## Credential policy

The preferred experiment uses no credential beyond local runtime access. Cloud routing
is disabled.

An optional cloud-routing subtest is separately gated. If the human authorizes it, the
credential must be experiment-only, disposable, narrowly provider-scoped, minimally
funded, quota-limited, unrelated to production or personal accounts, injected only
after authorization, visible only to the approved route boundary, absent from Git and
Council artifacts, unsupported by any saved browser session, and rotated or deleted
immediately during teardown. Credential creation and injection require separate,
recorded human authorization.

Any credential exposure or residue is an immediate stop and experiment failure.

## Model and routing policy

No model has been selected, approved, downloaded, or invoked. OpenClaw support is not a
selection criterion. The human authorization review must fill exact model identifiers
after model/provider license, intended-use, capability, privacy, residency, context,
cost, and route controls are reviewed.

| Function | Route | Provider | Candidate identifier | Purpose | Allowed data | Max context / output | Max invocations | Approval and cost | Fail closed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Runtime orchestration model | none | none | `none_required` | Scheduling and routing must be deterministic. | Council identifiers only | 0 / 0 | 0 | No model cost | Any attempted orchestration-model call stops. |
| Council member | disabled pending review | unresolved | `unselected` | Two independent positions and one cross-review each | Approved public/synthetic bundle only | 24,000 / 4,000 tokens per call | 6 aggregate | Exact route requires human approval; cost attributed by packet and role | Missing or different route is denied and stops. |
| Security adversary | disabled pending review | unresolved | `unselected` | Attack the declared boundaries on paper and through approved negative tests | Approved public/synthetic bundle and sanitized runtime evidence | 24,000 / 4,000 | 2 | Same | Missing or different route is denied and stops. |
| Evidence auditor | disabled pending review | unresolved | `unselected` | Check provenance, support, omissions, and claims | Approved public/synthetic bundle and sanitized exports | 24,000 / 4,000 | 2 | Same | Missing or different route is denied and stops. |
| Deterministic verifier | local non-model | repository-owned implementation prerequisite | `python-3.12-deterministic-verifier` | Validate contracts, digests, events, budgets, and boundaries | Council artifacts and bounded evidence only | not applicable | 2 runs per runtime path | No model cost; implementation requires a later authorized packet | Any unavailable or nondeterministic check stops. |
| Custom dispatcher | identical approved member routes | same as corresponding role | same exact identifiers as OpenClaw path | Equivalent comparison | Identical bundle | Identical limits | Included in role totals | Identical attribution | Any route difference invalidates comparison. |

The aggregate invocation limit is 12, leaving two calls of contingency within the
role-specific plan. Local routes are preferred but are not presumed safe or licensed.
Cloud routes remain disabled unless the human authorization record names the provider,
model, endpoint class, data class, credential, quota, and cost ceiling. Unauthorized or
unrecorded cloud routing stops the entire experiment.

The `unselected` rows do not permit invocation. They make the missing human model
decision visible instead of silently choosing a model because the candidate runtime
supports it.

## Network policy

The gateway is loopback-only with no inbound LAN or public exposure. Outbound network
access is denied by an independent boundary. Candidate provenance retrieval, package
retrieval after authorization, and any separately authorized provider route must be
time-bounded and endpoint-allowlisted as distinct phases. No general DNS, browsing,
telemetry, marketplace, update, messaging, or discovery access is permitted.

Observed connection attempts and approved connections must be recorded independently of
runtime logs. A destination outside the approved endpoint manifest, any cloud route not
named in the authorization record, or inability to inspect the effective boundary is an
immediate stop.

## Tool policy

The proposed allowlist contains only bounded Council and verification operations.

| Operation | Allowed role | Arguments and data boundary | Side effect | External enforcement | Required evidence and denial test |
| --- | --- | --- | --- | --- | --- |
| `deliver_packet` | human-controlled dispatcher | Known packet ID, role ID, manifest digest | Copies approved immutable input into one role workspace | Read-only source and role-specific destination | Delivery event and digest; reject unknown role, packet, or digest |
| `read_synthetic_evidence` | four Council roles | Allowlisted evidence ID only | Read approved immutable evidence | Manifest allowlist and read-only mount | Evidence-delivery event; reject paths, unknown IDs, and cross-bundle reads |
| `export_frozen_position` | two member roles | Valid position, role ID, packet ID, digest | Writes to external export staging | Schema gate and append-only staging | Position/freeze events plus digest; reject overwrite and wrong role |
| `deliver_peer_bundle` | human-controlled dispatcher | Frozen position IDs and digests | Copies immutable peer bundle after both freezes | Phase gate and read-only bundle | Peer-delivery event; reject early, mutable, missing, or self-only bundle |
| `submit_cross_review` | two member roles | Valid review targeting the other frozen position | Writes one Council artifact | Contract validation and append-only staging | Cross-review event; reject self-review, unknown target, or second round |
| `export_runtime_events` | runtime adapter | Known correlation IDs and declared event schema only | Writes sanitized supporting telemetry | Schema/redaction gate and export-only destination | Export digest and completeness report; reject secrets, unknown IDs, or extra fields |
| `calculate_digest` | external verifier | Approved staged artifact ID | Writes bounded digest record | Verifier has read-only artifact access | Digest record; reject arbitrary paths and compare mutation attempt |
| `validate_council_artifacts` | external verifier | Approved artifact bundle ID | Writes deterministic result | Separate process and read-only inputs | Two matching verification results; reject invalid or runtime-native authority fields |
| `export_comparison_record` | human-controlled comparison step | Two verified path result IDs | Writes bounded comparison record | Fixed dimensions and immutable inputs | Comparison event; reject asymmetric inputs or feature-count scoring |

Every other operation is denied. Explicit denials include arbitrary shell, arbitrary
filesystem access, package installation, process management, host configuration,
credential inspection, browser automation, email, messaging, calendar, finance,
personal-data connectors, Git push, repository mutation, runtime self-modification,
skill installation, worker-defined tools, and network access outside approved
endpoints. Each denial must be tested at least once through the adapter and observed at
the independent enforcement boundary where applicable.

## Proposed hard budgets

| Budget | Proposed limit |
| --- | --- |
| Council roles | 4: two members, one security adversary, one evidence auditor |
| Primary sessions | 4 |
| Total sessions | 6, including at most two depth-one workers |
| Subagent depth | exactly 1 maximum; depth 2 is denied |
| Workers | at most 1 per role and 2 aggregate; member roles receive none by default |
| Deliberation rounds | 2: independent position and cross-review |
| Cross-review rounds | 1 |
| Messages per role per round | 2 |
| Model invocations | 12 per runtime path; 24 total only when both equivalent paths are separately authorized and completed |
| Input tokens | 160,000 aggregate per authorized path; 24,000 per invocation |
| Output tokens | 32,000 aggregate per authorized path; 4,000 per invocation |
| Wall-clock runtime | 120 minutes per path |
| Local compute duration | 90 minutes per path |
| Cloud spend | USD 0 by default; optional separately approved subtest hard ceiling USD 10 total |
| Retry count | 1 per non-security operation; 0 for permission, data, credential, route, integrity, or teardown failures |
| Tool calls | 64 aggregate per path |
| Forced termination | Stop the affected operation at every limit; stop the experiment on a security, integrity, authority, event, or teardown limit |

All values remain proposals until human approval. No budget may expand automatically.
Limit exhaustion must produce the declared event, deny continuation, and preserve
sanitized evidence for external review.

## Required evidence

The experiment must produce:

- the approved authorization record, environment and data manifests, candidate
  provenance record, and effective independent boundary records;
- role contracts, effective permission records, packet and evidence delivery records;
- frozen positions, peer bundle, cross-reviews, security-adversary and evidence-auditor
  reports;
- the bounded runtime-event export and independent corroboration;
- deterministic contract, digest, ordering, isolation, permission, route, budget,
  residue, and portability results;
- model route, token, retry, tool, wall-clock, local-compute, and cost attribution;
- an equivalent custom-dispatcher record and bounded comparison;
- dissent-preserving synthesis and an external human decision;
- teardown and residue evidence.

Runtime-native logs are supporting observations only. They cannot establish event
completeness, isolation, approval authenticity, evidence authenticity, security,
correctness, or Council authority. Event and verification requirements are specified in
`R4B_EXPERIMENT_RUNBOOK.md`.

## Stop authority and conditions

The human operator named in the later authorization record has unconditional stop
authority. Independent enforcement should terminate automatically where practical.

Stop immediately on an unauthorized network connection or cloud route; credential
exposure; permission or host-filesystem escape; cross-role workspace access;
cross-session memory exposure; missing required event; unbounded or recursive worker
creation; depth greater than one; message, token, time, tool, compute, retry, or cost
violation; mutation of Council artifacts; failure to freeze positions externally;
runtime identity represented as Council authority; runtime approval represented as
human approval; introduction of an unreviewed skill, tool, model, provider, endpoint, or
artifact; sensitive-data discovery; incomplete teardown; or candidate version, digest,
provenance, or license mismatch.

Stopping does not authorize remediation, retry, broader access, budget expansion, or
configuration changes.

## Teardown requirement

Every path must terminate the runtime and remove or invalidate the experiment
environment, state, sessions, workspaces, memory, caches, temporary files, credentials,
network exceptions, mounts, staging areas, sensitive operational logs, and generated
configuration. Only the specifically approved durable evidence may remain.

Incomplete teardown is an experiment failure and blocks R4C. The normative plan is
`R4B_TEARDOWN_AND_RESIDUE_PLAN.md`.

## Remaining unknowns for human review

- Whether the human accepts the dedicated-WSL2 design and every externally enforced
  control.
- Whether the core, incorporated-code, dependency, model, provider, adapter, runtime,
  and image license reviews are sufficient for the bounded experiment and intended use.
- Exact model and provider identifiers; no route is authorized while they are
  `unselected`.
- Whether the optional cloud subtest is necessary; the default is no.
- Whether approved endpoints, dedicated credentials, quotas, and cost controls can be
  independently enforced.
- Whether the required adapter, verifier, dispatcher, and event exporter can be
  implemented later without widening the accepted contract or tool boundary.
- Actual OpenClaw capability, isolation, event completeness, routing, cost, recovery,
  teardown, and value; these are R4B questions, not documentation facts.

## Authorization checklist

Every unchecked item blocks installation and execution.

- [ ] Entry-gate review accepted
- [ ] Threat model accepted
- [ ] Isolation design accepted
- [ ] Candidate version identified
- [ ] Candidate provenance reviewed
- [ ] License reviewed
- [ ] Intended use reviewed
- [ ] Data bundle approved
- [ ] Sanitization approved
- [ ] Credential plan approved
- [ ] Model plan approved
- [ ] Cloud-routing policy approved
- [ ] Tool allowlist approved
- [ ] Tool denylist approved
- [ ] Budgets approved
- [ ] Event requirements approved
- [ ] Deterministic checks approved
- [ ] Stop authority assigned
- [ ] Teardown plan approved
- [ ] Human installation approval recorded
- [ ] Human execution approval recorded

## Human decision

Decision: pending

Authorization status: not_authorized
