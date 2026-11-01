# Install library skills into a vessel skills directory on Windows 10/11 (PowerShell).
# Usage:
#   .\scripts\install.ps1 -Vessel agy -Dest "$HOME\.gemini\skills"
#   .\scripts\install.ps1 -Vessel codex -Dest "$HOME\.agents\skills" -Mode copy

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("agy", "grok", "opencode", "codex")]
    [string]$Vessel,

    [Parameter(Mandatory = $true)]
    [string]$Dest,

    [ValidateSet("auto", "copy", "symlink")]
    [string]$Mode = "copy"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallPy = Join-Path $ScriptDir "install.py"

foreach ($candidate in @(@("py", "-3"), @("python"), @("python3"))) {
    $exe = $candidate[0]
    $prefixArgs = if ($candidate.Length -gt 1) { $candidate[1..($candidate.Length - 1)] } else { @() }
    if (Get-Command $exe -ErrorAction SilentlyContinue) {
        & $exe @prefixArgs -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)" 2>$null
        if ($LASTEXITCODE -eq 0) {
            & $exe @prefixArgs $InstallPy --vessel $Vessel --dest $Dest --mode $Mode
            exit $LASTEXITCODE
        }
    }
}

Write-Error "Python 3.8+ is required on PATH to run scripts/install.py."
exit 1
