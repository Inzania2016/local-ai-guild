# Vision

Local AI Guild will coordinate narrow, evidence-backed work across deterministic tools, local models, and deliberately approved cloud escalation.

The AI Council is the planned portable institutional layer for multi-role deliberation. It owns role and work-packet contracts, evidence and verification rules, approval and decision formats, knowledge promotion, and audit standards. Runtime adapters remain replaceable operational hosts. OpenClaw is a candidate reference runtime, not a selected or adopted runtime, and Council design must not depend on OpenClaw-native state.

## Target capabilities

- **Tiny tool router:** classify requests and propose one of a small set of approved tools.
- **Retrieval and reranking service:** locate bounded context and rank evidence.
- **Local coding worker:** perform constrained coding and documentation tasks.
- **Policy and dispatch layer:** validate requests, enforce permissions, and choose execution paths.
- **Cloud escalation adapters:** invoke cloud models only after explicit policy and human approval conditions are satisfied.
- **Evidence and audit subsystem:** retain traceable inputs, decisions, tool results, and verification claims without retaining secrets.
- **Portable AI Council:** conduct bounded independent analysis, cross-review, evidence audit, disagreement-preserving synthesis, and human-controlled decisions through runtime-neutral artifacts.
- **Replaceable runtime adapters:** map portable Council operations to a bounded runtime without transferring institutional authority into sessions, memory, configuration, or runtime identifiers.

These are planned roles, not implemented components.

## Initial model hypotheses

- MiniCPM5-1B Agentic Tooluse may be an initial router candidate.
- Needle may be a future fine-tuned router candidate.
- Ornith-1.0-9B may be a local coding-worker candidate.
- Qwen3 embedding and reranking models may be retrieval candidates.

Every candidate requires local evaluation against project-specific tasks. No choice is final, and R0 makes no quality, compatibility, performance, or hardware-fit claim about any candidate.

## Success characteristics

The system remains useful without custom training, defaults to deterministic proof, confines every tool call to an auditable contract, and escalates cost or authority only when measured task requirements justify it.
