[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Output "PowerShell: $($PSVersionTable.PSVersion)"

$Python = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $Python) {
    Write-Output "Python: not found on PATH"
}
else {
    & $Python.Source --version
}

$Git = Get-Command git -ErrorAction SilentlyContinue
if ($null -eq $Git) {
    Write-Output "Git: not found on PATH"
}
else {
    & $Git.Source --version
}

$OperatingSystem = Get-CimInstance -ClassName Win32_OperatingSystem
$Processor = Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1
$TotalRamGiB = [Math]::Round($OperatingSystem.TotalVisibleMemorySize / 1MB, 1)

Write-Output "OS: $($OperatingSystem.Caption) $($OperatingSystem.Version)"
Write-Output "CPU: $($Processor.Name.Trim())"
Write-Output "RAM: $TotalRamGiB GiB"
Write-Output "Available drive space:"

Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DriveType = 3" |
    Sort-Object DeviceID |
    ForEach-Object {
        $FreeGiB = [Math]::Round($_.FreeSpace / 1GB, 1)
        Write-Output "  $($_.DeviceID) $FreeGiB GiB free"
    }
