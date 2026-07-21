# Agent Operating Rules

These rules apply to every human or model-assisted change in this repository.

## Authority order

1. The current user-approved work packet and explicit user instructions.
2. `SECURITY.md` and `VERIFICATION.md`.
3. `PROJECT_STATE.md`, `DECISIONS.md`, and `NEXT_WORK_PACKET.md`.
4. Planned architecture and roadmap documents.

When documents disagree, stop and surface the conflict. Do not silently broaden scope.

## Working rules

- Separate confirmed current facts from plans, hypotheses, experiments, and unresolved questions.
- Keep changes within the named work packet.
- Prefer deterministic, typed, testable behavior.
- Attach important claims to reproducible evidence.
- Never claim a runtime, model, integration, or benchmark was tested unless the command was actually executed and recorded.
- Preserve user changes and inspect the full diff before handoff.
- Do not commit, push, open pull requests, or delegate to cloud services without explicit human approval.
- Do not install or invoke AI runtimes unless a later work packet explicitly authorizes it.

## Public-repository data boundary

- Treat this repository, its Git history, issues, and published artifacts as public.
- Never commit, log, trace, or publish corporate or proprietary source; government, military, client, contract, or internal work data; internal tickets, documentation, email, or chat; production logs, crash dumps, database contents, connection details, hostnames, internal endpoints, or network details.
- Never include credentials, API keys, tokens, certificates, secrets, non-public personal information, or unsanitized prompts, traces, evidence bundles, evaluation datasets, or benchmark inputs derived from non-public work.
- Use public or synthetic fixtures by default.
- Work-derived material requires sanitization, explicit approval for this public repository, and independent review before commit. If provenance or approval is unclear, exclude it.
- Review model, dataset, and adapter licenses before adoption, especially for commercial, corporate, government, or contract-related use. Do not infer license approval from technical suitability.

## Tool safety

- Never give a model unrestricted shell access.
- Future tools must be allowlisted, schema validated, bounded, and audited.
- Reject or safely encode unexpected paths and arguments.
- Keep secrets out of source, configuration examples, tests, fixtures, logs, traces, and evidence.
- Use repository-local environments and avoid elevation or machine-wide changes.

## Verification

Run `scripts/verify-repository.ps1` before handoff. Record exact commands and actual results in `VERIFICATION.md`. A successful build or unit test does not prove untested runtime or model behavior.
