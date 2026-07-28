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

## R3 verification — 2026-07-25

All commands ran from `C:\dev\source\Repos\local-ai-guild` using only public or synthetic cases. The accepted committed baseline was `903aa815a6e0176e682b4726ee8114627bd98940`, matching `origin/main`.

R3 added strict in-memory evaluation contracts, ten immutable versioned cases, exact-type single and batch evaluation functions, registry-owned bounded mismatch metadata, deterministic case results, and a consistent ordered summary. It did not change R1 or R2 behavior. Focused R3 tests passed before the complete suite ran.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The editable package was refreshed in the repository-local Python 3.12.6 environment. Existing Pydantic 2.13.4, pytest 8.4.2, and Ruff 0.15.22 satisfied the declared dependencies. No runtime, model, AI SDK, or additional dependency was installed or invoked.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, 16 Python files were already formatted, pytest collected and passed 263 tests in 0.97 seconds, the CLI reported R3, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Result: exit 0, `All checks passed!`

```powershell
.\.venv\Scripts\python.exe -m ruff format --check .
```

Result: exit 0, `16 files already formatted`.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result: exit 0. Pytest collected 263 tests and all 263 passed in 0.81 seconds under Python 3.12.6 and pytest 8.4.2.

```powershell
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Result: exit 0.

```text
Project: Local AI Guild
Stage: R3: deterministic evaluation harness
```

```powershell
rg -n 'model_construct|\bconstruct\s*\(|model_copy\s*\([^)]*update|SkipValidation|BeforeValidator|model_validate|TypeAdapter|validate_python' src/local_ai_guild/evaluation.py src/local_ai_guild/evaluation_cases.py
```

Result: exit 1 with no matches. R3 source contains no unchecked construction, copy-update bypass, coercion helper, or raw-data parser.

```powershell
rg -n 'subprocess|os\.system|\bopen\s*\(|pathlib|requests|httpx|urllib|socket|importlib|__import__|\beval\s*\(|\bexec\s*\(|\bcompile\s*\(|logging|sqlite|sqlalchemy|pydantic_ai|\bopenai\b|anthropic|boto|azure|\bmcp\b|\bembeddings?\b|\breranker\b|vector.?database|\brdf\b|\bowl\b|knowledge.?graph|\bontology\b|execute_tool|approval_workflow' src/local_ai_guild/evaluation.py src/local_ai_guild/evaluation_cases.py
```

Result: exit 1 with no matches. R3 source contains no execution, model, network, cloud, retrieval, persistence, approval-workflow, or ontology-infrastructure surface.

```powershell
rg -n 'read_text|write_text|read_bytes|write_bytes|mkdir|makedirs|unlink|remove\s*\(|rename\s*\(|replace\s*\(|rmdir|shutil|tempfile|glob\s*\(|iterdir|exists\s*\(|is_file\s*\(|is_dir\s*\(' src/local_ai_guild/evaluation.py src/local_ai_guild/evaluation_cases.py
```

Result: exit 1 with no matches. R3 source contains no direct or indirect filesystem method.

```powershell
.\.venv\Scripts\python.exe -c "import tomllib,pathlib; data=tomllib.loads(pathlib.Path('pyproject.toml').read_text(encoding='utf-8')); print(data['project']['dependencies']); print(data['project']['optional-dependencies']['dev'])"
```

Result: exit 0. Runtime dependencies remained `['pydantic>=2,<3']`; development dependencies remained `['pytest>=8.3,<9', 'ruff>=0.9,<1']`.

An inline boundary probe confirmed all five R3 boundary models inherit `strict=True`, `extra="forbid"`, and `frozen=True`; all ten versioned cases passed; and repeated complete evaluation serialization was byte-for-byte identical.

The repository credential-pattern scan found no candidate key, token, private-key block, or quoted credential assignment. The complete R3 case inventory was inspected and contains only public or synthetic commands, descriptions, paths, and marker values.

```powershell
git diff --check
```

Result: exit 0 with no output.

```powershell
git status --short --branch
```

Result: exit 0. `main` remained at `903aa815a6e0176e682b4726ee8114627bd98940`, matching `origin/main`. All R3 source, tests, and documentation remained unstaged, uncommitted, and unpushed.

These checks establish only deterministic conformance between the current R1/R2 implementation and repository-owned R3 synthetic expectations. No model was evaluated, no tool was executed, no external truth was established, no benchmark history was persisted, and no ontology functionality was implemented. The proposed O1 packet remains analysis-only and has not begun.

## R3 adversarial closeout audit — 2026-07-25

The closeout audit found and corrected two related R3 construction-boundary defects: a directly constructed result could be relabeled with another valid case identifier, and directly constructed results could be assembled into a caller-authored all-green summary. Case results and summaries are now evaluator-built. Trusted checks bind results privately to their case identifier and immutable expected result, bind summaries privately to ordered identifiers, and revalidate those non-serialized bindings after deliberate unchecked-copy corruption. No case input is retained by a result or summary.

Mismatch messages are now derived from their stable codes rather than accepted as constructor input. Registry construction explicitly rejects incomplete or duplicate mismatch-code definitions, registry constants remain identity-checked, and mismatch order is an explicit complete tuple rather than implicit enum or mapping iteration.

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_evaluation.py
```

Result: exit 0. All 85 focused R3 tests passed in 0.81 seconds. The focused suite includes deliberate test-only uses of `model_construct()` and `model_copy(update=...)` to corrupt cases, expectations, profiles, results, and summaries. Production R3 code uses neither API, and trusted evaluators or consistency checks reject every corrupted probe.

Four independent Python processes serialized the complete ten-case summary. All four outputs were byte-for-byte identical at 4,226 UTF-8 bytes. Four independent processes serialized the same deliberately failing synthetic case. All four outputs were byte-for-byte identical at 887 UTF-8 bytes and contained, in order, `routed_tool_mismatch`, `routing_evidence_mismatch`, `policy_outcome_mismatch`, `policy_issue_mismatch`, and `policy_evidence_mismatch`. Two complete evaluations in one process were also identical.

The complete official case evaluation returned ten cases, ten passes, zero failures, and preserved declared case order. All five public R3 boundary models again reported `strict=True`, `extra="forbid"`, and `frozen=True`.

Production-only parser-bypass scanning returned exit 1 with no matches for `model_construct`, deprecated `construct`, `model_copy`, `SkipValidation`, `BeforeValidator`, `model_validate`, `TypeAdapter`, or `validate_python`. The test-only scan found only the documented deliberate corruption probes.

Execution/infrastructure and filesystem-method scans returned exit 1 with no matches in `evaluation.py` or `evaluation_cases.py`. Credential scans found no private-key blocks, known token shapes, or non-empty quoted credential assignments. A private-network-address scan returned no matches; the only repository URLs were the existing synthetic `example.com` rejection fixtures.

Dependency inspection again reported `['pydantic>=2,<3']` as the sole runtime dependency and `['pytest>=8.3,<9', 'ruff>=0.9,<1']` as development dependencies.

The closeout corrections changed only R3 source, focused tests, and the R3 documentation needed to describe evaluator-built results and summaries. R1 and R2 implementation files remain unchanged. O1 remains documentation-only and has not begun.

## O2 verification — 2026-07-25

