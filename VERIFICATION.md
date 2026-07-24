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

## R2 verification — 2026-07-24

All commands ran from `C:\dev\source\Repos\local-ai-guild` using public or synthetic fixtures. The accepted baseline was `6c44970351fa2a59d78b51c8d2a441af381582ef`.

During implementation, the first Ruff pass found two modern import-placement findings, one long line, and one unused test import. After correction, Ruff formatting identified two new source files and later one policy file for mechanical formatting. The first complete behavioral run then passed 110 tests and exposed one test-expectation mismatch: the combined helper correctly rejected a raw dictionary with the bounded `EvidenceEnvelopeError`, while the test expected `TypeError`. The test was aligned with the public error contract. Subsequent focused and final runs passed.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The editable project was refreshed in the repository-local Python 3.12.6 environment. Pydantic 2.13.4 remained the sole runtime dependency; Ruff 0.15.22 and pytest 8.4.2 remained development dependencies. No AI runtime or AI SDK was installed or invoked.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, 13 Python files were already formatted, pytest collected and passed 117 tests in 0.39 seconds, the CLI reported R2, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Result: exit 0, `All checks passed!`

```powershell
.\.venv\Scripts\python.exe -m ruff format --check .
```

Result: exit 0, `13 files already formatted`.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result: exit 0. Pytest collected 117 tests and all 117 passed in 0.37 seconds under Python 3.12.6 and pytest 8.4.2.

```powershell
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Result: exit 0.

```text
Project: Local AI Guild
Stage: R2: typed evidence envelopes and deterministic policy checks
```

```powershell
git diff --check
```

Result: exit 0 with no output.

```powershell
git status --short --branch
```

Result: exit 0. `main` matched `origin/main`; R2 source, tests, and documentation remained unstaged, uncommitted, and unpushed.

These checks establish only the deterministic typed evidence and non-executing policy behavior covered by the tests. Evidence provenance is metadata rather than cryptographic authenticity. An `allow` outcome is not execution, and no model, executor, dispatcher, approval workflow, retrieval system, runtime, persistence layer, or cloud integration was implemented or tested.

## R2 adversarial closeout audit — 2026-07-24

The audit began from accepted committed baseline `6c44970351fa2a59d78b51c8d2a441af381582ef`, which matched `origin/main`. Initial focused probes reproduced three boundary defects in the uncommitted R2 implementation:

- `https:example.com`, `http:example.com`, `file:readme.md`, and drive-like `c:readme.md` values passed the evidence identifier pattern.
- Direct routing and policy construction accepted caller-created `EvidenceReference` or `PolicyIssue` values that were equal to registry constants but were not the registry-owned instances.
- A combined policy envelope did not contain the immutable profile evaluated, so direct construction could pair a policy result with a contradictory profile claim.

The corrected implementation reserves `rule:` for routing evidence and `policy:` for policy evidence, constructs registries with an explicit duplicate check, requires registry object identity, rechecks the R1 decision/evidence mapping, rejects raw nested dictionaries and subclasses at trusted boundaries, constrains refusal issue content to the R1 redaction-safe vocabulary, and binds combined envelopes to the exact immutable profile whose semantics are re-evaluated during construction. These checks perform no parsing, execution, persistence, filesystem access, network access, or approval workflow.

```powershell
rg -n 'model_construct|\bconstruct\(|model_copy\s*\([^)]*update|SkipValidation|BeforeValidator|model_validate|TypeAdapter|validate_python' src/local_ai_guild/evidence.py src/local_ai_guild/policy.py
```

Result: exit 1 with no matches. R2 source uses no construction bypass, unchecked copy update, pre-validation coercion helper, or raw-data parser. Rejection-only Pydantic field validators do not coerce input.

```powershell
rg -n 'subprocess|os\.system|\bopen\s*\(|pathlib|requests|httpx|urllib|socket|importlib|__import__|\beval\s*\(|\bexec\s*\(|\bcompile\s*\(|logging|sqlite|sqlalchemy|pydantic_ai|\bopenai\b|anthropic|boto|azure|execute_tool|approval_workflow' src/local_ai_guild/evidence.py src/local_ai_guild/policy.py
```

Result: exit 1 with no matches. No execution, filesystem, network, dynamic import, compilation, logging, database, model SDK, cloud SDK, tool execution, or approval-workflow surface was found in R2 source.

```powershell
rg -n 'read_text|write_text|read_bytes|write_bytes|mkdir|makedirs|unlink|remove\s*\(|rename\s*\(|replace\s*\(|rmdir|shutil|tempfile|glob\s*\(|iterdir|exists\s*\(|is_file\s*\(|is_dir\s*\(' src/local_ai_guild/evidence.py src/local_ai_guild/policy.py
```

Result: exit 1 with no matches. No indirect `pathlib`, directory, temporary-file, or other filesystem method was found in R2 source.

```powershell
rg -n --hidden -g '!.git/**' -g '!.venv/**' -e 'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(?i)(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*["''][^"'']{8,}["'']' .
```

Result: exit 1 with no matches. The repository credential-pattern scan found no candidate key, token, private-key block, or quoted credential assignment. Test markers and fixtures remain public or synthetic.

```powershell
.\.venv\Scripts\python.exe -c "import tomllib, pathlib; print(tomllib.loads(pathlib.Path('pyproject.toml').read_text(encoding='utf-8'))['project']['dependencies'])"
```

Result: exit 0, `['pydantic>=2,<3']`. Pydantic remains the sole runtime dependency.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The editable project was refreshed in the repository-local Python 3.12.6 environment. Existing Pydantic 2.13.4, Ruff 0.15.22, and pytest 8.4.2 installations satisfied the project; no AI runtime or SDK was installed or invoked.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, 13 Python files were already formatted, all 178 tests passed in 0.36 seconds, the CLI reported R2, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Result: exit 0, `All checks passed!`

```powershell
.\.venv\Scripts\python.exe -m ruff format --check .
```

Result: exit 0, `13 files already formatted`.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result: exit 0. Pytest collected 178 tests and all 178 passed in 0.40 seconds under Python 3.12.6 and pytest 8.4.2.

```powershell
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Result: exit 0.

```text
Project: Local AI Guild
Stage: R2: typed evidence envelopes and deterministic policy checks
```

```powershell
git diff --check
```

Result: exit 0 with no output.

```powershell
git status --short --branch
```

Result: exit 0. `main` remained at `6c44970351fa2a59d78b51c8d2a441af381582ef`, matching `origin/main`. All R2 source, test, and documentation changes remained unstaged, uncommitted, and unpushed.

The final audit covered direct inconsistent construction, exact-type and subclass behavior, strict enum and collection inputs, URL-like identifiers, registry uniqueness and cross-registry rejection, caller-created lookalike metadata, R1 success/refusal evidence separation, all policy precedence branches and collisions, empty-allowlist denial, marker isolation, profile-bound combined envelopes, deterministic serialization, and absence of execution state. R2 remains a non-executing in-memory control-plane slice; evidence authenticity, profile persistence, approval workflow, tool execution, and all runtime integrations remain deferred.
