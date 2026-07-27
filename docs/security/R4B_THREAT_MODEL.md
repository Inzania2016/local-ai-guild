# R4B Experiment Threat Model

## Status and security claim boundary

Authorization status: `not_authorized`

This threat model describes required controls for a proposed experiment. It does not
claim that OpenClaw, the custom dispatcher, a model, an adapter, or the surrounding
environment implements or passes any control. OpenClaw, models, agents, tools, sessions,
memory, skills, and runtime logs are untrusted. Runtime-native logs are observations,
not proof of security.

No runtime, model, provider, credential, WSL2 distribution, virtual machine, container,
network rule, or host setting was created or changed while preparing this document.

## Protected assets

| Asset | Required protection |
| --- | --- |
| Windows host | No experiment process, mount, credential, listener, route, or residue outside the approved isolation boundary |
| WSL2 or VM boundary | Dedicated, inspectable, removable, and not a bridge to Windows home or unrelated host resources |
| Repository source | Sanitized read-only copy only; no repository or Git mutation |
| Council contracts and frozen artifacts | Council-owned, schema-valid, digest-stable, externally stored, and never overwritten by runtime state |
| Credentials | None by default; otherwise dedicated, narrowly scoped, quota-limited, hidden from roles, and destroyed after use |
| Model-provider access | Disabled by default; exact approved route only, with independently observed use and cost |
| Network access | Loopback-only ingress and deny-by-default egress outside separately allowlisted phases |
| Runtime event records | Bounded, correlated, redacted, complete against the declared inventory, and externally corroborated |
| Human approval records | External to the runtime, identity-bound, action-specific, immutable, and never inferred from repository publication |
| Teardown evidence | Complete, independently inspected, durable, and sufficient to establish residue status |
| Excluded personal and work-derived data | Never staged, mounted, prompted, logged, traced, exported, or retained |

## Trust boundaries

1. **Human operator:** sole authorization and unconditional stop authority; the runtime
   cannot impersonate, infer, or replace the human.
2. **Windows host:** trusted administrative boundary that must not be exposed to the
   experiment runtime.
3. **Dedicated WSL2 distribution:** experiment-only OS boundary selected for this
   packet and subject to approval before installation.
4. **Containers:** additional process/filesystem/resource boundary where practical, not
   a substitute for the dedicated WSL2 boundary.
5. **OpenClaw runtime:** untrusted candidate control plane.
6. **Council adapter:** narrow translation boundary; may not create Council authority.
7. **Local models:** untrusted content processors with separately reviewed artifacts,
   licenses, caches, and resource limits.
8. **Cloud providers:** external data, credential, network, residency, billing, and
   availability boundary; disabled unless separately approved.
9. **Filesystem:** read-only approved bundle, isolated role workspaces, append-only
   export staging, and prohibited host paths.
10. **Network gateway:** independent ingress, egress, DNS, endpoint, and connection
    enforcement.
11. **Evidence export:** redaction and schema boundary between untrusted runtime
    observations and Council-controlled review artifacts.
12. **External deterministic verifier:** separately controlled, read-only verifier that
    does not trust runtime identity or conclusions.

OpenClaw's official security policy describes a one-trusted-operator model rather than a
shared adversarial multi-tenant boundary and states that host execution can be available
when sandboxing is inactive. The R4B design therefore requires stronger external
isolation and never treats session IDs, runtime auth, tool policy, or runtime logs as the
sole boundary.

## Preferred isolation architecture

```text
Windows 11 host
└─ dedicated experiment-only WSL2 distribution
   └─ container-backed services where practical
      ├─ loopback-only candidate gateway
      ├─ role workspace A
      ├─ role workspace B
      ├─ security-adversary workspace
      ├─ evidence-auditor workspace
      └─ bounded export interface to external verification
```

Required properties:

- no Windows home-directory or broad host mount;
- one manifest-checked sanitized repository copy mounted read-only;
- separate writable workspace per role with no shared writable role directory;
- no global runtime memory and no role-to-role state path;
- loopback-only listener and no inbound LAN exposure;
- independently enforced outbound deny-by-default;
- explicit time-bounded allowlist only for separately approved release or provider
  endpoints;