All commands ran from `C:\dev\source\Repos\local-ai-guild` against accepted published baseline `3285d4410111f512068b33d9581ba97bc7690bd2`, which matched `origin/main` before implementation. O2 used only public repository citations and synthetic invalid markers. All changes remained unstaged, uncommitted, and unpushed.

O2 added one fixed `docs/traces/r2-closeout.toml` fixture, strict trace contracts, a fixed standard-library TOML loader, and a deterministic in-memory semantic validator. The loader accepts no caller path. The verifier checks O2 file presence and the normal Python suite, but trace completeness is not a repository progression gate.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The editable package was refreshed in the repository-local Python 3.12.6 environment. Pydantic 2.13.4 remained the sole runtime dependency; pytest 8.4.2 and Ruff 0.15.22 remained development dependencies. No model, runtime, AI SDK, or additional dependency was installed or invoked.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, 22 Python files were already formatted, pytest collected and passed 361 tests in 4.07 seconds, the CLI reported `O2: R2 evidence-trace validation pilot`, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Result: exit 0, `All checks passed!`

```powershell
.\.venv\Scripts\python.exe -m ruff format --check .
```

Result: exit 0, `22 files already formatted`.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result: exit 0. Pytest collected 361 tests and all 361 passed in 2.11 seconds under Python 3.12.6 and pytest 8.4.2.

```powershell
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Result: exit 0.

```text
Project: Local AI Guild
Stage: O2: R2 evidence-trace validation pilot
```

```powershell
git diff --check
```

Result: exit 0 with no output.

```powershell
git status --short --branch
```

Result: exit 0. `main` remained at `3285d4410111f512068b33d9581ba97bc7690bd2`, matching `origin/main`; all O2 source, trace, test, and documentation changes were unstaged and uncommitted.

### Focused O2 tests

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_trace_contracts.py
.\.venv\Scripts\python.exe -m pytest tests/test_trace_loading.py
.\.venv\Scripts\python.exe -m pytest tests/test_trace_validation.py
```

Results: every command exited 0. Contract tests passed 63 tests in 0.41 seconds, loading tests passed 9 tests in 3.78 seconds, and validation tests passed 26 tests in 0.41 seconds. The 98 focused tests cover strict/frozen/extra-forbid boundaries, identifier and locator grammar, status combinations, all supported relationship shapes, registry completeness, the official fixture, bounded loader errors, unsafe corruption probes, result forgery, redaction, and same- and separate-process determinism.

### Official fixed trace result

```powershell
.\.venv\Scripts\python.exe -c "from local_ai_guild.trace_validation import validate_r2_trace; print(validate_r2_trace().model_dump_json())"
```

Result: exit 0. The contract-valid trace contained 30 ordered records and returned `trace_complete=false`, one error, zero warnings, and three informational findings in this order:

1. `missing_approval_evidence` for `approval_gate:r2-publication-v1`
2. `commit_does_not_prove_authorization` for `commit:r2-publication-v1`
3. `commit_does_not_prove_correctness` for `commit:r2-publication-v1`
4. `repository_assertion_not_external_truth` for `work_packet:r2-v1`

The approval message is `No first-class repository approval record is declared for this gate`. It does not assert that approval failed or did not occur. The known completeness error is the intended honest representation of the repository evidence gap and does not make O2 validation a mandatory progression gate.

### Determinism and dependencies

```powershell
.\.venv\Scripts\python.exe -c "from local_ai_guild.trace_validation import validate_r2_trace; a=validate_r2_trace().model_dump_json(); b=validate_r2_trace().model_dump_json(); assert a == b; print(f'same-process deterministic: true; utf8_bytes: {len(a.encode())}')"
```

Result: exit 0, `same-process deterministic: true; utf8_bytes: 1072`.

Two separate Python processes ran the official validation and their serialized results were compared case-sensitively.

Result: exit 0, `separate-process deterministic: true; utf8_bytes: 1072`.

```powershell
.\.venv\Scripts\python.exe -c "import tomllib,pathlib; data=tomllib.loads(pathlib.Path('pyproject.toml').read_text(encoding='utf-8')); print(data['project']['dependencies']); print(data['project']['optional-dependencies']['dev'])"
```

Result: exit 0. Runtime dependencies remained `['pydantic>=2,<3']`; development dependencies remained `['pytest>=8.3,<9', 'ruff>=0.9,<1']`. TOML parsing uses Python 3.12 standard-library `tomllib`.

### Security and prohibited-surface review

Credential-pattern and private-address scans covered repository content while excluding `.git`, `.venv`, bytecode, and caches. Both corrected commands exited 0 with explicit no-match output: no candidate access key, token, private-key block, or private IPv4 address was found. Synthetic `PRIVATE` and `MARKER` strings appear only in focused redaction and corruption tests and are asserted absent from errors and results.

The first composed private-address scan attempt failed because its regular expression used unsupported look-around in the default Ripgrep engine. The expression was replaced with an equivalent supported word-boundary form and the corrected scan passed. No repository change was needed.

```powershell
rg -n 'model_construct|\bconstruct\s*\(|model_copy\s*\([^)]*update|SkipValidation|BeforeValidator|model_validate|TypeAdapter|validate_python' src/local_ai_guild/trace_contracts.py src/local_ai_guild/trace_loading.py src/local_ai_guild/trace_validation.py
```

Result: exit 1 with no matches. Production O2 source contains no construction bypass, unchecked copy update, coercive parser helper, or general raw-data validation API. Deliberate `model_construct()` and `model_copy(update=...)` uses remain confined to tests that prove trusted-boundary rejection.

The first broad prohibited-surface expression reported only the three intentional `re.compile(...)` calls used for bounded syntax patterns. The scan was narrowed to distinguish regular-expression compilation from Python's code-compilation builtin.

```powershell
rg -ni 'subprocess|os\.system|requests|httpx|urllib|socket|importlib|__import__|(^|[^.A-Za-z0-9_])eval\s*\(|(^|[^.A-Za-z0-9_])exec\s*\(|(^|[^.A-Za-z0-9_])compile\s*\(|logging|sqlite|sqlalchemy|pydantic_ai|\bopenai\b|anthropic|\bboto\b|\bazure\b|\bmcp\b|\bembeddings?\b|vector.?database|\brdf\b|\bowl\b|\bsparql\b|knowledge.?graph|execute_tool|approval_workflow|glob\s*\(|rglob\s*\(|iterdir\s*\(|os\.walk|scandir\s*\(' src/local_ai_guild/trace_contracts.py src/local_ai_guild/trace_loading.py src/local_ai_guild/trace_validation.py
```

Result: exit 1 with no matches. Production O2 source contains no shell, subprocess, Git invocation, network client, dynamic import, code execution, logging, database, graph, retrieval, model, cloud, tool-execution, approval-workflow, directory-scan, glob, or recursive-loading surface.

The arbitrary-path surface scan returned no matches for caller paths, environment paths, path discovery, URLs, globbing, directory enumeration, or recursive loading. A separate fixed-I/O inspection found only the internal repository-owned `docs/traces/r2-closeout.toml` constant and its single binary open in `trace_loading.py`.

### Diff, index, and ignored-file review

The complete tracked diff and all seven untracked O2 files were inspected. No unrelated file, O1 analysis file, user prompt, conversation content, personal identity, invented approval record, private work data, arbitrary finding prose, or overstated claim was found.

