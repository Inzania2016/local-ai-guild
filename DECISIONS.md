# Decisions

## R0 decisions — 2026-07-21

- Use Python 3.12 with a conventional `src` package layout; R0 verification used Python 3.12.6.
- Keep runtime dependencies empty in R0; use Ruff and pytest as development dependencies.
- Expose only a harmless `status` CLI command in R0.
- Treat deterministic scripts as sources of facts and model output as proposals requiring validation.
- Prohibit unrestricted shell tools, automatic cloud delegation, and automatic commits or pushes.
- Keep tracked configuration limited to `.example.yaml` files; ignore real local configuration.
- Keep generated evidence, traces, benchmark results, model files, runtime state, caches, and virtual environments out of Git.
- Keep the repository at `C:\dev\source\Repos\local-ai-guild`; plan `E:\AI` for active assets and `D:\AI` for archival assets.
- Defer every model and runtime choice until project-specific local evaluation exists.
- Make R1 only typed tool contracts plus a deterministic mock router, with no model connection.
- Treat the repository and its published artifacts as public; prohibit non-public or sensitive work material from commits, logs, traces, and publications.
- Use public or synthetic fixtures by default. Require sanitization, explicit repository approval, and independent review before committing any work-derived material.
- Require model, dataset, and adapter license review before adoption, with heightened attention to commercial, corporate, government, and contract-related use. Do not select a project license or approve a candidate license in R0.

Future durable architecture decisions should receive focused records under `docs/decisions/` and be summarized here.

## R1 decisions — 2026-07-21

- Use Pydantic v2 `BaseModel` contracts for validation and serialization at untrusted proposal and routing boundaries.
- Configure boundary models for strict validation, forbidden unknown fields, and frozen instances. Use discriminated unions so each tool identifier accepts only its own argument contract.
- Confine Pydantic to external validation and serialization boundaries. Deterministic routing remains ordinary typed Python, avoiding a custom general-purpose validation framework and keeping domain logic independent from validation machinery.
- Generate JSON Schema in memory from Pydantic contracts when requested; do not add a schema registry or persist generated schemas in R1.
- Define `project_status`, `search_public_docs`, and `read_public_doc` as harmless R1-only mock contracts, not production tools.
- Require every success and refusal to carry at least one stable rule evidence reference.
- Keep proposals untrusted and non-executable. R1 has no dispatcher, executor, filesystem read, network access, subprocess, or tool invocation path.
- Convert validation failures to bounded generic messages and schema-owned locations only. Do not serialize Pydantic messages or attacker-chosen location components because they may contain rejected input.

## R2 decisions — 2026-07-24

- Represent routing and policy evidence as strict typed references with a bounded identifier, evidence kind, and public-repository-safe provenance metadata.
- Treat evidence identifiers as deterministic references rather than proof of external truth; provenance metadata does not establish cryptographic authenticity.
- Resolve R1 evidence strings and select policy evidence only through immutable registries of synthetic constants. Unknown or duplicate routing evidence fails closed without echoing the identifier.
- Reserve the `rule:` namespace for `routing_rule` evidence and `policy:` for `policy_rule` evidence. Reject other namespaces, drive-like values, and URL-like forms rather than broadening the grammar.
- Build routing envelopes only from exact, already validated R1 decision instances. Reject subclasses deliberately so trusted-boundary code cannot acquire unreviewed behavior. Policy likewise accepts only an exact validated routing envelope and profile and never implicitly parses raw dictionaries or standalone proposals.
- Bind each combined policy-evaluation envelope to the immutable profile actually evaluated. Direct construction rechecks the routing, profile, and policy combination; no profile identifier or persistence is introduced.
- Apply policy in explicit deny-by-default precedence: routing refusal, missing allowlist membership, human approval requirement, then allow.
- Treat `allow` and `require_human_approval` as non-executing outcomes. R2 has no executor or approval workflow and stores no raw request or persistent audit record.

## R3 decisions — 2026-07-25

- Implement R3 as a small in-memory deterministic harness over the existing R1 router and R2 combined evidence/policy helper; do not redesign those boundaries.
- Store ten versioned public or synthetic cases as immutable Python records. Add no file loader, caller-supplied path, parsing dependency, generalized benchmark framework, or evaluator extension system.
- Treat expected results as repository-owned test assertions rather than external facts, runtime evidence, or model-quality scores.
- Compare routing outcome, applicable refusal reason or routed tool, routing evidence, policy outcome, policy issues, and policy evidence in fixed order. Suppress refusal-reason and routed-tool mismatches when the routing outcome itself differs.
- Restrict failures to registry-owned mismatch codes with messages derived from those codes. Case results and summaries are evaluator-built, recheck private non-serialized case bindings at trusted boundaries, and exclude raw input, proposal arguments, exception text, timing, execution state, and machine metadata.
- Reject empty batches, mutable collections, raw dictionaries, arbitrary objects, duplicate case identifiers, and subclasses at the trusted evaluator boundary.
- Keep R3 non-executing and non-persistent. It connects no model, tool, retrieval service, approval workflow, network, cloud service, or ontology infrastructure.
- Defer ontology work to a proposed analysis-only O1 packet after R3.

