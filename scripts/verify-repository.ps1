[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepositoryRoot = Split-Path -Parent $PSScriptRoot

function Invoke-CheckedPython {
    param(
        [Parameter(Mandatory)]
        [string]$Python,
        [Parameter(ValueFromRemainingArguments)]
        [string[]]$Arguments
    )

    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code ${LASTEXITCODE}: $($Arguments -join ' ')"
    }
}

$ExpectedPaths = @(
    "README.md", "AGENTS.md", "PROJECT_STATE.md", "VISION.md", "ROADMAP.md",
    "NEXT_WORK_PACKET.md", "OPEN_QUESTIONS.md", "DECISIONS.md", "VERIFICATION.md",
    "SECURITY.md", ".gitignore", ".python-version", "pyproject.toml",
    "config/models.example.yaml", "config/providers.example.yaml",
    "config/routing.example.yaml", "config/tools.example.yaml",
    "docs/architecture/SYSTEM_CONTEXT.md", "docs/architecture/COMPONENT_MODEL.md",
    "docs/architecture/SECURITY_BOUNDARIES.md", "docs/architecture/EXECUTION_FLOW.md",
    "docs/decisions/.gitkeep", "docs/experiments/.gitkeep", "docs/verification/.gitkeep",
    "evals/.gitkeep", "artifacts/evidence/.gitkeep", "artifacts/traces/.gitkeep",
    "artifacts/benchmark-results/.gitkeep",
    "scripts/bootstrap.ps1", "scripts/verify-repository.ps1", "scripts/show-environment.ps1",
    "src/local_ai_guild/__init__.py", "src/local_ai_guild/__main__.py",
    "src/local_ai_guild/cli.py", "src/local_ai_guild/contracts.py",
    "src/local_ai_guild/mock_router.py", "src/local_ai_guild/validation.py",
    "tests/test_cli.py", "tests/test_contracts.py", "tests/test_mock_router.py"
)

$MissingPaths = @(
    foreach ($RelativePath in $ExpectedPaths) {
        if (-not (Test-Path -LiteralPath (Join-Path $RepositoryRoot $RelativePath))) {
            $RelativePath
        }
    }
)

if ($MissingPaths.Count -gt 0) {
    throw "Missing expected repository paths: $($MissingPaths -join ', ')"
}

$VirtualPython = Join-Path $RepositoryRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $VirtualPython -PathType Leaf)) {
    throw "Repository virtual environment not found. Run scripts/bootstrap.ps1 first."
}

Push-Location $RepositoryRoot
try {
    Invoke-CheckedPython $VirtualPython -m ruff check .
    Invoke-CheckedPython $VirtualPython -m ruff format --check .
    Invoke-CheckedPython $VirtualPython -m pytest
    Invoke-CheckedPython $VirtualPython -m local_ai_guild status
}
finally {
    Pop-Location
}

Write-Output "Repository verification passed."
