# OpenClaw Reference-Runtime Proof-of-Concept Design

## Status and decision question

OpenClaw is a **candidate reference runtime**. It is not selected, approved, or adopted. This R4A document designs a possible R4B experiment; it does not authorize installation, configuration, download, execution, or access to models or tools.

The experiment asks:

> Should the AI Council use OpenClaw as its initial reference runtime, or should it build a smaller custom dispatcher?

The Council remains the portable institutional layer. The experiment evaluates whether OpenClaw can host bounded Council procedures without becoming authoritative Council state.

## Candidate mapping

| Council concept | Candidate OpenClaw primitive | Boundary |
| --- | --- | --- |
| Council members | Persistent agents | Agent identity and memory are runtime details; the `RoleContract` remains authoritative. |
| Temporary researchers | Subagents | Workers are depth-one, short-lived, narrower than the parent, and cannot promote knowledge. |
| Deliberation rounds | Isolated sessions | Session state is disposable; frozen positions are exported to Council-controlled storage. |
| Bounded capabilities | Skills | Only explicitly reviewed first-party capabilities may be considered; no marketplace skills. |
| Tool policy | Runtime enforcement | Runtime enforcement is defense in depth, not the sole permission or security boundary. |
| Role working areas | Separate workspaces | Each role receives a distinct, sanitized, least-privilege workspace. |
| Temporary working context | OpenClaw memory | Memory is non-authoritative, isolated, erasable, and excluded from durable Council records unless promoted under policy. |

The mapping is a hypothesis for evaluation. R4B must record mismatches rather than modifying Council concepts to fit runtime primitives.

## What OpenClaw cannot establish by itself

OpenClaw cannot independently establish:

- Human approval authenticity.
- Evidence authenticity.
- Institutional authority.
- Immutable decisions.
- Knowledge promotion.
- Frozen independent positions.
- Portable Council semantics.

These properties require Council-controlled contracts, external records, deterministic verification, independent controls, and applicable human authority.

## Structured experiment

The experiment uses public or synthetic material only and contains these phases:

1. **Structured decision packet:** Create one bounded `CouncilWorkPacket` containing the decision question, alternatives, criteria, constraints, evidence requirements, security boundary, budgets, and required decision record.
2. **Independent analysis by multiple agents:** Give at least two Council-member roles identical authorized inputs in isolated sessions without peer positions.
3. **Frozen initial positions:** Export and freeze each `IndependentPosition` before any cross-disclosure.
4. **Cross-review:** Deliver the immutable position bundle and collect explicit challenges, agreements, missing evidence, and unresolved disagreements.
5. **Security adversary:** Assign a separate role to attack isolation, permission, credential, memory, event-integrity, teardown, and authority-boundary claims.
6. **Evidence auditor:** Assign a separate role to check provenance, citation scope, freshness, claim support, and unsupported runtime assertions.
7. **Deterministic verification:** Run external deterministic checks over packet completeness, frozen artifacts, event records, budgets, limits, permission denials, and teardown evidence.
8. **Disagreement-preserving synthesis:** Produce a synthesis that retains material dissent, uncertainty, and failed criteria instead of forcing consensus.
9. **Human decision:** Present the evidence, tradeoffs, security review, costs, and disagreements to the authorized human; the runtime cannot approve itself.
10. **Durable external decision record:** Store the human decision, rationale, evidence, limitations, and follow-up conditions outside OpenClaw.

No phase performs autonomous coding or grants email, personal-account, messaging-channel, scheduling, financial, browser, or broad system access.

## Compared alternatives

Evaluate at least:

- OpenClaw as a bounded reference-runtime adapter.
- A smaller custom dispatcher implementing only the minimum portable Council operations.

Compare demonstrated capability, isolation, audit completeness, replaceability, operational complexity, attack surface, recovery, maintenance, and attributable cost. Feature count alone is not a success criterion.

## Required artifacts

- Structured decision packet.
- Role contracts and effective permission declarations.
- Frozen independent positions.
- Cross-reviews.
- Security-adversary report.
- Evidence-auditor report.
- Deterministic verification results.
- Bounded runtime-event export with documented omissions.
- Cost and routing report.
- Disagreement-preserving synthesis.
- Human approval or rejection record.
- Durable decision record.
- Teardown evidence.

All durable artifacts use Council-owned formats. Runtime-native exports are supporting observations only.

## Isolation recommendation

If R4B receives separate authorization, use:

- A dedicated WSL2 distribution or VM.
- Container-backed runtime services where practical.
- A loopback-only gateway.
- A separate workspace per role.
- No Windows home-directory mount.
- A read-only sanitized repository copy.
- Dedicated test credentials.
- No unrestricted shell.
- No browser, email, financial, or personal-account access.
- No third-party marketplace skills.
- No global shared memory.
- Subagent depth of one.
- Explicit token, runtime, and message limits.
- Full teardown after the experiment.

OpenClaw must be treated as untrusted and cannot serve as its own security boundary. Independent host, network, filesystem, credential, approval, and audit controls are required.

## Entry and stop conditions

The minimum Council contracts are now defined but remain pending human acceptance. R4B
cannot begin until a separate entry-gate review is accepted, licenses are reviewed, the
isolation design is approved, and a human explicitly authorizes installation and
execution.

Stop the experiment on any unauthorized network or cloud route, permission escape, cross-role memory exposure, missing required event record, unbounded loop or worker spawn, credential exposure, inability to freeze a position externally, or attempt to represent runtime state as Council approval or authority.

## Decision boundary

R4B evidence informs R4C. Only R4C may create the runtime-selection ADR and recommend adoption. Until that decision, OpenClaw remains a candidate reference runtime.
