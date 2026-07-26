# Roadmap

Roadmap items are planned stages, not promises that features exist.

## R0 — Repository control plane

Authority documents, architecture boundaries, safe scripts, a typed Python package skeleton, tracked configuration examples, tests, and verification conventions.

## R1 — Typed tool contracts and mock router

Define the first small set of typed request/result contracts and a deterministic mock router. No model runtime connection.

## R2 — Evidence envelopes and policy checks

Define evidence references, validation failures, allowlist decisions, and redaction-safe audit records.

## R3 — Evaluation harness

Create versioned public or synthetic routing/policy cases, deterministic typed comparisons, bounded case results, and an in-memory summary before selecting models. Do not connect a runtime or persist benchmark history.

## O1 — Read-only ontology discovery and evidence-trace pilot design

Under a separately approved analysis-only packet, inventory implicit workflow entities, relationships, epistemic states, and lifecycle states, then design one narrow R2 work-packet trace pilot. The first pass makes no repository, prompt, role, or implementation changes.

## O2 — R2 evidence-trace validation pilot

Represent the completed R2 packet in one fixed repository-owned TOML trace, validate strict typed relationships deterministically, and stop with bounded in-memory findings. Do not add generalized ontology, graph, retrieval, persistence, execution, model, runtime, or approval infrastructure.

## O3 — New-packet handoff completeness experiment

Implement one public synthetic completed packet and one contract-valid incomplete
R2-style trace, then compare a repository-authored manual assertion with the existing
deterministic validator. O3 keeps matched, manual-only, and validator-only findings
distinct and adds no validator rule, automatic state promotion, routing, retrieval,
persistence, runtime, or graph infrastructure.

## R4A — Portable Council runtime boundary

Define the runtime-neutral AI Council concepts, ownership boundary, adapter operations, objective runtime requirements, knowledge-promotion policy, OpenClaw candidate mapping, proof-of-concept design, and isolation recommendation. Add no runtime code and do not install or execute a runtime.

R4A was completed early as a documentation-only architecture stage so the OpenClaw candidate could be placed behind the correct portable boundary. O3 now supplies the
synthetic handoff experiment that remained next after R4A. R4B stays blocked until O3
is accepted and the minimum portable Council contracts are defined and accepted.

## R4B — OpenClaw reference-runtime proof of concept

Under a separately approved packet, test OpenClaw only as a candidate reference runtime against the R4A requirements and compare it with a smaller custom dispatcher. R4B cannot begin until the minimum portable Council contracts are defined and accepted. Runtime installation, model configuration, and execution require explicit authorization.

## R4C — Runtime adoption decision

Review R4B evidence, security and operational cost, portability, and alternatives. Record the human runtime decision in the first runtime-selection ADR. Until this stage completes, no candidate is selected, approved, or adopted.

## R5 — First adopted runtime implementation

Under a separately approved implementation packet, build the first adapter for the runtime selected in R4C. Preserve Council-owned contracts and authority outside runtime-native state.

## Later stages

Retrieval experiments, bounded coding work, optional cloud escalation adapters, and possible router fine-tuning follow only after earlier gates produce evidence.