```powershell
git diff --cached --stat
git diff --cached --check
```

Results: exit 0 with no output. The Git index is empty; nothing is staged.

```powershell
git status --ignored --short
git ls-files --others --exclude-standard
```

Results: exit 0. Ignored content was limited to `.venv`, Ruff and pytest caches, and Python bytecode caches. The untracked set contained only the fixed trace, three O2 source modules, and three focused O2 test modules. No generated trace output, model file, secret, local configuration, or runtime state was present.

These checks establish only strict parsing and deterministic internal consistency of one repository-declared R2 trace. They do not establish source-citation authenticity or freshness, external truth, human approval, evidence authenticity, runtime behavior, model quality, tool correctness, retrieval quality, production readiness, or general ontology correctness.

## O2 adversarial closeout audit — 2026-07-26

The audit began from published baseline `3285d4410111f512068b33d9581ba97bc7690bd2`, which matched local `HEAD`, `main`, and `origin/main`. It inspected the complete tracked O2 diff, all seven untracked O2 files, the Git index, ignored content, the fixed fixture, contracts, loader, validator, tests, authority documents, architecture documents, CLI stage, and repository verifier. O3 was not started, and no change was staged, committed, or pushed.

The audit corrected identifier-specific authority behavior, globally unified trace/record/requirement identifier ownership, rejected duplicate relationship targets, constrained evidence kind/provenance/epistemic combinations, derived repository-assertion findings from evidence, made finding and relationship order explicit and complete, required confirmed explicit-human authority for an approval gate, and rejected `not_required` as publication-commit authorization. It also added a fully complete differently identified synthetic trace, complete relationship probes, approval/status forgery probes, result-corruption probes, TOML boundary probes, and four-process complete/incomplete determinism checks.

The repository-checkout limitation is now explicit: `docs/traces/r2-closeout.toml` is repository content rather than wheel package data. O2 supports a repository checkout or editable install and does not claim standalone installed-wheel fixture loading.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The repository-local Python 3.12.6 editable environment was refreshed. Existing Pydantic 2.13.4, pytest 8.4.2, and Ruff 0.15.22 satisfied the declared dependencies. No AI runtime, AI SDK, model, or additional dependency was installed or invoked.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, 22 Python files were already formatted, pytest collected and passed 452 tests, the CLI reported `O2: R2 evidence-trace validation pilot`, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Results: all commands exited 0. Ruff reported `All checks passed!`; formatting reported `22 files already formatted`; all 452 tests passed under Python 3.12.6 and pytest 8.4.2; the CLI printed:

```text
Project: Local AI Guild
Stage: O2: R2 evidence-trace validation pilot
```

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_trace_contracts.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_trace_loading.py -q
.\.venv\Scripts\python.exe -m pytest tests/test_trace_validation.py -q
```

Results: exit 0. The focused suites passed 94, 22, and 73 tests respectively. They cover all ten exact record types, global durable-ID ownership, all supported relationship fields, reciprocal Decision/Artifact links, evidence/status rules, authority and approval forgery, result binding, complete and incomplete traces, fixed-loader rejection and redaction, and deterministic ordering.

The explicit semantic probes returned:

```text
official complete=False errors=1 warnings=0 infos=3
complete_synthetic complete=True errors=0 warnings=0 infos=3
invalid_semantic complete=False errors=1 warnings=0 infos=3
```

The official error remained only `missing_approval_evidence`. The complete synthetic trace retained only the three informational limitations. The deliberately invalid trace used a confirmed security-policy authority in place of explicit human authority and produced `unsupported_authority_claim`. Four repeated same-process and four repeated separate-process validations of both incomplete and complete traces were byte-identical.

TOML boundary tests confirmed rejection of parseable datetime, date, time, float, Boolean-in-integer, nested unexpected table, duplicate array-of-table semantic record, empty required array, mixed array, oversized integer, escaped Unicode control, unknown field, and wrong discriminator values. Missing, unreadable, invalid-TOML, and invalid-contract failures remained bounded and excluded source values, parser text, and machine paths.

Dependency inspection reported runtime dependencies `['pydantic>=2,<3']` and development dependencies `['pytest>=8.3,<9', 'ruff>=0.9,<1']`. The parser-bypass scan found no production O2 use of unchecked construction, unchecked copy updates, coercive parser helpers, or general raw-data model validation. The `object` annotations found in production are confined to strict runtime narrowing at the TOML boundary, exact-type consistency checks, and internal registry construction; no `Any` or arbitrary-value model field exists.

The prohibited-surface scan found only Git vocabulary used by the typed Git locator/Commit contract and three intentional `re.compile()` syntax patterns. Filesystem inspection found only the internal fixed path constant and its single binary read. No subprocess, shell, Git invocation, network client, dynamic import, code execution, logging, database, persistence, graph, retrieval, model, cloud, environment lookup, directory discovery, arbitrary-path parameter, executor, or approval workflow exists in production O2 source.

Credential-pattern, private-address, and personal-machine-path scans found no matches. Synthetic `PRIVATE`/`MARKER` values occur only in focused rejection/redaction tests and are asserted absent from errors and serialized results. `git check-ignore` confirmed repository-local environments and caches, real local configuration, `.env` and secret/credential files, model/runtime files, and generated trace, evidence, and benchmark artifacts remain ignored.

```powershell
git diff --check
git diff --cached --stat
git diff --cached --check
git status --short --branch
```

Results: all commands exited 0. Diff checks emitted no errors, the index remained empty, and `main` still matched `origin/main` at `3285d4410111f512068b33d9581ba97bc7690bd2`. All O2 changes remained unstaged, uncommitted, and unpushed.

The official trace remains contract-valid but intentionally incomplete. Its missing repository approval record does not prove that approval failed or did not occur. The audit establishes deterministic internal trace consistency and bounded failure behavior only; it does not dynamically resolve citations, authenticate evidence or humans, establish external truth, prove approval or correctness from Git history, validate wheel-installed fixture loading, or add a repository progression gate.

## R4A verification — 2026-07-26

All commands ran from `C:\dev\source\Repos\local-ai-guild` against accepted published baseline `a79d8103ea7d2a13ac808ccf046efdf55b767d2b`, which matched `HEAD`, `main`, and `origin/main` before R4A. The baseline working tree was clean.

R4A changed documentation only. It defined the portable Council/runtime authority boundary, objective runtime requirements, knowledge-promotion policy, and a future OpenClaw reference-runtime POC design. OpenClaw remained a candidate reference runtime; no runtime, model, adapter, interface, source code, configuration, ADR, credential, workspace, session, skill, or execution path was added.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The existing repository-local Python 3.12.6 editable environment was refreshed. Pydantic 2.13.4 remained the sole runtime dependency; pytest 8.4.2 and Ruff 0.15.22 remained development dependencies. No OpenClaw component, model runtime, AI SDK, or additional dependency was installed or invoked.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, 22 Python files were already formatted, all 452 tests passed, the CLI reported `O2: R2 evidence-trace validation pilot`, and repository verification passed.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
```

Result: exit 0, `All checks passed!`

```powershell
.\.venv\Scripts\python.exe -m ruff format --check .
```

Result: exit 0, `22 files already formatted`.

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result: exit 0. Pytest collected and passed 452 tests under Python 3.12.6 and pytest 8.4.2.

