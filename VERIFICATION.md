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

## R1 verification — 2026-07-21

All commands ran from `C:\dev\source\Repos\local-ai-guild`. R1 used only public or synthetic test values.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The repository-local Python 3.12.6 environment installed the declared editable project and sole runtime dependency, Pydantic 2.13.4. No AI runtime or AI SDK was installed or invoked.

During implementation, the first Ruff check exited 1 with three Python 3.12 type-alias style findings and one line-length finding. After those corrections, the first formatting check identified one test file requiring formatting. The following command reformatted that file and exited 0:

```powershell
.\.venv\Scripts\python.exe -m ruff format tests\test_contracts.py
```

Final verification commands and results:

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, nine Python files were already formatted, pytest collected and passed 34 tests, the CLI reported the R1 stage, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Result: exit 0, `All checks passed!`

```powershell
.\.venv\Scripts\python.exe -m ruff format --check .
```

Result: exit 0, `9 files already formatted`.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result: exit 0. Pytest collected 34 tests and all 34 passed in 0.50 seconds under Python 3.12.6 and pytest 8.4.2.

```powershell
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Result: exit 0.

```text
Project: Local AI Guild
Stage: R1: typed tool contracts and deterministic mock router
```

```powershell
git diff --check
```

Result: exit 0 with no output.

```powershell
git status --short --branch
```

Result: exit 0. `main` matched `origin/main`; R1 source, tests, and documentation were modified or untracked and remained uncommitted.

These checks prove the deterministic R1 contracts and mock routing behavior covered by the tests. They do not prove or claim model behavior, tool execution, retrieval, runtime integration, or cloud integration.

## R1 closeout audit — 2026-07-21

The complete R1 diff and every new or modified Python file were inspected adversarially. A targeted probe found that Pydantic's `include_input=False` did not by itself provide complete redaction: an invalid discriminator value appeared inside the Pydantic error message, and attacker-chosen extra field names appeared in the error location. The converter was corrected to emit only stable error codes, bounded generic messages, and allowlisted schema-owned location components. Unknown location components become `<redacted>`.

Focused tests were added for boundary configuration, integer and Boolean strictness, non-string paths, nested extra fields, every discriminator/argument mismatch, empty-argument rules, redaction markers, evidence isolation, case sensitivity, fuzzy-match refusal, and the required path edge-case matrix.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The editable project was refreshed in the repository-local Python 3.12.6 environment. Pydantic 2.13.4 remained the sole runtime dependency; Ruff 0.15.22 and pytest 8.4.2 remained development dependencies.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, nine Python files were already formatted, pytest collected and passed 62 tests in 0.21 seconds, the CLI reported R1, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Result: exit 0, `All checks passed!`

```powershell
.\.venv\Scripts\python.exe -m ruff format --check .
```

Result: exit 0, `9 files already formatted`.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result: exit 0. Pytest collected 62 tests and all 62 passed in 0.32 seconds.

```powershell
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Result: exit 0.

```text
Project: Local AI Guild
Stage: R1: typed tool contracts and deterministic mock router
```

```powershell
git diff --check
```

Result: exit 0 with no output.

```powershell
git status --short --branch
```

Result: exit 0. `main` remained at accepted baseline `14f90483279b2739ea41739bdabae882666f48de`, matching `origin/main`; all R1 changes remained unstaged, uncommitted, and unpushed.

Source scans found no construction or validation-bypass API, unchecked model-copy update, execution surface, filesystem I/O, network client, dynamic import, logging, persistence, cloud SDK, or model SDK. The only dictionary-shaped package output is generated JSON Schema. All externally reachable boundary models inherited strict validation, forbidden extras, and frozen instances.
