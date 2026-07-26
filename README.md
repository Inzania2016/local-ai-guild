# Local AI Guild

Local AI Guild is a local-first orchestration project for routing bounded work among deterministic tools, local models, and explicitly approved cloud adapters. The repository is the durable control plane: policies, typed contracts, implementation code, tests, evaluation definitions, and traceable evidence live here. Model weights, runtime caches, and generated traces do not.

## Current status

The accepted published baseline is `6fe01f7dd0d756a757bea8213803f0e23c42bfab`.
O3 is published at `a307d1274a88a64ed6dd9a334f4f757f6d67ed80`. The published portable-contract checkpoint defines the minimum strict runtime-neutral Council contracts, one public synthetic in-memory proceeding, and deterministic cross-contract validation.
These contracts are not a completed Council implementation or runtime adapter. OpenClaw
remains an unevaluated candidate reference runtime. No provider, dispatcher, executor,
retrieval system, graph database, generalized ontology infrastructure, model runtime,
cloud integration, persistence layer, or training pipeline is implemented or claimed
to have been tested.

The only executable application behavior is a harmless status command. Bootstrap and use the repository-local interpreter:

```powershell
.\scripts\bootstrap.ps1
.\.venv\Scripts\python.exe -m local_ai_guild status
.\scripts\verify-repository.ps1
```

## Design principles

- Deterministic scripts establish facts; model output is treated as a proposal.
- Models may request narrow, approved tools but never receive unrestricted shell access.
- Important claims must link to evidence.
- Cloud delegation is explicit, policy-controlled, and never automatic.
- The system must provide value before custom model training exists.
- Delivery proceeds through small, independently verifiable work packets.

## R1 deterministic command language

Matching is case-sensitive. The router trims leading and trailing whitespace from the complete input, requires the documented space after each colon, and trims surrounding whitespace from the extracted query or path before contract validation.

```text
status
search docs: <query>
read doc: <repository-relative-markdown-path>
```

The three identifiers—`project_status`, `search_public_docs`, and `read_public_doc`—are R1-only test contracts, not production tools. Proposals are untrusted until validated. No executor exists, and the mock router never reads a file, runs a command, accesses a network, or mutates state.

Path validation is syntax-only. Leading `./` and uppercase `.MD` extensions are intentionally accepted as repository-relative Markdown forms. Surrounding path whitespace is normalized; traversal, absolute and drive-qualified paths, UNC forms, backslashes, colon-containing or URI-like forms, and non-Markdown final extensions are rejected. R1 does not decode URLs, resolve symlinks, canonicalize filesystem paths, or read files.

## R2 evidence and policy boundary

R2 resolves each validated R1 rule identifier through an immutable registry and produces a typed routing-decision envelope. The trusted builders and evaluator require exact validated model types and deliberately reject subclasses, raw dictionaries, standalone proposals, and arbitrary objects. Routing evidence uses the `rule:` namespace and policy evidence uses `policy:`; URI-like, drive-like, cross-namespace, unknown, duplicate, and semantically inconsistent identifiers fail closed. Evidence identifiers are deterministic references, not proof of external truth. The `public` and `synthetic` provenance labels are metadata, not cryptographic authenticity.

Policy accepts only a validated routing envelope and immutable profile. It refuses R1 refusals and tools outside the selected allowlist, requires human approval for `read_public_doc` under the default profile, and otherwise returns `allow`. The combined envelope contains the exact in-memory profile evaluated so direct construction cannot pair a result with a different profile. This is not profile persistence or an approval workflow. An `allow` outcome does not execute a tool. R2 stores no raw request, writes no trace or audit record, and has no executor.

## R3 deterministic evaluation boundary

R3 defines strict expected-result, evaluation-case, bounded-mismatch, case-result, and summary contracts. The immutable case set contains ten public or synthetic routing and policy cases. Evaluation calls `route_user_input()`, wraps and evaluates the decision through the existing R2 helper, compares stable outcomes in a fixed order, and stops with an in-memory summary. Case results and summaries are evaluator-built; trusted boundaries recheck their private, non-serialized case bindings so unchecked copies or directly forged aggregates are not accepted as evaluated output.

Passing cases establish only that the current deterministic R1/R2 implementation matched the repository-owned synthetic expectations. Expected results are test assertions, not observations of external truth or model-quality scores. Results exclude raw commands, queries, document paths, exception text, timing, execution state, and arbitrary caller metadata. R3 exposes no evaluation CLI command and writes no schemas, traces, or benchmark history.

## O2 fixed R2 evidence-trace pilot

O2 parses only `docs/traces/r2-closeout.toml` with Python 3.12 standard-library `tomllib`. The fixed loader accepts no caller path and performs the pilot's only new runtime I/O. The fixture is repository content rather than wheel package data, so this pilot supports a repository checkout or editable install and does not claim standalone installed-wheel support. Ten strict record contracts preserve typed requirements, evidence locators, authorities, constraints, decisions, artifacts, verification, the publication gate, the R2 commit identity, and the documented R3 next action. Relationships are checked in memory without reading cited files, inspecting Git, running commands, resolving URLs, or validating external facts.

