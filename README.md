# Local AI Guild

Local AI Guild is a local-first orchestration project for routing bounded work among deterministic tools, local models, and explicitly approved cloud adapters. The repository is the durable control plane: policies, typed contracts, implementation code, tests, evaluation definitions, and traceable evidence live here. Model weights, runtime caches, and generated traces do not.

## Current status

The project is at **R3: deterministic evaluation harness**. R3 runs a fixed set of versioned public or synthetic cases through the existing R1 router and R2 evidence/policy pipeline, compares only stable typed outcomes, and returns bounded in-memory results. It does not execute tools, connect a model runtime, persist benchmark history, or prove external correctness. No provider, dispatcher, executor, retrieval system, cloud integration, or training pipeline is implemented or claimed to have been tested.

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
