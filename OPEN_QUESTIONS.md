# Open Questions

This file separates resolved design questions from questions deferred to later packets.

## Resolved in R1

- Use Pydantic v2 at untrusted validation and serialization boundaries; do not build a custom validation framework.
- Use three R1-only mock contracts: `project_status`, `search_public_docs`, and `read_public_doc`.
- Require at least one stable opaque rule identifier on every successful or refused routing decision.

## Deferred

- Which local runtime best satisfies the eventual adapter contract on available hardware?
- Which router, coding, embedding, and reranking candidates pass project-specific evaluations?
- What thresholds justify human-approved cloud escalation?
- What retention and redaction policy should govern local traces and benchmark history?
- How should active assets move between `E:\AI` and the `D:\AI` archive without breaking provenance?
- What evidence template and reviewer role should document future model, dataset, and adapter license decisions?
- What sanitization and independent-review checklist should govern exceptional work-derived fixtures?

## Resolved in R2

- Use typed `routing_rule` and `policy_rule` references with only `public` or `synthetic` provenance metadata.
- Use immutable registries for R1 routing evidence and deterministic policy evidence; never derive identifiers from user input.
- Use a deny-by-default profile with all three R1 mock tools allowlisted and `read_public_doc` requiring human approval.
- Keep evidence authenticity, approval workflows, execution, and persistence outside R2.

## Resolved in R3

- Use an immutable Python tuple for the first ten public or synthetic evaluation cases; do not add a data-file loader or dependency.
- Reject empty evaluation batches and preserve the declared case order in results.
- Compare independently stable fields while suppressing refusal-reason and routed-tool mismatches when routing outcomes differ.
- Keep mismatch output to registry-owned constant codes and messages and keep raw case input out of results and summaries.
- Treat a passing evaluation as deterministic contract conformance only, not model evaluation or external truth.
- Defer ontology discovery and evidence-trace design to the proposed analysis-only O1 packet.

## Resolved in O2

- Use one fixed TOML representation for the completed R2 trace and parse it only through standard-library `tomllib`.
- Keep the pilot to ten strict record types with embedded requirements and evidence rather than a generalized ontology or relationship graph.
- Distinguish contract validity from trace completeness. The official fixture is contract-valid but incomplete because no first-class R2 publication-approval record is present.
- Treat `unknown_from_repository` as an evidence limitation, not proof that approval failed or did not occur.
- Keep citation authenticity, citation freshness, external truth, human identity, approval authenticity, persistence, and generalized ontology design outside O2.

## Resolved in R4A

- Keep the AI Council portable and authoritative over institutional contracts and durable records; keep runtime operations behind replaceable adapters.
- Treat OpenClaw only as a candidate reference runtime and defer any selection or adoption ADR to R4C.
- Treat runtime memory as temporary, isolated, and non-authoritative.
- Require externally enforced isolation because a runtime cannot serve as its own security boundary.
- Preserve O3 as the next implementation packet and require minimum Council contracts before R4B.

## Resolved in O3

- Use one fixed public synthetic handoff fixture and an immutable repository-authored
  manual assertion; do not parse the experiment Markdown for findings.
- Preserve the existing validator unchanged. It detects four planted structural
  defects, while manual review uniquely detects the non-reciprocal publication edge.
- Compare finding code, subject identifier, and relationship only, with deterministic
  matched, manual-only, and validator-only partitions.
- Treat deterministic validation as structural consistency evidence only. It does not
  prove external truth, approval authenticity, artifact existence, or general ontology
  correctness.

## Resolved in the portable-contract checkpoint

- Use ten strict runtime-neutral contracts plus one exact in-memory proceeding for the
  minimum Council representation; do not add a generalized ontology or graph.
- Use Council-owned durable identifiers and SHA-256 frozen-position digests. Exclude
  runtime-native identity, sessions, models, workspaces, objects, and provider
  configuration from institutional authority.
- Store relationships in one canonical direction and derive reverse navigation. Do not
  require reciprocal duplicate edges.
- Keep verification separate from human approval, preserve decision dissent, make
  knowledge promotion request-only, and treat runtime events as non-authoritative
  telemetry.

