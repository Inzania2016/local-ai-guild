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