- no unrestricted shell, browser, email, messaging, calendar, finance,
  personal-account, marketplace-skill, or host-configuration tool;
- dedicated test credentials only after action-specific human authorization;
- depth-one workers only, with an aggregate worker cap and independent depth-two denial;
- independent process, resource, cost, event, and termination observation;
- full teardown of the experiment environment unless a human separately authorizes
  retention for investigation.

A dedicated VM is not the selected design. Substituting one would require a revised
threat model, teardown plan, and authorization decision.

### Controls that must be external

The Windows/WSL2 boundary must enforce host isolation. OS permissions and read-only
mounts must enforce filesystem separation. The container engine or OS must enforce
process, memory, CPU, and workspace boundaries. A firewall or equivalent
network policy outside the runtime must enforce loopback ingress and outbound denial.
The provider account must enforce quota and spend. An external controller must enforce
depth, session, message, time, invocation, token, retry, tool, and termination limits.
Council-controlled storage must freeze artifacts. The independent verifier must check
contracts, digests, events, routes, denials, budgets, and residue.

No command or configuration recipe is part of this documentation packet.

## Threat scenarios and required controls

Control status uses:

- `repository_supported`: portable contracts or repository policy support the required
  representation, but do not enforce a runtime boundary.
- `externally_enforced`: the proposed experiment must enforce and inspect the control
  outside the candidate runtime.
- `unproven_until_r4b`: only the authorized experiment can show candidate behavior.

