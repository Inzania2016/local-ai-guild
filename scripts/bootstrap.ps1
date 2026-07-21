[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepositoryRoot = Split-Path -Parent $PSScriptRoot
$VirtualEnvironment = Join-Path $RepositoryRoot ".venv"
$VirtualPython = Join-Path $VirtualEnvironment "Scripts\python.exe"

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory)]
        [string]$Executable,
        [Parameter(ValueFromRemainingArguments)]
        [string[]]$Arguments
    )

    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Executable $($Arguments -join ' ')"
    }
}

if (-not (Test-Path -LiteralPath $VirtualPython -PathType Leaf)) {
    $Launcher = Get-Command py -ErrorAction SilentlyContinue
    if ($null -eq $Launcher) {
        throw "Python launcher 'py' was not found. Install Python 3.12 explicitly before bootstrapping."
    }

    Invoke-CheckedCommand $Launcher.Source -3.12 -c "import sys; assert sys.version_info[:2] == (3, 12)"
    Invoke-CheckedCommand $Launcher.Source -3.12 -m venv $VirtualEnvironment
}

Invoke-CheckedCommand $VirtualPython -m pip install --disable-pip-version-check --editable "${RepositoryRoot}[dev]"
Invoke-CheckedCommand $VirtualPython -c "import sys; print(f'Repository environment ready: Python {sys.version.split()[0]}')"