```powershell
.\.venv\Scripts\python.exe -m local_ai_guild status
```

Result: exit 0.

```text
Project: Local AI Guild
Stage: O2: R2 evidence-trace validation pilot
```

```powershell
git diff --check
git status --short --branch
```

Results: exit 0. The diff check produced no output. `main` remained at `a79d8103ea7d2a13ac808ccf046efdf55b767d2b`, matching `origin/main`; all R4A changes remained unstaged, uncommitted, and unpushed.

The complete tracked diff and four untracked R4A documents were inspected. A path audit confirmed that every changed or untracked path was Markdown documentation; `src/`, `tests/`, `scripts/`, `config/`, and `pyproject.toml` were unchanged. Searches found no OpenClaw reference in source, tests, scripts, configuration, or project metadata; no affirmative claim that OpenClaw is selected, approved, or adopted; no O3 implementation reference; and no runtime-selection ADR.

Content checks confirmed all required runtime-neutral Council concepts, all eight conceptual adapter operations, all fourteen objective runtime requirements, all six adoption gates, the ten-phase decision experiment, the requested isolation recommendations, and the six required knowledge-promotion conditions are present. Council authority remains outside runtime identifiers, sessions, memory, configuration, and event records.

These checks establish documentation consistency and preservation of the existing deterministic implementation only. They do not establish OpenClaw capability, security, compatibility, license suitability, operational value, model quality, runtime behavior, or readiness to begin R4B.

## O3 verification — 2026-07-26

All commands ran from `C:\dev\source\Repos\local-ai-guild` against published baseline
`c68632b27802924b94e135f61ed153a4dd6c4485`, which matched `HEAD`, `main`, and
`origin/main`. The starting working tree and index were clean. O3 used only public
synthetic data and left all changes unstaged, uncommitted, and unpushed.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The editable package was refreshed in the repository-local Python
3.12.6 environment. Pydantic 2.13.4 remained the sole runtime dependency; pytest
8.4.2 and Ruff 0.15.22 remained development dependencies. No AI runtime, model SDK,
OpenClaw component, or new dependency was installed or invoked.

```powershell
.\scripts\verify-repository.ps1
```

Final result: exit 0. Ruff passed, 24 Python files were already formatted, pytest
collected and passed 468 tests in 20.72 seconds, the CLI reported the O3 stage, and the
script reported `Repository verification passed.`

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m local_ai_guild status
git diff --check
git status --short --branch
```

Results: every command exited 0. Ruff reported `All checks passed!`; formatting
reported `24 files already formatted`; pytest passed all 468 tests in 42.02 seconds;
the CLI printed:

```text
Project: Local AI Guild
Stage: O3: synthetic handoff completeness experiment
```

The diff check produced no output. Git reported `main...origin/main`, twelve modified
or untracked O3 paths, and no staged path.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_o3_experiment.py -q
```

Final focused result: exit 0, 16 tests passed. The tests cover the zero-argument fixed
loader, exact contract validity, semantic rather than parser failures, manual-review
immutability and bounds, matched/manual-only/validator-only partitions, deterministic
ordering, differently identified trace behavior, absence of O3 hardcoding in the
validator, direct construction and unsafe-corruption rejection, caller-created
lookalikes, reassignment of the public manual tuple, same- and separate-process
serialization, and rejected-marker redaction.

During result-binding hardening, one focused Ruff check exited 1 for an unsorted import
block in `tests/test_o3_experiment.py`. The import order was corrected; the final
focused and repository-wide Ruff checks exited 0.

```powershell
$code = 'from local_ai_guild.o3_experiment import run_o3_handoff_experiment; print(run_o3_handoff_experiment().model_dump_json())'
$sameProcess = & .\.venv\Scripts\python.exe -c "from local_ai_guild.o3_experiment import run_o3_handoff_experiment; a=run_o3_handoff_experiment().model_dump_json(); b=run_o3_handoff_experiment().model_dump_json(); print(a == b); print(a)"
$sameProcess
$first = & .\.venv\Scripts\python.exe -c $code
$second = & .\.venv\Scripts\python.exe -c $code
"SEPARATE_PROCESS_EQUAL=$($first -ceq $second)"
"FIRST=$first"
"SECOND=$second"
```

Results: exit 0. The same-process comparison printed `True`; the two separate-process
serializations were byte-for-byte equal. The official result contained 5 manual
findings, 7 validator findings, 4 matches, 1 manual-only finding, and 3 validator-only
findings. It contained no raw TOML, packet prose, paths, parser errors, or free-form
messages.

```powershell
.\.venv\Scripts\python.exe -m pip show local-ai-guild pydantic pytest ruff
```

Result: exit 0. The editable project required only Pydantic. Installed versions were
Pydantic 2.13.4, pytest 8.4.2, and Ruff 0.15.22. `pyproject.toml` was unchanged.

```powershell
rg -n --hidden -g '!.git/**' -g '!.venv/**' -e 'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(?i)(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*["''][^"'']{8,}["'']' .
rg --pcre2 -n --hidden -g '!.git/**' -g '!.venv/**' -e '(?<![0-9])10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}(?![0-9])|(?<![0-9])192\.168\.(?:[0-9]{1,3}\.)[0-9]{1,3}(?![0-9])|(?<![0-9])172\.(?:1[6-9]|2[0-9]|3[01])\.(?:[0-9]{1,3}\.)[0-9]{1,3}(?![0-9])|(?i:https?://[^/\s]*(?:\.local|\.internal)(?:[/:\s]|$))' .
rg -n --hidden -g '!.git/**' -g '!.venv/**' -e '(?i)C:\\Users\\|\\\\[A-Za-z0-9._-]+\\|(?i)(hostname|internal endpoint|connection string)\s*[:=]\s*\S+' .
rg -n -e 'subprocess|os\.system|requests|httpx|urllib|socket|importlib|__import__|\beval\s*\(|\bexec\s*\(|logging|sqlite|sqlalchemy|pydantic_ai|\bopenai\b|anthropic|boto|azure|write_text|write_bytes|mkdir|unlink|remove\s*\(|rename\s*\(|replace\s*\(' src/local_ai_guild/o3_experiment.py src/local_ai_guild/trace_loading.py
```

Credential-pattern and private-address scans covered all repository content while
excluding `.git` and `.venv`; both produced no matches. The first private-address scan
used lookaround unsupported by ripgrep's default regex engine and exited 2; rerunning the
same expression with `rg --pcre2` exited 1 with no matches. A machine-specific scan
returned only three intentional synthetic UNC-path rejection cases in R1 tests. No
credential-like value, private address, user-profile path, hostname, internal endpoint,
or connection string was found in publishable O3 content.

A prohibited-surface scan of `o3_experiment.py` and the shared fixed loader found no
subprocess, network, dynamic import, evaluation, logging, database, model SDK, cloud
SDK, or filesystem mutation API. The one new I/O operation is the authorized fixed O3
TOML read through the existing bounded loader.