The trace contract is structurally valid, but its deterministic result is trace-incomplete because the repository lacks a first-class record of the human authorization event for R2 publication. This does not mean approval failed or did not occur. The validator also records that commit identity proves neither authorization nor correctness and that repository assertions are not external truth. O2 is not a repository progression gate and exposes no trace CLI command.

## O3 synthetic handoff completeness experiment

O3 parses only `docs/traces/o3-synthetic-handoff.toml` through the zero-argument
`load_o3_trace()` fixed loader. The fixture describes a clearly fictional documentation
metadata packet and plants five contract-valid semantic handoff defects. The unchanged
O2 validator detects four; the immutable repository-authored manual assertion detects
those four plus a non-reciprocal publication edge outside current validator semantics.

`run_o3_handoff_experiment()` compares only finding code, subject identifier, and
relationship. It returns deterministic matched, manual-only, and validator-only tuples
without raw TOML, packet prose, paths, parser errors, or free-form messages. Manual
findings are experiment assertions, and deterministic findings establish structural
consistency only. Neither proves external truth, approval authenticity, artifact
existence, or general ontology correctness. O3 adds no experiment CLI command,
mutation, persistence, runtime, model, OpenClaw component, routing, retrieval, or
execution. O3 is published at `a307d1274a88a64ed6dd9a334f4f757f6d67ed80`.

## Minimum portable Council contracts

The checkpoint defines strict, frozen, extra-forbid contracts for roles, work packets,
frozen positions, cross-reviews, evidence, verification, approval requests, decisions,
knowledge-promotion requests, and bounded runtime events. Council-owned durable
identifiers remain authoritative; runtime agent IDs, sessions, model names, workspace
paths, provider configuration, and runtime-native objects are absent from the
institutional contracts.

One immutable public synthetic proceeding covers two independently frozen positions,
cross-review, deterministic verification, a human approval request, a
disagreement-preserving decision, a knowledge-promotion proposal, and portable runtime
telemetry. The validator reports bounded registry-owned issues for essential
cross-contract failures and performs no I/O or mutation.

Relationships have one canonical stored direction. Reverse navigation is derived and
non-authoritative, resolving O3's manual-only reciprocal-publication question without
adding duplicate edges. `RuntimeEvent` is operational telemetry correlated through
Council IDs, not institutional truth. Verification cannot establish human approval,
approval requests execute nothing, and knowledge-promotion requests mutate nothing.

## Portable Council runtime planning

R4A defines the AI Council as a portable institutional layer that owns roles, work packets, deliberation, evidence, verification, approval, decisions, knowledge promotion, and audit standards. A future runtime adapter may own sessions, models, tools, workers, scheduling, permissions, events, and runtime-specific messaging, but runtime state cannot become authoritative Council state.

OpenClaw is documented only as a **candidate reference runtime** for a future, separately authorized R4B proof of concept. No OpenClaw installation, configuration, adapter, model, skill, session, or runtime execution exists. The portable boundary, objective requirements, knowledge policy, and proposed experiment are documented in:

- `docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md`
- `docs/architecture/COUNCIL_RUNTIME_REQUIREMENTS.md`
- `docs/architecture/KNOWLEDGE_PROMOTION_POLICY.md`
- `docs/experiments/OPENCLAW_REFERENCE_RUNTIME_POC.md`

## Planned storage layout

- Repository: `C:\dev\source\Repos\local-ai-guild`
- Active models, runtimes, caches, and active workspace assets: `E:\AI`
- Archives, datasets, experiments, benchmark history, and backups: `D:\AI`

These locations are documented plans, not evidence that the directories or runtimes have been configured.

## Repository map

- `config/`: tracked examples; real local configuration is ignored
- `docs/architecture/`: planned system boundaries and flows
- `docs/decisions/`: future architecture decision records
- `docs/experiments/`: experiment designs and results
- `docs/verification/`: durable verification procedures
- `docs/traces/`: fixed, repository-reviewed trace fixtures
- `src/local_ai_guild/`: Python package
- `tests/`: deterministic automated tests
- `evals/`: reserved for separately approved future evaluation artifacts
- `artifacts/`: ignored generated evidence, traces, and benchmark results

Read [PROJECT_STATE.md](PROJECT_STATE.md) for confirmed current facts, [ROADMAP.md](ROADMAP.md) for staged plans, and [NEXT_WORK_PACKET.md](NEXT_WORK_PACKET.md) for the single proposed next packet.

## Security

This is a public repository. Use public or synthetic fixtures by default. Never add non-public work material, production data, credentials, internal network details, unsanitized work-derived prompts or traces, or personal information that is not intentionally public. Work-derived material requires sanitization, explicit repository approval, and independent review before commit. Model, dataset, and adapter licenses require review before adoption. See [SECURITY.md](SECURITY.md).

## Development

Python 3.12 is pinned in `.python-version`. Development dependencies are Ruff and pytest only. The bootstrap script creates `.venv` inside the repository and installs the declared project dependencies; it does not install system software or change machine-wide settings.

No commits or pushes are performed by repository scripts.