| Threat | Asset at risk / boundary crossed | Required preventive control | Required detection evidence | Immediate stop condition | Residual risk | Control status |
| --- | --- | --- | --- | --- | --- | --- |
| Runtime or agent broadens authority | Human approval and Council authority / runtime-to-human and adapter boundaries | Exact action allowlist; external approval record; adapter rejects runtime-native authority | Approval/denial events, adapter result, external approval comparison | Runtime claims approval, changes scope, or continues without exact approval | A model may phrase a persuasive false claim; humans must inspect bounded records | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Unrestricted shell or command execution | Windows host and isolated OS / tool and process boundaries | No shell tool; process allowlist outside runtime; no interpreter escape | Denied request plus process observation | Any undeclared process, command, interpreter, or shell succeeds | Unknown native or dependency behavior may still create processes | `externally_enforced`, `unproven_until_r4b` |
| Filesystem escape | Host, repository, credentials / container and OS filesystem boundaries | Read-only approved mount, role-specific roots, no arbitrary path tool, OS permissions | Denial event, mount inventory, file-access audit, post-run reconciliation | Read or write outside role roots or export interface | Kernel, mount, symlink, or implementation flaws remain possible | `externally_enforced`, `unproven_until_r4b` |
| Windows home-directory access | Personal/work data / WSL2-or-VM-to-Windows boundary | No Windows home mount or drive interop path; dedicated environment | Mount and path inventory; negative access test | Any home-directory content becomes visible | Host integration features could reintroduce a path if misconfigured | `externally_enforced`, `unproven_until_r4b` |
| Cross-role workspace access | Independent positions and role data / role filesystem boundary | Separate workspaces and identities; no shared writable workspace | Negative reads/writes from every role; file-access audit | Any role reads or changes another role's undisclosed workspace | Covert leakage through shared services or logs may remain | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Cross-session memory leakage | Independent analysis and excluded data / session and memory boundary | No global memory; isolated sessions; explicit immutable peer delivery only after freeze | Canary-based negative test, memory inventory, event ordering | Undisclosed peer content or canary appears in another session | Model/provider caching and opaque runtime state may limit proof | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Credential disclosure | Dedicated credentials and provider access / credential-to-role and export boundaries | No credentials by default; separate secret injection; role denial; redaction | Secret canary scan, provider audit, export/log scan, credential-store inspection | Credential or token appears in role input, output, tool args, event, file, or log | Opaque dependency memory or provider logging may retain material | `externally_enforced`, `unproven_until_r4b` |
| Unauthorized network access | Host/network and data / runtime-to-network boundary | Outbound deny-by-default outside runtime; endpoint/time allowlist | Independent connection, DNS, and destination record | Any unapproved destination or protocol attempt succeeds | Encrypted approved endpoints can conceal application behavior | `externally_enforced`, `unproven_until_r4b` |
| Unauthorized cloud routing | Data, credentials, spend / local-to-cloud-provider boundary | Cloud disabled by default; exact route manifest; provider quota and external route gate | Per-invocation route record plus provider-side usage reconciliation | Any unapproved provider, model, endpoint, or route is attempted | Runtime may omit route metadata; external provider evidence is required | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Hidden or incomplete runtime events | Auditability and human decision / runtime-to-evidence boundary | Predeclared event inventory; external phase observer; fail on absence | Completeness and ordering report reconciled with independent observations | Any required event is absent, unknown, secret-bearing, or unorderable | Some internal actions may remain unobservable | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Runtime logs treated as security proof | Human decision / runtime-to-verifier boundary | Logs labeled supporting observations; external controls and verifier authoritative | Evidence-source classification in every finding | A pass depends only on runtime self-report | Independent observers can also be incomplete or misconfigured | `repository_supported`, `externally_enforced` |
| Runtime identity treated as Council authority | Council contracts and decisions / adapter boundary | Council IDs and external human approval only; runtime fields forbidden in authority records | Contract validation and runtime-field scan | Runtime agent/session ID is used as role, approval, decision, or evidence authority | Human reviewers may misread correlated telemetry | `repository_supported`, `unproven_until_r4b` |
| Position modified after freezing | Frozen artifacts and dissent / export boundary | Canonical serialization, external SHA-256 freeze, append-only storage | Pre/post digest comparison and immutable storage record | Frozen bytes, digest, identity, or meaning changes | Canonicalization defects or storage compromise remain possible | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Unbounded worker spawning | Compute, spend, event completeness / session-to-worker boundary | One worker per role, two aggregate, external spawn controller | Worker request/create/deny events and session inventory | Worker or session count exceeds declared budget | Runtime-internal work may not map cleanly to visible workers | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Recursive subagent creation | Authority and compute / parent-to-child boundary | Depth exactly one; child has no spawn permission; external depth record | Depth-one success and depth-two denial with process/session inspection | Any depth-two or uncorrelated child exists | Hidden delegation inside a provider may be opaque | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Unbounded message loops | Tokens, time, spend / session and dispatcher boundary | Fixed rounds/messages; external counter and deadline | Message counters, event sequence, forced-termination record | Round or message limit reached or loop pattern detected | One allowed message may still be computationally expensive | `externally_enforced`, `unproven_until_r4b` |
| Token, compute, time, tool, or cost runaway | Host resources and provider account / model, host, and billing boundaries | Per-call and aggregate limits; provider quota; OS resource cap; hard deadline | Independent usage, process, wall-clock, tool, and billing reconciliation | Any threshold is reached, exceeded, or cannot be measured | Provider accounting delay and tokenizer differences may create uncertainty | `externally_enforced`, `unproven_until_r4b` |
| Tool-call argument injection | Filesystem, network, artifacts / model-to-tool boundary | Strict schema, registry-owned IDs, no paths or free commands, exact role/phase gate | Accepted/denied request records and adversarial malformed cases | Unknown field, path, identifier, target, operation, or encoded escape succeeds | Parser or validation defects remain possible | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Marketplace or third-party skill introduction | Host, network, data, supply chain / plugin boundary | Skill installation and discovery denied; fixed reviewed runtime surface | Installed-component inventory and denied skill request | New, updated, dynamically fetched, or undeclared skill/plugin appears | Candidate package includes a broad surface even when disabled | `externally_enforced`, `unproven_until_r4b` |
| Persistence after teardown | Host and future runs / runtime-to-host lifecycle boundary | Ephemeral environment; no service/autostart; complete destruction or approved quarantine | Process, service, task, container, VM/WSL2, file, and listener inspection | Any unapproved process, service, listener, task, state, or environment remains | Firmware, host logs, provider logs, and opaque caches may be outside deletion scope | `externally_enforced`, `unproven_until_r4b` |
| Credentials or runtime state not removed | Provider access and data / teardown boundary | Credential revocation, state manifest, environment destruction, external verification | Provider-side revocation plus filesystem, environment, store, and cache scan | Any active credential or unapproved runtime state remains | Provider retention may persist non-secret usage records | `externally_enforced`, `unproven_until_r4b` |
| Supply-chain or provenance uncertainty | Host and experiment validity / release-to-environment boundary | Immutable version/commit, official source only, integrity/signature checks, component inventory | Recomputed digests, signature record, package and lock inventory | Version, commit, package, digest, signature, license, or source mismatch | Validly signed upstream code may still be vulnerable or malicious | `externally_enforced`, `unproven_until_r4b` |
| Sensitive or work-derived data enters experiment | Public-repository boundary and excluded data / staging boundary | Approved manifest, public/synthetic default, independent sanitization review | Pre-run content/provenance scan and post-run reconciliation | Sensitive, unclear-provenance, personal, work, government, client, or production data found | Automated scans cannot prove provenance or complete sanitization | `repository_supported`, `externally_enforced` |
| Approval forgery or ambiguity | Human authority / runtime and repository-to-human boundary | External action-specific approval with named operator; pending means deny | Approval identity, scope, timestamp, candidate, model, route, and budget comparison | Missing, mismatched, runtime-created, or publication-inferred approval | Human-account compromise or mistaken authorization remains possible | `repository_supported`, `externally_enforced` |
| Evidence export leaks secrets or operational details | Credentials, host details, excluded data / export boundary | Strict bounded schema, redaction, secret/private-address scan, human review | Export validation, scan results, independent reviewer sign-off | Export contains a secret, host path, private address, internal detail, or unapproved prose | Novel secret formats and inference from metadata remain possible | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Custom dispatcher receives weaker controls | Comparison validity / alternative-path boundary | Identical packet, routes, tools, budgets, events, checks, and teardown | Side-by-side manifest equality and deviation report | Any material control or input differs without preapproval | Implementations have inherently different attack surfaces | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |
| Teardown cannot preserve required evidence | Human decision and portability / runtime-to-durable-storage boundary | Export and validate approved evidence before destruction; runtime-free formats | Artifact readability and digest check after runtime removal | Teardown would destroy required evidence or evidence requires runtime state | External storage or verifier defects may still affect durability | `repository_supported`, `externally_enforced`, `unproven_until_r4b` |

## Detection and evidence hierarchy

Evidence is evaluated in this order:

1. Council-owned contracts, frozen bytes, and external human approval records.
2. Independently enforced host, filesystem, network, credential, quota, and lifecycle
   observations.
3. External deterministic verification results.
4. Sanitized runtime-native exports and logs as supporting observations only.
5. Model statements only as untrusted proposals.

Conflicts are not reconciled in favor of the runtime. Missing independent evidence
fails the affected control.

## Residual-risk decision

Even with every proposed control, residual risk includes supply-chain compromise,
isolation defects, kernel or container escape, opaque model/provider processing,
incomplete observability, human error, flawed deterministic checks, data
re-identification, and incomplete third-party deletion. No experiment result can prove
general OpenClaw security or suitability outside the exact candidate, environment,
inputs, routes, and limits tested.

The human authorization review must explicitly accept or reject this residual risk.
Silence, repository publication, a passing repository test suite, or runtime-native
status does not accept it.

## Stop and resume boundary

The named human operator may stop for any reason. Every listed stop condition terminates
the experiment. Available sanitized evidence is preserved if safe, credentials are
revoked, and teardown begins. Resume or remediation requires a new explicit
authorization that names the changed boundary; stopping never grants broader access.