```powershell
git diff --cached --name-status
git ls-files --others --exclude-standard
git check-ignore -v .venv\probe.py .pytest_cache\probe .ruff_cache\probe config\local.yaml config\local\providers.yaml artifacts\traces\probe.toml artifacts\evidence\probe.json artifacts\benchmark-results\probe.json models\probe.gguf runtime-state\probe.json .env secrets.local.json probe.key datasets\probe.json logs\probe.log crash-dumps\probe.dmp
git diff --stat
git diff --name-status
git diff -- DECISIONS.md NEXT_WORK_PACKET.md OPEN_QUESTIONS.md PROJECT_STATE.md README.md ROADMAP.md src/local_ai_guild/cli.py src/local_ai_guild/trace_loading.py
Get-Content docs/experiments/O3_SYNTHETIC_HANDOFF.md
Get-Content docs/traces/o3-synthetic-handoff.toml
Get-Content src/local_ai_guild/o3_experiment.py
Get-Content tests/test_o3_experiment.py
```

The Git index was empty. `git ls-files --others --exclude-standard` listed exactly the
four new O3 files. `git check-ignore -v` confirmed that `.venv`, pytest and Ruff
caches, local configuration, generated traces, evidence, benchmark output, model
files, runtime state, environment files, secret files, keys, local datasets, logs, and
crash dumps remain ignored.

The complete tracked diff and all four untracked files were inspected. O3 changes only
the fixed loader, adds the bounded comparison module and focused tests, changes the
harmless CLI stage string, adds the synthetic packet and trace, and updates required
authority documents. The existing validator, O2 fixture, contracts, dependencies,
scripts, configuration, runtime planning documents, and R4A architecture documents are
unchanged.

These checks establish only the deterministic structural behavior of the public
synthetic fixture and comparison. Manual findings are repository-authored assertions.
Deterministic findings do not prove external truth, approval authenticity, artifact
existence, human identity, or general ontology correctness. O3 used no model, runtime,
OpenClaw component, routing, retrieval, persistence, mutation, or execution.

## Portable Council contracts checkpoint — 2026-07-26

All commands ran from `C:\dev\source\Repos\local-ai-guild` against published baseline
`a3e6facaf77153486236ebea5b4a383d216e7bcf`, which matched `HEAD`, `main`, and
`origin/main`. The starting working tree and index were clean. The checkpoint used one
public synthetic in-memory proceeding and left every change unstaged, uncommitted, and
unpushed.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The editable package was refreshed in the repository-local Python
3.12.6 environment. Pydantic 2.13.4 remained the sole runtime dependency; pytest
8.4.2 and Ruff 0.15.22 remained development dependencies. No dependency, model SDK,
AI runtime, OpenClaw component, or machine-wide setting was added.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, 28 Python files were already formatted, pytest collected
and passed 499 tests in 43.74 seconds, the CLI reported the portable Council contracts
checkpoint stage, and the script reported `Repository verification passed.`

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m local_ai_guild status
git diff --check
git status --short --branch
```

Results: every command exited 0. Ruff reported `All checks passed!`; formatting
reported `28 files already formatted`; pytest passed all 499 tests in 43.48 seconds;
the CLI printed:

```text
Project: Local AI Guild
Stage: Portable Council contracts checkpoint
```

The diff check produced no output. Git reported `main...origin/main`, modified
authority, architecture, experiment, and CLI documents, four untracked implementation
and test files, and no staged path.

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_council_contracts.py -q
```

Final focused result: exit 0, 31 tests passed in 5.45 seconds. Coverage includes all ten
strict/frozen/extra-forbid contracts, identifier namespaces, runtime-neutral fields,
frozen-position integrity, canonical relationship direction, exact cross-contract
references, human approval separation, dissent, promotion requirements, runtime-event
correlation, issue ordering, direct and unsafe corruption, nested dissent corruption,
same-process serialization, separate-process serialization, and absence of runtime
adapter or OpenClaw surfaces.

During implementation, the first focused Ruff pass exited 1 for two line-length
findings and one unused import, and formatting identified two files. They were
corrected mechanically. The first focused test run then passed 29 tests and failed two
test-quality assertions: a one-issue result could not demonstrate reordering, and a
broad `requests` substring matched `approval_requests`. While correcting them, one
intermediate run exposed an unmatched test parenthesis. The fixture was strengthened,
the scan assertion was narrowed to import syntax, the syntax was corrected, and every
final focused and repository-wide check passed.

```powershell
$code='from local_ai_guild.council_fixture import synthetic_council_proceeding; from local_ai_guild.council_validation import validate_council_proceeding; print(validate_council_proceeding(synthetic_council_proceeding()).model_dump_json())'
.\.venv\Scripts\python.exe -m pytest tests\test_council_contracts.py -q
$same=& .\.venv\Scripts\python.exe -c "from local_ai_guild.council_fixture import synthetic_council_proceeding; from local_ai_guild.council_validation import validate_council_proceeding; a=validate_council_proceeding(synthetic_council_proceeding()).model_dump_json(); b=validate_council_proceeding(synthetic_council_proceeding()).model_dump_json(); print(a == b); print(a)"
$same
$first=& .\.venv\Scripts\python.exe -c $code
$second=& .\.venv\Scripts\python.exe -c $code
"SEPARATE_PROCESS_EQUAL=$($first -ceq $second)"
"FIRST=$first"
"SECOND=$second"
```

Results: exit 0. The same-process comparison printed `True`; the two separate-process
serializations were byte-for-byte equal. The official synthetic proceeding contained
19 Council records and returned `valid: true`, `issue_count: 0`, and no issues.

```powershell
.\.venv\Scripts\python.exe -m pip show local-ai-guild pydantic pytest ruff
git diff -- pyproject.toml scripts config
```

Results: exit 0. The editable project required only Pydantic. Installed versions were
Pydantic 2.13.4, pytest 8.4.2, and Ruff 0.15.22. Dependencies, scripts, and
configuration were unchanged.

```powershell
rg -n -e 'import (subprocess|requests|httpx|urllib|socket|importlib|logging|sqlite|sqlalchemy|pydantic_ai|openai|anthropic|boto|azure|tomllib|pathlib)|from (subprocess|requests|httpx|urllib|socket|pathlib)|os\.system|__import__|\beval\s*\(|\bexec\s*\(|\.open\s*\(|write_text\s*\(|write_bytes\s*\(|mkdir\s*\(|unlink\s*\(' src\local_ai_guild\council_contracts.py src\local_ai_guild\council_fixture.py src\local_ai_guild\council_validation.py
rg -n -i -e 'openclaw|runtime[_ -]?agent[_ -]?id|session[_ -]?id|model[_ -]?name|workspace[_ -]?path|provider[_ -]?(configuration|config)' src\local_ai_guild\council_contracts.py src\local_ai_guild\council_fixture.py src\local_ai_guild\council_validation.py
rg -n --hidden -g '!.git/**' -g '!.venv/**' -e 'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(?i)(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*["''][^"'']{8,}["'']' .
rg --pcre2 -n --hidden -g '!.git/**' -g '!.venv/**' -e '(?<![0-9])10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}(?![0-9])|(?<![0-9])192\.168\.(?:[0-9]{1,3}\.)[0-9]{1,3}(?![0-9])|(?<![0-9])172\.(?:1[6-9]|2[0-9]|3[01])\.(?:[0-9]{1,3}\.)[0-9]{1,3}(?![0-9])|(?i:https?://[^/\s]*(?:\.local|\.internal)(?:[/:\s]|$))' .
rg -n --hidden -g '!.git/**' -g '!.venv/**' -e '(?i)C:\\Users\\|\\\\[A-Za-z0-9._-]+\\|(?i)(hostname|internal endpoint|connection string)\s*[:=]\s*\S+' .
```