## Resolved in the R4B entry-gate review

- The accepted portable contracts strongly represent the minimum Council flow and
  runtime-independent artifacts, but only partially support Gates 1 and 5 because no
  candidate adapter has been exercised.
- Gate 2 is blocked by the missing approved threat model, isolation design, independent
  controls, and teardown procedure. Gates 3, 4, and 6 require bounded runtime evidence.
- A separate bounded R4B authorization-and-experiment-design packet is ready to be
  proposed. This does not authorize R4B, installation, execution, selection, or adoption.

## Resolved in the R4B authorization package

- Propose official stable OpenClaw `v2026.7.1` at immutable commit
  `2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4` and no floating or prerelease
  candidate.
- Record the official MIT core license and third-party notice while leaving dependency,
  model, provider, intended-use, and legal approval to human review.
- Use a dedicated experiment-only WSL2 distribution with container-backed services
  where practical, loopback-only ingress, independently denied egress, no Windows home
  mount, separate role workspaces, and full teardown.
- Bound the proposed data, credentials, model routes, tools, workers, rounds, messages,
  invocations, tokens, time, compute, retries, cost, events, verification, comparison,
  stop, and residue controls on paper.
- Keep the model routes disabled with exact identifiers `unselected` until human review;
  do not select a model solely because OpenClaw supports it.
- Keep authorization `not_authorized`, decision `pending`, and all checklist items
  unchecked. The package performs no installation or execution.

## Resolved in the Human R4B authorization-review preparation

- Use `docs/PUBLICATION_INDEX.md` as the authoritative detailed ledger and keep concise
  current-state summaries elsewhere without removing historical evidence.
- Treat official OpenClaw release, package, dependency, license, notice, Node, and
  security metadata as bounded static evidence, not legal approval or runtime evidence.
- Prefer the exact complete local Qwen2.5-Coder 7B artifact provisionally for all four
  roles and both runtime paths, but leave the model plan `unresolved` because no exact
  runtime-visible route was confirmed.
- Keep cloud routing excluded, credentials absent, and the deterministic dispatcher and
  verifier model-free.
- Record Codex's advisory recommendation as `recommend_defer`; keep the human decision
  `pending`, authorization `not_authorized`, and all approval items unchecked.

## Resolved in R4B local-model route qualification

- The complete local Ollama Qwen2.5-Coder 7B manifest and every blob match their direct
  SHA-256 identities; the manifest also matches the official Ollama registry response.
- The LM Studio Q5_K_M GGUF exactly matches its Hugging Face LFS object at the recorded
  conversion-repository revision.
- The Ollama route is conditionally qualified for a bounded public/synthetic capability
  benchmark at 8,192/2,048 context/output limits, subject to human license, limit, and
  benchmark authorization.
- The two complete artifacts are quantizations of the same Qwen family and do not
  support a heterogeneous model-diversity claim.

## Deferred to the capability benchmark, later R4B packets, or R4C

- Can the conditionally qualified model follow strict formats, cite bounded evidence,
  freeze independent positions, cross-review, preserve dissent, analyze security
  boundaries, audit provenance, and repeat results consistently?
- Does the exact route load and remain viable on the declared Windows/AMD hardware
  within the reduced context, memory, invocation, and time limits?
- Will a human or authorized legal reviewer accept the Apache-2.0, official Ollama
  redistribution, attribution, and missing conversion-source-revision conditions?
- Which external serialization and adapter mapping can preserve the accepted Council
  contracts without introducing runtime-native authority?
- Will the human accept the OpenClaw candidate provenance, core and dependency license
  posture, intended use, dedicated-WSL2 residual risks, teardown standard, and external
  controls?
- Will the human authorize optional dedicated credentials and cloud routing, or retain
  the preferred credential-free and cloud-disabled boundary?
- Can OpenClaw demonstrate the required role, session, workspace, memory, permission,
  routing, cost, and teardown boundaries under independent inspection?
- Does a smaller custom dispatcher produce better security, portability, auditability,
  and operational value?
- Which runtime, if any, should R4C select and record in the first runtime-selection ADR?
