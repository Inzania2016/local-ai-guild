# Next Work Packet

## R1 — Typed tool contracts and deterministic mock router

### Goal

Create the first executable orchestration seam without connecting any model runtime.

### In scope

- Define typed request, tool proposal, routing decision, and validation-error contracts.
- Define two or three harmless mock tool identifiers with explicit argument schemas.
- Implement a deterministic rule-based mock router for a tiny documented task set.
- Reject unknown tools and invalid arguments.
- Add unit tests for successful routes, refusal paths, and stable serialization.
- Document how later model adapters may propose—but never directly execute—tool calls.
- Use only public or synthetic task examples and fixtures unless the public-repository approval process has been completed.

### Out of scope

- Model downloads or runtime configuration.
- LM Studio, Ollama, OpenCode, llama.cpp, MCP, HTTP, retrieval, cloud APIs, training, Docker, or unrestricted shell execution.
- Real filesystem mutation, network calls, commits, pushes, or automatic cloud delegation.

### Acceptance evidence

- Contracts and mock routing behavior are fully type annotated.
- Ruff and pytest pass.
- Tests prove invalid proposals are rejected before execution.
- Documentation clearly labels deterministic mock behavior as non-model behavior.
- Fixtures comply with the public-repository data boundary in `SECURITY.md`.
- No model, dataset, adapter, or project license is selected or approved by R1 unless a separately authorized license-review decision is added to scope.

### Open design inputs

Resolve only the R1-relevant questions identified in `OPEN_QUESTIONS.md`; defer runtime and hardware choices.
