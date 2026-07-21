# Verification

Last updated: 2026-07-21

This document records commands actually executed for R0. It must not be read as evidence for any model or runtime behavior.

## Environment observed before implementation

- PowerShell: 7.6.4
- Default `python`: 3.14.3
- Python 3.12 is available through the Windows Python launcher.
- Git: 2.51.1.windows.1
- GitHub CLI: 2.96.0

## R0 command record

All commands were run from `C:\dev\source\Repos\local-ai-guild` on 2026-07-21.

### Bootstrap

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. Created repository-local `.venv`, installed the declared editable project and development dependencies, and reported `Repository environment ready: Python 3.12.6`. Installed tool versions included Ruff 0.15.22 and pytest 8.4.2.

### Repository verification

```powershell
.\scripts\verify-repository.ps1
```

First result: exit 1. Ruff found one import-order violation in `tests/test_cli.py`; the script stopped and surfaced the nonzero exit. The import order was corrected.

Second result: exit 0. Ruff check passed, Ruff reported four Python files already formatted, pytest collected and passed one test, the CLI printed the expected identity and R0 stage, and the script reported `Repository verification passed.`

Final result after documentation, ignore-rule, and expected-path review: exit 0 with the same passing checks and output.

### Requested individual checks

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Result: exit 0, `All checks passed!`

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result: exit 0, one test passed in 0.01 seconds under Python 3.12.6 and pytest 8.4.2.

```powershell
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Result: exit 0.

```text
Project: Local AI Guild
Stage: R0: repository control plane and minimal skeleton
```

### Safe environment report

```powershell
.\scripts\show-environment.ps1
```

Result: exit 0. It reported PowerShell 7.6.4, default PATH Python 3.14.3, Git 2.51.1.windows.1, Windows 11 Home 10.0.26200, an Intel Core i7-9700F CPU, 31.9 GiB RAM, and free-space totals for fixed drives C, D, and E. It did not enumerate environment variables, credentials, API keys, MAC addresses, or network addresses.

## Claim boundary

Repository checks can establish file presence, lint cleanliness, formatting, deterministic tests, and CLI output. They cannot establish model quality, runtime compatibility, routing accuracy, retrieval quality, security of future integrations, or performance.

## R0 closeout — 2026-07-21

The complete repository content was inspected before publication. Authority documents were updated with the public-repository data boundary and the requirement to review model, dataset, and adapter licenses before adoption. No project or candidate license was selected or approved.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff check passed, four Python files were already formatted, pytest passed one test, the CLI printed the expected R0 status, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m local_ai_guild status
git diff --check
```

Results: every command exited 0. Ruff check passed; Ruff reported four files already formatted; pytest passed one test in 0.01 seconds; the CLI reported `Local AI Guild` at `R0: repository control plane and minimal skeleton`; and the diff whitespace check produced no errors.

The untracked and ignored sets were inspected. Ignore probes confirmed repository-local virtual environments, Python and quality-tool caches, real local configuration, generated traces, evidence, benchmark results, model files, log and crash output, local datasets, credential files, and secret-key formats remain ignored. Placeholder `.gitkeep` files remain publishable.

Credential-pattern and machine/network-identifier scans found no credential-like values, user-profile paths, IP addresses, MAC addresses, or internal endpoints in publishable repository content. The documented repository path and safe development facts in this file are intentional R0 records.
