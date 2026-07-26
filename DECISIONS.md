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
