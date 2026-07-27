# Project State

Last updated: 2026-07-27

## Confirmed current facts

- R0 established the repository control plane and minimal Python skeleton at commit `14f90483279b2739ea41739bdabae882666f48de`.
- R1 implements strict, frozen Pydantic v2 contracts for untrusted user requests, three tool-specific proposals, successful and refused decisions, stable evidence references, and structured validation issues.
- R1 implements a case-sensitive deterministic mock router for `status`, `search docs: <query>`, and `read doc: <repository-relative-markdown-path>`.
- The three R1 tool identifiers are harmless test contracts, not production tools. The router stops at a validated proposal or typed refusal.
- The repository path is `C:\dev\source\Repos\local-ai-guild`.
- Python is pinned to 3.12 for project work.
- The CLI remains a harmless project `status` command and reports the portable Council contracts checkpoint stage.
- Example configuration files contain no live provider or model connection details.
- Pydantic 2.13.4 is the sole runtime dependency and is confined to validation, serialization, and JSON Schema generation at untrusted boundaries.
- R1 validation issues retain stable error codes, bounded generic messages, and sanitized schema-owned locations; rejected values and attacker-chosen field names are not serialized.
- R2 implements strict typed routing and policy evidence references, immutable synthetic registries, namespace/kind separation, and a routing-decision envelope built only from exact validated R1 decision instances. Raw dictionaries, subclasses, unknown or cross-registry evidence, caller-created lookalike evidence, and semantically inconsistent rule evidence are rejected.
- R2 implements immutable allowlist profiles and explicit deny-by-default policy precedence. The default allows `project_status` and `search_public_docs`, requires human approval for `read_public_doc`, and refuses R1 refusals or unallowlisted tools. Combined envelopes include the exact immutable profile evaluated and validate the routing/profile/result relationship.
- Policy outcomes are non-executing metadata. R2 has no approval workflow, executor, raw-request storage, trace persistence, audit database, timestamping, or machine-identity fields.
- Evidence identifiers are deterministic references rather than proof of external truth; `public` and `synthetic` provenance values are metadata, not cryptographic authenticity.
- R3 implements five strict, frozen evaluation boundary models, exact-type single-case and batch runners, registry-owned bounded mismatch metadata, evaluator-built case results, and a deterministic evaluator-built in-memory summary. Trusted result and summary checks retain only private non-serialized identifier and expected-result bindings, never case input.
- The versioned R3 case set contains ten public or synthetic cases covering successful routing, routing refusals, default policy behavior, an empty allowlist, approval-free document reads, and allowlist exclusion.
- R3 comparisons use stable R1/R2 outcomes, reasons, tools, issue codes, and registered evidence identifiers. Results and summaries do not contain raw commands, queries, document paths, proposal arguments, exception text, timing, or execution state.
- R3 passing evaluations establish only conformance between the deterministic implementation and repository-owned synthetic expectations. No model was evaluated and no external correctness claim is supported.
- O2 implements one fixed repository-owned TOML evidence-trace fixture for the completed R2 packet, parsed with Python 3.12 standard-library `tomllib` through a loader that accepts no caller path.
- O2 uses strict, frozen, extra-forbid Pydantic contracts for exactly ten top-level record types. Requirements and evidence remain typed embedded values; explicit relationship fields are validated deterministically in memory.
- O2 enforces global uniqueness across the trace, top-level record, and embedded requirement identifiers; duplicate relationship targets, incompatible evidence semantics, non-human approval authority, approval forgery, and publication/status contradictions fail closed.
- The fixed fixture is repository content, not wheel package data. O2 supports loading from a repository checkout or editable install and does not claim standalone installed-wheel support.
- The O2 trace is subordinate to cited authority sources. It performs no dynamic citation, Git, filesystem-artifact, external-truth, human-identity, or approval-authenticity verification.
- The official R2 trace is contract-valid and produces one known completeness error: `missing_approval_evidence`. The repository lacks a first-class record of the R2 publication authorization event; this does not establish that approval failed or did not occur.
- O2 findings also state that commit identity does not establish authorization or correctness and repository assertions are not external truth.
- O2 is published at commit `a79d8103ea7d2a13ac808ccf046efdf55b767d2b`.
- O3 adds one fixed public synthetic handoff packet and contract-valid but semantically
  incomplete trace. The fixture's packet, artifact, verification, approval, commit, and
  publication are fictional repository assertions and do not claim the work occurred.
- The O3 loader accepts no path and shares only bounded fixed-loader internals with O2.
  It does not alter `load_r2_trace()` or add a generic trace-loader API.
- The immutable manual assertion contains five findings. The unchanged deterministic
  validator returns seven findings: four structural matches and three validator-only
  epistemic scope caveats. Manual review alone identifies the non-reciprocal
  publication edge.
- O3 comparison results are evaluator-built, strictly typed, immutable, deterministically
  ordered, and limited to finding code, subject identifier, and relationship. They
  retain no raw TOML, packet prose, paths, parser errors, or free-form messages.