## O2 decisions — 2026-07-25

- Implement only one evidence-trace pilot for the completed R2 work packet, represented by the fixed repository-owned `docs/traces/r2-closeout.toml`.
- Treat TOML as the pilot representation and strict Pydantic contracts as its schema implementation; neither replaces cited authority sources or constitutes a generalized ontology.
- Parse with Python 3.12 standard-library `tomllib` through a loader with no caller-supplied path, discovery, dynamic citation resolution, Git inspection, or external verification.
- Use exactly ten top-level record types. Keep requirements and evidence as strict embedded values and relationships as explicit typed fields.
- Separate realization, automated verification, human verification, approval, approval-evidence, provenance, and epistemic status.
- Represent R2 publication as commit `903aa815a6e0176e682b4726ee8114627bd98940` while marking approval `unknown_from_repository` and approval evidence `not_recorded_in_repository`.
- Treat the missing approval-evidence finding only as absence of a first-class repository record; do not infer that approval failed or did not occur.
- Keep findings registry-owned, bounded, evaluator-built, and deterministically ordered. Commit identity proves neither authorization nor correctness, and repository assertions are not external truth.
- Keep O2 non-executing and in-memory after the single fixed TOML read. Add no routing, retrieval, graph database, ontology infrastructure, persistence, model, runtime, executor, or approval workflow.
- Do not make trace completeness a repository progression gate in O2.
- Derive findings from typed record, evidence, relationship, and status semantics rather than official fixture identifiers. Require globally unique trace, top-level record, and embedded requirement identifiers, and reject duplicate targets within every relationship field.
- Bind evidence kinds to compatible provenance and epistemic status combinations. A claimed approval requires human-record evidence and a confirmed explicit-human authority; Git commit evidence and security or verification policy authority cannot establish approval.
- Keep `docs/traces/r2-closeout.toml` outside wheel package data. The fixed loader is supported from a repository checkout or editable install only in O2; installed-wheel fixture support is deferred rather than expanding packaging scope.

## R4A decisions — 2026-07-26

- Keep the AI Council portable and institutionally authoritative over ontology, roles, work packets, deliberation, evidence, verification, approval, decisions, knowledge promotion, and audit standards.
- Keep agent creation, sessions, model configuration, tool wiring, bounded worker spawning, scheduling, runtime permissions, runtime events, and runtime-specific messaging behind a replaceable adapter boundary.
- Treat every runtime as untrusted. Runtime identifiers, objects, memory, configuration, and self-reported events cannot become authoritative Council state or serve as their own security proof.
- Record OpenClaw only as a candidate reference runtime for a future R4B proof of concept. R4A does not select, approve, adopt, install, configure, download, or execute OpenClaw.
- Require minimum portable Council contracts before R4B, then use R4B evidence to inform a human R4C runtime decision and runtime-selection ADR.
- Keep runtime memory non-authoritative. Promotion requires evidence, epistemic classification, review, applicable human approval, durable rationale, and freshness or expiration metadata.
- Recommend an isolated WSL2 distribution or VM, loopback-only access, role-specific workspaces, a sanitized read-only repository, dedicated test credentials, depth-one workers, explicit budgets, no broad host or personal-account access, and complete teardown for a future POC.

## O3 decisions — 2026-07-26

- Use one clearly labeled public synthetic documentation-metadata packet and one fixed
  contract-valid but semantically incomplete TOML trace. The fictional packet,
  artifact, verification, approval, commit, and publication are assertions only and do
  not claim the work occurred.
- Add `load_o3_trace()` as a zero-argument fixed loader over the existing bounded TOML
  parsing internals. Add no caller-supplied path or generalized trace-loader API, and
  leave `load_r2_trace()` behavior intact.
- Compare findings only by finding code, subject identifier, and relationship. Exclude
  free-form messages, raw TOML, packet prose, paths, parser errors, and run metadata
  from the result.
- Keep the manual review as an immutable repository-authored assertion rather than
  Markdown-derived data or external truth.
- Plant five semantic handoff defects. Accept four validator matches and one
  manual-only reciprocal-publication gap rather than adding an O3-specific or
  insufficiently justified general validator rule.
