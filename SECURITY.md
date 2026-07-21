# Security Policy

## Non-negotiable boundaries

- Models must never receive an unrestricted shell tool.
- Cloud delegation must never occur automatically.
- Future model workers must never commit or push automatically.
- Future tool arguments must be schema validated before execution.
- Future tool execution must be allowlisted, bounded, and audited.
- Secrets must never be stored in repository files, logs, traces, prompts, fixtures, generated environment reports, or benchmark output.

## Public-repository data boundary

This is a public repository. The following material must not be committed, logged, traced, or published here:

- Corporate or proprietary source code.
- Government, military, client, or contract data.
- Internal tickets, documentation, email, or chat content.
- Production logs, crash dumps, database contents, connection information, hostnames, internal endpoints, or network details.
- Credentials, API keys, tokens, certificates, private keys, or other secrets.
- Unsanitized prompts, traces, evidence bundles, evaluation datasets, or benchmark inputs derived from non-public work.
- Personal information that is not intentionally public.

Use public or synthetic fixtures by default. Work-derived material may enter this repository only after it has been sanitized, explicitly approved for this public repository, and independently reviewed before commit. Sanitization alone is not approval, and approval by the author alone is not independent review.

When provenance or publication rights are uncertain, treat the material as non-public and keep it out of the repository and its generated artifacts.

## License review boundary

Review the license and applicable use restrictions of every model, dataset, and adapter before adoption, especially before commercial, corporate, government, or contract-related use. Record the review as evidence before integration. R0 does not select a project license or approve any candidate model, dataset, or adapter license.

## Repository hygiene

- Commit example configuration only; real local configuration is ignored.
- Keep `.env` files, credentials, tokens, private keys, model weights, caches, runtime state, generated traces, evidence, and benchmark output untracked.
- Do not encode personal paths beyond the explicitly documented repository and planned storage locations.
- Review staged content and the full diff for secrets before any future commit.
- Review staged content for non-public provenance and publication approval before every commit.

## Script constraints

Repository scripts use strict mode, stop on errors, avoid elevation, and do not modify machine-wide settings. `bootstrap.ps1` may create only a repository-local virtual environment and install declared development dependencies. `show-environment.ps1` reports safe development facts and must not enumerate environment variables, credentials, network addresses, or identifiers.

## Reporting

If a secret is exposed, stop work, remove it from working files and generated artifacts, notify the owner, and rotate the secret. Rewriting Git history or deleting shared artifacts requires explicit human coordination.