- O3 establishes only synthetic structural comparison behavior. It does not prove
  external truth, approval authenticity, artifact existence, human identity, or
  general ontology correctness.
- O3 is published at `a307d1274a88a64ed6dd9a334f4f757f6d67ed80`.
- R4A documents a portable AI Council/runtime ownership boundary, objective runtime requirements, a knowledge-promotion policy, and an OpenClaw reference-runtime proof-of-concept design. These are architecture artifacts only.
- The portable contract checkpoint implements strict, frozen, extra-forbid
  `RoleContract`, `CouncilWorkPacket`, `FrozenPosition`, `CrossReview`,
  `CouncilEvidence`, `VerificationRecord`, `ApprovalRequest`, `DecisionRecord`,
  `KnowledgePromotionRequest`, and `RuntimeEvent` contracts.
- One immutable public synthetic in-memory proceeding contains four roles, two
  independently frozen positions, one cross-review, deterministic verification, a
  human approval request, one dissent-preserving decision, a knowledge-promotion
  proposal, and three portable runtime events.
- The deterministic proceeding validator checks essential identifier, reference,
  frozen-review, approval, promotion, runtime-correlation, and runtime-authority
  boundaries with registry-owned issues in fixed order. It performs no I/O, mutation,
  persistence, execution, or external resolution.
- Council relationships store one canonical direction. Reverse navigation is derived
  and non-authoritative; reciprocal duplicate edges are not required.
- These are minimum portable contracts, not a completed Council, deliberation engine,
  approval workflow, promotion engine, persistence layer, or runtime adapter.
- OpenClaw is a candidate reference runtime. It has not been selected, approved, adopted, installed, configured, downloaded, or executed.
- The documentation-only R4B entry-gate review classifies minimum-flow representation and
  artifact portability as partially supported, isolation as blocked by missing approved
  prerequisites, and execution records, routing/cost visibility, and net value as requiring
  a bounded runtime experiment.
- The review concludes that a separate bounded R4B authorization-and-experiment-design
  packet is ready to be proposed. It does not authorize R4B, installation, execution, or
  adoption.
- No AI SDK, web framework, vector database, runtime-specific dependency, MCP implementation, HTTP API, dispatcher, executor, filesystem reader, retrieval implementation, cloud integration, training pipeline, audit persistence, or Docker configuration is present.
- The repository-local environment uses Python 3.12.6 with Ruff 0.15.22 and pytest 8.4.2.
- R3 repository verification, Ruff, formatting, pytest, CLI status, deterministic case evaluation, redaction checks, and prohibited-surface scans pass as recorded in `VERIFICATION.md`. O2 verification and security-review results are recorded separately in that document.
- The authority documents establish an explicit public-repository data boundary: public or synthetic fixtures are the default, and work-derived material requires sanitization, explicit repository approval, and independent pre-commit review.
- Model, dataset, and adapter licenses require review before adoption; R0 through R3 and O2 select no project license and approve no candidate license.

## Planned, not implemented

- `E:\AI` will hold active models, runtimes, caches, and active workspace assets.
- `D:\AI` will hold archives, datasets, experiments, benchmark history, and backups.
- Candidate components and model hypotheses are described in `VISION.md` and architecture documents.
- R4B may evaluate a runtime only under a separate explicitly authorized packet.
- Before any R4B installation or execution, a separate packet must finalize and obtain
  review of the experiment threat model, isolation design, independent controls, teardown,
  candidate version, license and intended-use posture, data, credentials, models, routing,
  tools, budgets, event export, deterministic checks, and human stop authority.

## Not validated

- No local or cloud model candidate has been evaluated.
- LM Studio, Ollama, OpenCode, llama.cpp, OpenClaw, and cloud agents have not been configured or invoked.
- The planned storage layout has not been provisioned or validated by R0.
- No project, model, dataset, or adapter license has been selected or approved.
- No eligible OpenClaw version, license conclusion, current runtime capability, routing
  behavior, event completeness, isolation result, teardown result, or operational-value
  result has been established.

## Current stage gate

R3 remains published at commit `3f20d28390086619b8268e35855d4789b4a75304`,
O2 is published at commit `a79d8103ea7d2a13ac808ccf046efdf55b767d2b`,
and O3 is published at `a307d1274a88a64ed6dd9a334f4f757f6d67ed80`. The current
published baseline is `9d0e2a225f4b9c41ac4f41a8ae125c4e9ad98e11`. The minimum
portable Council contracts are published at
`6fe01f7dd0d756a757bea8213803f0e23c42bfab` and accepted as the current executable
checkpoint. They do not validate a model, external truth,
executor, dispatcher, approval workflow, retrieval service, runtime integration,
evidence authenticity, generalized ontology, or cloud adapter.

R4A documentation was completed ahead of O3 to position OpenClaw correctly as a
candidate reference runtime without advancing executable work. The portable contracts
are accepted, and the documentation-only R4B entry-gate review is complete. Its sole
progression result is that a separate bounded authorization-and-experiment-design packet
may be proposed. R4B remains unauthorized; installation and execution remain blocked
pending completion and human approval of that later packet's prerequisites and actions.