Results: the prohibited-surface, runtime-specific-field, credential, and private-address
scans returned no matches. The first broad prohibited-surface expression matched only
the legitimate `approval_requests` field; the refined import and call syntax scan above
returned no matches. The machine-specific scan returned only documented scan text and
synthetic path-rejection fixtures. No publishable checkpoint content contained a
credential-like value, private address, personal path, hostname, internal endpoint, or
connection string.

```powershell
git diff --cached --name-status
git ls-files --others --exclude-standard
git diff --stat
git diff --name-status
git diff -- README.md PROJECT_STATE.md ROADMAP.md DECISIONS.md OPEN_QUESTIONS.md NEXT_WORK_PACKET.md src/local_ai_guild/cli.py
git diff -- docs/architecture/COMPONENT_MODEL.md docs/architecture/COUNCIL_RUNTIME_BOUNDARY.md docs/architecture/COUNCIL_RUNTIME_REQUIREMENTS.md docs/architecture/EXECUTION_FLOW.md docs/architecture/KNOWLEDGE_PROMOTION_POLICY.md docs/experiments/OPENCLAW_REFERENCE_RUNTIME_POC.md
Get-Content src/local_ai_guild/council_contracts.py
Get-Content src/local_ai_guild/council_fixture.py
Get-Content src/local_ai_guild/council_validation.py
Get-Content tests/test_council_contracts.py
```

The Git index was empty. The untracked set contained exactly the three Council source
modules and focused test file. The complete tracked diff and every untracked file were
inspected. The checkpoint changed no dependency, script, configuration, existing O2/O3
contract, trace, loader, validator, fixture, or test.

These checks establish only strict portable contract behavior and deterministic
in-memory consistency for the public synthetic proceeding. They do not establish a
completed Council, external truth, approval authenticity, knowledge mutation,
persistence, runtime capability, runtime isolation, OpenClaw suitability, model
quality, or readiness to begin R4B.

## R4B documentation-only entry-gate review — 2026-07-27

All commands ran from `C:\dev\source\Repos\local-ai-guild` against published baseline
`9d0e2a225f4b9c41ac4f41a8ae125c4e9ad98e11`, which matched `HEAD`, `main`, and
`origin/main`. The starting worktree and index were clean. No external web research,
runtime installation, runtime execution, model configuration, provider access, or
OpenClaw invocation occurred.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The editable package was refreshed in the repository-local Python
3.12.6 environment. Pydantic 2.13.4 remained the sole runtime dependency; pytest
8.4.2 and Ruff 0.15.22 remained development dependencies. No new dependency or
machine-wide setting was added.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff passed, 28 Python files were already formatted, pytest collected
and passed 499 tests in 15.15 seconds, the CLI reported the portable Council contracts
checkpoint stage, and the script reported `Repository verification passed.`

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m local_ai_guild status
git diff --check
git status --short --branch
```

Results: every command exited 0. Ruff reported `All checks passed!`; formatting
reported `28 files already formatted`; pytest passed all 499 tests in 16.43 seconds;
the CLI printed:

```text
Project: Local AI Guild
Stage: Portable Council contracts checkpoint
```

The diff check produced no output. Git reported `main...origin/main`, eight modified
Markdown files, one untracked Markdown review, and no staged path at that point.

The documentation audit required all six gate sections; all six evidence, limitation,
test, pass, and stop subsections; only the four approved classification strings; and
exactly one final recommendation. It found:

- Gates 1 and 5: `partially_supported`.
- Gate 2: `blocked_by_missing_prerequisite`.
- Gates 3, 4, and 6: `requires_r4b_experiment`.
- Recommendation: `ready_to_propose_bounded_r4b_packet`.

The recommendation permits only proposing a separate documentation and authorization
packet. It does not authorize R4B, installation, execution, runtime selection, or
adoption.

```powershell
git status --short
git diff --name-only
git diff --cached --name-only
git status --short docs/decisions
git diff -- src tests scripts config pyproject.toml
```

Results: every changed or untracked path was Markdown documentation. The Git index was
empty. Source, tests, scripts, configuration, dependencies, and `docs/decisions/`
were unchanged; no runtime-selection ADR was created.

Credential-pattern and private-network scans over all changed documentation returned no
matches. An actionable runtime-command scan returned only the README's negative statement
that no OpenClaw installation exists; no installation, download, configuration, or
execution command was added. The review contains no live credentials, private network
details, runtime configuration, external runtime capability claim, or affirmative
selection/adoption language.

These checks establish documentation consistency and repository-evidence traceability
only. They do not establish an eligible OpenClaw version, license suitability, runtime
capability, isolation, permission enforcement, event completeness, routing behavior,
cost attribution, teardown completeness, operational value, or adoption readiness.

Final structural inspection found all six gate sections, all required gate subsections,
all 18 prerequisite rows with one approved disposition each, every required stop
condition, and exactly one recommendation in
`docs/experiments/R4B_ENTRY_GATE_REVIEW.md`. The complete tracked diff and the new
384-line review were inspected.

Final `git diff --check` passed with no output. `git status --short --branch` reported
`main...origin/main`, nine modified Markdown files, one untracked Markdown file, and no
staged path. `git diff -- src tests scripts config pyproject.toml docs/decisions`
produced no output.

## Bounded R4B authorization-and-experiment-design packet — 2026-07-27

Before editing, the exact commit with subject
`docs: review R4B entry gates` was resolved as
`f49d6f26c712c451efc496b1f35f389422651c2e`. `HEAD`, `main`, and
`origin/main` all matched that commit; the worktree and index were clean.
`docs/experiments/R4B_ENTRY_GATE_REVIEW.md` was tracked and its sole recommendation was
`ready_to_propose_bounded_r4b_packet`.

Official-source read-only research identified OpenClaw `v2026.7.1`, released
2026-07-13 at immutable commit
`2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4`. The official release, commit,
`LICENSE`, `THIRD_PARTY_NOTICES.md`, `package.json`, `SECURITY.md`, and release
evidence were inspected through GitHub and official repository URLs. The core license
is MIT. Dependency, model, provider, intended-use, and legal approval remain human
review items. No candidate artifact was downloaded, and no package or release digest
was independently recalculated.

```powershell
.\scripts\bootstrap.ps1
```

Result: exit 0. The repository-local editable package was refreshed under Python
3.12.6. Pydantic 2.13.4 remained the sole runtime dependency; pytest 8.4.2 and Ruff
0.15.22 remained development dependencies. No OpenClaw, model, provider, or new project
dependency was installed.

```powershell
.\scripts\verify-repository.ps1
```

Result: exit 0. Ruff reported `All checks passed!`; formatting reported
`28 files already formatted`; pytest collected and passed 499 tests in 7.87 seconds;
the CLI reported:

```text
Project: Local AI Guild
Stage: Portable Council contracts checkpoint
```

The script ended with `Repository verification passed.`

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m local_ai_guild status
git diff --check
git status --short --branch
```

Results: every command exited 0. Ruff reported `All checks passed!`; formatting
reported `28 files already formatted`; the direct pytest run passed all 499 tests in
8.50 seconds; the CLI printed the same portable Council contracts checkpoint stage.
The final diff check produced no output. Git reported `main...origin/main`, nine
modified Markdown files, four untracked Markdown files, and no staged path.