- Preserve the validator's three informational scope findings as validator-only
  results. They are epistemic caveats, not additional planted structural defects.
- Keep O3 to fixed loading, deterministic in-memory validation, and immutable result
  comparison. Add no mutation, persistence, model, runtime, OpenClaw, routing,
  retrieval, executor, approval workflow, or external inspection.

## Portable Council contract decisions — 2026-07-26

- Implement the minimum institutional set as ten strict, frozen, extra-forbid Pydantic
  contracts plus one exact in-memory `CouncilProceeding`; do not build a generalized
  ontology, graph, loader, persistence layer, or workflow engine.
- Keep every authoritative identifier in the Council-owned durable identifier grammar.
  Exclude runtime agent IDs, session IDs, model names, workspace paths, runtime-native
  objects, and provider configuration from Council authority fields.
- Represent a frozen position with a Council-owned SHA-256 content digest and explicit
  integrity status so reviews target a stable version.
- Keep evidence provenance and epistemic classification separate. Verification has no
  approval field; a validator issue rejects any decision that treats verification as
  its approval request.
- Make approval and promotion request-only contracts. Human decisions are separate
  durable records, and knowledge-promotion requests cannot directly mutate knowledge.
- Preserve material dissent as strict nested values in the decision record.
- Treat runtime events as bounded operational telemetry with a Council correlation ID.
  Runtime events cannot become role, decision, or approval authority.
- Store every relationship in one canonical direction and derive reverse navigation.
  This resolves O3's manual-only reciprocal-publication question by not treating
  reciprocal duplicate edges as an institutional requirement.
- Validate only essential cross-contract integrity through bounded registry-owned issue
  codes in deterministic order. Keep the validator exact-type, in-memory,
  non-executing, and non-persistent.
- Keep OpenClaw a candidate reference runtime. The checkpoint does not implement a
  runtime adapter or authorize R4B.

## R4B entry-gate review decisions — 2026-07-27

- Treat the accepted portable contracts and synthetic proceeding as strong
  representation evidence, not candidate-runtime capability evidence.
- Classify Gates 1 and 5 as `partially_supported`: the minimum flow and
  runtime-independent artifacts are represented, but an adapter must still demonstrate
  hosting, export, hash preservation, and post-teardown portability.
- Classify Gate 2 as `blocked_by_missing_prerequisite` until an experiment-specific threat
  model, isolation design, independent controls, and teardown procedure are documented
  and approved.
- Classify Gates 3, 4, and 6 as `requires_r4b_experiment`; synthetic contracts cannot prove
  runtime-event completeness, route/cost attribution, unauthorized-cloud denial, or net
  operational value.
- Conclude `ready_to_propose_bounded_r4b_packet` only for a separate
  authorization-and-experiment-design packet. The conclusion does not authorize R4B,
  installation, execution, runtime selection, or adoption.
- Require that later packet to define the exact version, license and intended-use review,
  public or synthetic data, credentials, models, routing, tools, budgets, events,
  deterministic checks, human stop authority, and explicit installation/execution gate.
- Preserve OpenClaw as a candidate reference runtime and defer any selection ADR to R4C.

## R4B authorization-package decisions — 2026-07-27

- Keep authorization status `not_authorized`, the human decision `pending`, and every
  authorization checklist item unchecked. Repository publication cannot authorize
  installation or execution.
- Propose only official stable OpenClaw `v2026.7.1` at immutable commit
  `2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4`; reject floating or prerelease
  identifiers for the experiment.
- Record the official MIT core license, incorporated-code notice, package dependency
  surface, and release integrity metadata as review evidence, not legal, dependency,
  intended-use, security, or adoption approval.
- Select a dedicated experiment-only WSL2 distribution with container-backed services
  where practical and a loopback-only gateway. Require no Windows home mount, separate
  role workspaces, independently denied outbound access, external verification, and
  complete environment teardown. Substituting a VM requires a revised review.
- Treat OpenClaw, models, agents, sessions, tools, skills, memory, and logs as untrusted.
  Enforce host, filesystem, network, credential, quota, budget, freeze, approval, stop,
  and teardown controls outside the runtime where practical.
- Use public or synthetic data only. Prefer no credentials and no cloud route. Any cloud
  subtest requires exact models, providers, endpoints, dedicated disposable credentials,
  quotas, cost ceilings, and separate action-specific human approval.
- Leave model identifiers `unselected` until the human review considers license,
  intended use, privacy, capability, cost, and route controls. Runtime compatibility
  alone is not a model-selection criterion.
