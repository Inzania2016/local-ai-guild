# Knowledge Promotion Policy

## Purpose

This policy keeps temporary runtime memory separate from durable Council knowledge. It applies to every candidate runtime, including OpenClaw. Runtime memory is non-authoritative working state and cannot promote itself.

## Knowledge classes

| Class | Meaning | Authority |
| --- | --- | --- |
| Authoritative knowledge | Durable institutional rules or accepted facts within a declared scope. | Council-controlled source with applicable human authority and review. |
| Current operational state | Time-sensitive state used to coordinate an active packet or system. | Named state owner; expires or is refreshed. |
| Verified evidence | Evidence whose declared method and checks passed within documented limitations. | Verification record, not automatic institutional authority. |
| Approved decisions | Human decisions with scope, rationale, authority, evidence considered, and durable approval record. | Named human authority under Council rules. |
| Temporary working memory | Runtime context, notes, summaries, caches, and intermediate messages. | None; disposable and non-authoritative. |
| Unverified observations | Reported or retrieved material not yet verified. | None beyond its declared provenance. |
| Hypotheses | Testable explanations or predictions. | None; require evidence and review. |
| Recommendations | Proposed actions with rationale, tradeoffs, and uncertainty. | Advisory only until an authorized decision. |

Classification describes epistemic and institutional status; it does not prove truth. Public availability, a runtime memory entry, repeated model agreement, or a Git commit does not by itself create authority.

## Promotion requirements

A proposal to promote material from runtime memory or another lower-authority class must include:

1. A source or evidence reference.
2. An explicit epistemic classification.
3. Review appropriate to the claim and its risk.
4. Human approval where institutional authority is involved.
5. A durable approval record and rationale.
6. Freshness or expiration metadata.

The request must also identify its target knowledge class, scope, owner, dissent or unresolved uncertainty, and the source runtime correlation only when needed for audit.

## Promotion procedure

1. Export the candidate material from runtime memory into a bounded `KnowledgePromotionRequest`.
2. Remove secrets, private data, transient runtime identifiers, and unsupported claims.
3. Attach source evidence and classify provenance, epistemic status, freshness, and limitations.
4. Run deterministic checks appropriate to the artifact.
5. Obtain independent review; use adversarial or domain review when risk warrants it.
6. Obtain a human decision when the target class carries Council authority.
7. Write the accepted material, rationale, review evidence, expiration, and approval record into Council-controlled durable storage.
8. Retain dissent and rejected alternatives when they materially affect interpretation.
9. Expire, supersede, or demote material when its freshness or supporting evidence no longer holds.

## Prohibited promotions

The following cannot establish promotion:

- A runtime writing to its own memory.
- A runtime event or session status alone.
- Model consensus without evidence and review.
- Tool execution without an applicable verification result.
- A Git commit without approval and evidence semantics.
- A runtime-native “approved,” “important,” or “remember” flag.
- Copying a session transcript into durable storage without classification and review.
- Converting personal, proprietary, or other non-public material into Council knowledge without the repository's sanitization, approval, and independent-review requirements.

## OpenClaw boundary

OpenClaw memory, if evaluated later, remains temporary working memory. It may support continuity inside a bounded experiment but cannot become the source of truth for roles, packets, evidence, decisions, approvals, or promoted knowledge. Durable Council records must remain external, portable, reviewable, and usable after the runtime is removed.

## Freshness and revocation

Every promoted item must declare how freshness is evaluated and, where applicable, an expiration or review date. Revocation or supersession preserves the historical decision record while preventing stale material from being presented as current authority.

R4A defines this policy conceptually. It adds no memory store, promotion engine, runtime hook, or automatic state transition.