The structural documentation audit found:

- exactly four new packet documents;
- authorization status `not_authorized` in every new document and one human
  `Decision: pending`;
- 21 unchecked authorization items and no checked item;
- one immutable candidate, one selected dedicated-WSL2 design, and no floating runtime
  version;
- 27 experiment-specific threat rows covering every required scenario and recording
  prevention, detection, stop, residual risk, and enforcement status;
- 24 proposed runbook phases, 25 required runtime-event kinds, and 20 deterministic
  external checks;
- identical OpenClaw and custom-dispatcher comparison dimensions;
- a complete removal, retained-evidence, residue, credential, failure, and closeout
  plan.

```powershell
git diff --cached --name-only
git ls-files --others --exclude-standard
git status --ignored --short
git status --short docs/decisions
git diff -- src tests scripts config pyproject.toml docs/decisions
```

Results: the Git index was empty. The untracked set contained exactly the four new
Markdown documents. Ignored state was limited to the repository-local `.venv`, Ruff and
pytest caches, and Python bytecode caches. Source, tests, scripts, configuration,
dependencies, CLI code, portable Council contracts, and `docs/decisions/` were
unchanged. No runtime-selection ADR was created.

The `.gitignore` inspection confirmed that virtual environments and caches; local
configuration and environment files; certificates, keys, credential and secret JSON;
logs, crash dumps, databases, local data; model files and runtime state; generated
evidence, traces, and benchmark results; and build output remain ignored. Tracked
example configuration and artifact directory placeholders remain allowed.

```powershell
rg -n --hidden -g '!.git/**' -g '!.venv/**' -e 'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(?i)(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*["''][^"'']{8,}["'']' .
rg --pcre2 -n --hidden -g '!.git/**' -g '!.venv/**' -e '(?<![0-9])10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}(?![0-9])|(?<![0-9])192\.168\.(?:[0-9]{1,3}\.)[0-9]{1,3}(?![0-9])|(?<![0-9])172\.(?:1[6-9]|2[0-9]|3[01])\.(?:[0-9]{1,3}\.)[0-9]{1,3}(?![0-9])|(?i:https?://[^/\s]*(?:\.local|\.internal)(?:[/:\s]|$))' .
rg -n --hidden -g '!.git/**' -g '!.venv/**' -e '(?i)C:\\Users\\|\\\\[A-Za-z0-9._-]+\\|(?i)(hostname|internal endpoint|connection string)\s*[:=]\s*\S+' .
```

Results: credential and private-address scans returned no matches. The machine-specific
scan matched only its own commands already recorded in this file and public synthetic
UNC/path-rejection fixtures in tests. No new packet document contained a user profile
path, hostname, internal endpoint, connection string, credential-like value, or private
address.

All external URLs in the new packet resolve under the official
`github.com/openclaw/openclaw` or `github.com/openclaw/releases` organizations. Claims
are labeled as observed official-source facts, repository design decisions, inferences,
or unresolved human-review questions. The complete tracked diff and all four untracked
documents were inspected.

These checks establish a coherent documentation-only authorization design and preserve
the existing deterministic repository behavior. They do not establish OpenClaw
capability, license approval, intended-use approval, dependency suitability, model
quality, isolation, permission enforcement, event completeness, routing, cost,
teardown, operational value, or adoption readiness. No OpenClaw or model download,
installation, configuration, invocation, provider connection, credential creation or
injection, WSL2/container/network/firewall change, proof-of-concept execution, or R4C
ADR occurred.

## Human R4B authorization-review preparation — 2026-07-27

The review began at published baseline
`c779ea815490ec14b9f6357729b46087235c03ba`, subject
`docs: finish R4B reference corrections`. Local `HEAD` and `origin/main` matched, the
worktree and index were clean, the bounded authorization package existed, authorization
was `not_authorized`, its human decision was `pending`, and every checklist item was
unchecked. Repository evidence confirmed that no OpenClaw runtime or R4B experiment had
executed.

The complete durable Markdown set was audited for publication identity and status.
Twenty-eight Markdown files contained 21 unique 40-character SHA values and no
backtick-delimited abbreviated SHA. Every Local AI Guild SHA resolved to a commit in
this repository. The OpenClaw SHA
`2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4` remained explicitly namespaced as an
external `openclaw/openclaw` commit. The new publication index records the detailed
ledger, keeps `c779ea815490ec14b9f6357729b46087235c03ba` as the current published
baseline, and keeps `6fe01f7dd0d756a757bea8213803f0e23c42bfab` as the current
executable checkpoint. The known README error was corrected so
`2984cecbf52bdf356d84c559bb49db13dc8bab9c` describes the bounded authorization
package rather than the earlier entry-gate review. Historical verification references
were preserved.

Official-source static review reconfirmed OpenClaw `v2026.7.1`, package version
`2026.7.1`, external commit `2d2ddc43d0dcf71f31283d780f9fe9ff4cc04fe4`,
release date 2026-07-13, npm integrity, MIT core license, third-party notice, security
model, Node ranges, pnpm source lock, and npm shrinkwrap. The root metadata declares 56
direct runtime dependencies, one optional dependency, no `bundledDependencies`, and 31
development dependencies. The bounded shrinkwrap surface has no missing license field;
the exception-focused review names MPL-2.0, dual-license, combined-license, Unlicense,
BlueOak, internal-workspace, Node, native/install-script, and container considerations.
This is static technical evidence, not legal approval.

Read-only local inventory found one complete pinned Ollama Qwen2.5-Coder 7B
manifest/blob set and one LM Studio Q5_K_M GGUF file. `ollama list`, a command explicitly
permitted by the packet, returned no model row but auto-started Ollama background
processes; the newly started processes were immediately terminated. `lms ls --json`
timed out and its remaining CLI process was terminated. No model was loaded, invoked,
downloaded, converted, or quantized, and no Ollama, LMS, LM Studio, or OpenClaw process
remained. Because file/manifest presence did not yield one exact runtime-visible route,
model selection remains unresolved and the advisory recommendation is
`recommend_defer`.

The required commands were then run from the repository root:

```powershell
.\scripts\bootstrap.ps1
.\scripts\verify-repository.ps1
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m local_ai_guild status
git diff --check
git status --short --branch
```

Results:

- `bootstrap.ps1`: exit 0; repository-local Python 3.12.6 environment refreshed.
  Pydantic 2.13.4, pytest 8.4.2, and Ruff 0.15.22 satisfied the existing declarations.
- `verify-repository.ps1`: exit 0; Ruff passed, 28 Python files were already formatted,
  all 499 tests passed in 7.18 seconds, and CLI status passed.
- standalone Ruff check: exit 0, `All checks passed!`.
- standalone Ruff format check: exit 0, `28 files already formatted`.
- standalone pytest: exit 0, 499 tests passed in 7.18 seconds.
- CLI status: exit 0; project `Local AI Guild`, stage
  `Portable Council contracts checkpoint`.
- `git diff --check`: exit 0 with no output.
- `git status --short --branch`: exit 0; `main` still matched `origin/main`; all packet
  changes were unstaged and the index was empty.

The changed and untracked path inventory contained Markdown files only:

