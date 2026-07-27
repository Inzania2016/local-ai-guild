# Next Work Packet

## R4B local-model route qualification

This is the smallest unresolved prerequisite identified by the advisory Human R4B
authorization review. It is a read-only inventory and provenance packet. It does not
approve installation or execution and does not make the human R4B decision.

### Authority boundary

The packet must not:

- load or invoke a model;
- download, convert, quantize, copy, or delete a model artifact;
- start or configure a model server;
- create or change WSL2, VM, container, filesystem, network, firewall, credential,
  provider, agent, session, route, or runtime state;
- install or execute OpenClaw;
- implement the adapter, dispatcher, exporter, verifier, or teardown automation;
- check an authorization item, change `not_authorized`, select OpenClaw, or create the
  R4C runtime-selection ADR.

If a read-only runtime command cannot be proven side-effect free, prefer static
manifest, file, and official-source inspection. Record any unavoidable observed
side effect and restore the prior process state.

### Entry evidence

- `docs/experiments/R4B_HUMAN_AUTHORIZATION_REVIEW.md`
- `docs/research/R4B_OPENCLAW_LICENSE_REVIEW.md`
- `docs/experiments/R4B_DATA_BUNDLE_MANIFEST.md`
- `docs/experiments/R4B_AUTHORIZATION_PACKET.md`
- the complete local Ollama Qwen2.5-Coder 7B manifest/blob identity recorded in the
  human review
- the local LM Studio GGUF inventory recorded in the human review

### Goal

Reconcile one exact installed local-model identifier with an immutable local artifact
identity and establish whether that exact artifact could later be made available inside
the proposed dedicated-WSL2 boundary under a separately authorized process.

### Required review

- Confirm, without loading or invoking a model, whether the pinned Ollama
  `registry.ollama.ai/library/qwen2.5-coder:7b` artifact is registered under one exact
  local route.
- Reconcile its manifest, model/config/license blob digests, quantization, apparent
  size, official Apache-2.0 provenance, and intended-use status.
- Determine whether the existing artifact is already accessible to the proposed
  environment or would require a later authorized copy or acquisition. Do not perform
  either action.
- Use the same exact role-model route for all four Council roles and both the OpenClaw
  and custom-dispatcher paths, or keep selection unresolved.
- Keep the deterministic dispatcher and verifier model-free and keep cloud routing
  excluded.
- Record capability as unverified; presence and registration do not establish quality.

### Required result

Record exactly one:

- `qualified_for_renewed_human_review`: one immutable artifact and exact local route
  pass the bounded license, intended-use, and availability review;
- `deferred`: the smallest remaining identity, provenance, availability, or isolation
  gap is named; or
- `rejected`: the candidate is ineligible and the reason is preserved.

Even `qualified_for_renewed_human_review` authorizes no environment creation,
installation, model load, inference, or R4B execution. The following packet would be a
separate human decision record, not an installation packet.

### Recommended model

Use GPT-5.6 Sol High because the work combines local artifact identity, runtime
registration, provenance, license, intended-use, and isolation-boundary reasoning.
Use xhigh only if immutable identity or WSL2 availability evidence materially
contradicts the current review.