- Limit the proposed experiment to four Council roles, four primary sessions, at most
  two depth-one workers, one cross-review round, fixed message/model/token/time/compute/
  retry/tool/cost budgets, and a minimal schema-validated non-shell tool allowlist.
- Require the same packet, roles, evidence, model routes, policies, budgets, events,
  checks, stops, and teardown for OpenClaw and the smaller dispatcher. Feature count is
  not a success metric.
- Require predeclared bounded runtime events plus independent corroboration and external
  deterministic checks. Runtime-native logs remain supporting observations only.
- Define incomplete teardown as experiment failure. Preserve only approved sanitized
  Council artifacts, verification, comparison, cost/routing, review, teardown, and
  human-decision evidence in runtime-independent formats.
- Make a human R4B authorization review the next packet. It may approve, reject, or
  defer the specifically bounded later installation and execution actions, but it must
  not perform them and cannot select OpenClaw for adoption.

## Human R4B authorization-review preparation decisions — 2026-07-27

- Make `docs/PUBLICATION_INDEX.md` the authoritative detailed publication ledger.
  Keep concise current-state summaries in root authority documents and preserve
  historical verification evidence.
- Correct the bounded authorization package dependency statement to 56 direct runtime
  dependencies, one optional dependency, and no declared `bundledDependencies`.
  Treat static package metadata as technical evidence rather than legal approval.
- Record `recommend_defer` as Codex's advisory recommendation while preserving the
  official human decision as `pending`, authorization as `not_authorized`, and every
  authoritative checklist item as unchecked.
- Defer environment creation and OpenClaw installation until one exact installed local
  model route is reconciled with an immutable artifact identity and its dedicated-WSL2
  use is reviewed. Do not substitute a cloud route.
- Keep execution separately blocked until installed-state controls, an externally
  enforced egress mechanism, the adapter, event exporter, deterministic verifier,
  stop enforcement, and teardown evidence exist under later authorized packets.
- Use only the proposed repository-owned public or synthetic bundle. Freeze its commit,
  derived packet, SHA-256 values, sanitization review, and human approval only in a
  later pre-run step.
- Accept the existing sessions, rounds, messages, retry, zero-cloud-budget, human-stop,
  and equal-comparison limits as proposed. Keep named conditions on tools, worker depth,
  invocation/token/time/compute/tool-call limits, events, deterministic checks, and
  teardown. Defer egress and event export until independently enforceable and evidenced.
- Name read-only local-model route qualification as the smallest next prerequisite. It
  must stop without loading or invoking a model, downloading an artifact, creating an
  environment, installing a runtime, or executing R4B.

## R4B local-model route-qualification decisions — 2026-07-28

- Reconcile the published human-review packet at
  `9d1f1935560c010f36a27be85483924a2c52bffd` as the current published baseline.
  Preserve `c779ea815490ec14b9f6357729b46087235c03ba` as the final publication-reference
  correction before that advisory review.
- Use filesystem manifests, direct SHA-256 calculation, local settings, and official
  web metadata only. Do not call Ollama, LM Studio, llama.cpp, OpenClaw, or another
  model runtime.
- Classify the complete Ollama Qwen2.5-Coder 7B Q4_K_M artifact and LM Studio Q5_K_M
  file as exact immutable local artifacts. Exclude the incomplete Ollama 14B and Qwen3
  30B manifests.
- Conditionally qualify only route
  `r4b-local-qwen25-coder-7b-q4km-v1`, pinned to the exact official-registry-matching
  Ollama manifest, model, config, and Apache-2.0 license digests.
- Prefer the Ollama artifact over the LM Studio conversion because it has the shorter
  official distribution chain. Keep the LM artifact as an exact alternate, not a
  heterogeneous route.
- Reduce the proposed per-invocation context/output ceilings from 24,000/4,000 to
  8,192/2,048 as an explicit amendment requiring human acceptance. Preserve the
  10-planned and 12-hard invocation ceilings per runtime path.
- Treat separate sessions, frozen positions, and isolated delivery as procedural
  independence only. One Qwen model for all roles provides no model diversity and
  creates correlated-failure risk.
- Qualify immutable identity, provenance evidence, license evidence, and plausible
  static hardware fit only. Defer performance, AMD acceleration, runtime viability,
  instruction following, evidence use, adversarial competence, and audit competence to
  a later authorized benchmark.
- Keep the broader Codex recommendation `recommend_defer`, authorization
  `not_authorized`, human decision `pending`, and every human checklist item unchecked.
- Make R4B local-model capability benchmark the next packet. It must define cases and
  thresholds before inference and obtain separate human authorization before runtime
  start or model invocation.