```text
DECISIONS.md
NEXT_WORK_PACKET.md
OPEN_QUESTIONS.md
PROJECT_STATE.md
README.md
ROADMAP.md
VERIFICATION.md
docs/PUBLICATION_INDEX.md
docs/experiments/R4B_AUTHORIZATION_PACKET.md
docs/experiments/R4B_DATA_BUNDLE_MANIFEST.md
docs/experiments/R4B_HUMAN_AUTHORIZATION_REVIEW.md
docs/research/R4B_OPENCLAW_LICENSE_REVIEW.md
```

No source, test, script, dependency, configuration, portable-contract, or CLI file
changed. The complete tracked diff and all four new documents were inspected.

Credential-prefix, credential-assignment, credential-bearing URL, private-key, email,
private IPv4, and user-profile-path scans of non-ignored repository content returned no
matches. `.gitignore` probes confirmed virtual environments, Python and tool caches,
local configuration, environment files, credentials/secrets, generated traces,
evidence, benchmark output, logs, crash dumps, datasets, local data, model files,
Ollama state, and runtime state remain ignored.

Authorization remains `not_authorized`, both decision fields remain `pending`, and no
authoritative checklist item is checked. OpenClaw remains an external candidate rather
than selected or adopted. No candidate download, installation, configuration, or
execution; model download or invocation; provider connection; credential creation or
injection; WSL2, VM, container, network, firewall, or other host-control change; proof
of concept; or R4C ADR occurred. The local inventory process auto-start described above
is the sole observed command side effect and was reversed immediately.

## R4B local-model route qualification — 2026-07-28

### Published prerequisite and authority state

The packet began from a clean worktree and empty index. Local `HEAD` and `origin/main`
matched at:

```text
9d1f1935560c010f36a27be85483924a2c52bffd
docs: prepare human R4B authorization review
```

`docs/PUBLICATION_INDEX.md` and the human-review packet existed. The review
recommendation was `recommend_defer`, authorization was `not_authorized`, both human
decision fields were `pending`, every authorization item was unchecked, and project
state recorded that no R4B runtime experiment had executed.

The publication ledger now records `9d1f1935560c010f36a27be85483924a2c52bffd`
as the published advisory-review checkpoint and current published baseline.
`c779ea815490ec14b9f6357729b46087235c03ba` remains the historical final
publication-reference correction before that review, and
`2984cecbf52bdf356d84c559bb49db13dc8bab9c` remains the bounded authorization-package
checkpoint. The current executable checkpoint remains
`6fe01f7dd0d756a757bea8213803f0e23c42bfab`.

### Read-only process and artifact inspection

Preflight and postflight used `Get-Process` and a bounded `Get-CimInstance
Win32_Process` query. Neither inventory found an Ollama, LM Studio, llama.cpp, OpenClaw,
or clearly attributable Node process. No preexisting process was modified, and no new
relevant process appeared.

No Ollama, LM Studio, llama.cpp, or other model-runtime CLI was executed. Inspection
used bounded `Test-Path`, `Get-ChildItem`, `Get-Item`, `Get-Content`, `Get-FileHash`,
PowerShell JSON parsing, and official-source HTTP metadata reads only.

Direct local hashing established:

```text
Ollama 7B manifest:
dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364

Ollama 7B model layer:
60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463

Ollama 7B config:
d9bb33f2786931fea42f50936a2424818aa2f14500638af2f01861eb2c8fb446

Ollama/Qwen license:
832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e

LM Studio Q5_K_M GGUF:
b0f8a344452d5462193991fd7cf2bffdbee1a05fccfe98aa25a6ed91a56624a2
```

The local Ollama manifest body matched the official Ollama registry manifest SHA-256
and every declared config/layer digest and size. The license layer matched the official
Qwen Apache-2.0 license bytes. The local LM Studio GGUF matched the exact Hugging Face
LFS SHA-256 and size at conversion revision
`10ba8b9be9729feb1d3c476d014c861dbfc01177`.

The 7B and floating `latest` Ollama manifests were complete and byte-identical. The 14B
manifest lacked its config and model; the Qwen3 30B manifest lacked every referenced
blob. The incomplete artifacts were excluded. No model file or manifest was written or
modified.

### Qualification result

Route `r4b-local-qwen25-coder-7b-q4km-v1` is
`conditionally_qualified_for_benchmark`. Its immutable identity, official distribution
match, upstream Qwen lineage, Apache-2.0 evidence, and static fit are sufficient for a
later bounded public/synthetic capability benchmark, subject to human acceptance.

The proposed per-invocation limit is reduced from 24,000/4,000 to 8,192 total context
and 2,048 output tokens. This is an explicit proposed amendment, not silent
authorization. Runtime availability, CPU/GPU behavior, AMD acceleration, memory use,
throughput, latency, context reliability, instruction following, schema compliance,
evidence use, adversarial competence, audit competence, quality, and stability remain
untested.

The two complete files are quantizations of the same Qwen model family. Separate
sessions can support procedural independence, but the route provides no model diversity
and retains correlated-failure risk.

### Required repository verification

Commands run from the repository root:

```powershell
.\scripts\bootstrap.ps1
.\scripts\verify-repository.ps1
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m local_ai_guild status
git diff --check
git status --short --branch
```

Results:

- `bootstrap.ps1`: exit 0; repository-local Python 3.12.6 editable environment
  refreshed; every declared dependency was already satisfied and no new dependency was
  added.
- `verify-repository.ps1`: exit 0; Ruff passed, 28 Python files were already formatted,
  499 tests passed in 36.38 seconds, and CLI status passed.
- final post-documentation `verify-repository.ps1` recheck: exit 0; 499 tests passed in
  37.92 seconds and CLI status remained unchanged.
- standalone Ruff check: exit 0, `All checks passed!`.
- standalone Ruff format check: exit 0, `28 files already formatted`.
- standalone pytest: exit 0, 499 tests passed in 35.61 seconds.
- CLI status: exit 0; stage remained `Portable Council contracts checkpoint`.
- `git diff --check`: exit 0 with no output.
- `git status --short --branch`: exit 0; `main` remained at the published prerequisite,
  matching `origin/main`; all packet changes remained unstaged and the index was empty.

### Repository, publication, and sensitive-data audit

The complete diff is Markdown documentation only. No source, test, script, dependency,
configuration, portable-contract, CLI, runtime, manifest, or model file changed.

The durable Markdown audit covered 31 files, 24 unique 40-character SHA values, and no
abbreviated SHA. Every Local AI Guild SHA resolved to a repository commit. The three
external revisions were explicitly namespaced as OpenClaw or Hugging Face sources.
Model SHA-256 values remain 64-character artifact digests and are never described as
repository commits. Current-baseline and executable-checkpoint statements were
consistent, and no transient working-tree or future-publication claim was added.

The five frozen route digests were consistent across the inventory, license review,
qualification, human review, and next packet. Durable packet documents contained no
full user-profile or UNC path; public-safe root aliases were used.

Credential-prefix, credential-assignment, credential-bearing URL, private-key, and
private-IPv4 scans returned no matches. Authorization remained `not_authorized`, human
decision remained `pending`, and no checklist item was checked.

No model runtime CLI, model load, inference, download, pull, import, conversion,
quantization, training, configuration change, server start, provider connection,
credential action, OpenClaw action, WSL2/VM/container/network/firewall change, or R4B
runtime experiment occurred.
