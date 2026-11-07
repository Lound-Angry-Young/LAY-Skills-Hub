param(
    [ValidateSet('all','codex','claude','antigravity')]
    [string]$Agents = 'all',
    [ValidateSet('complete','public')]
    [string]$Mode = 'complete',
    [string]$UserHome = $env:USERPROFILE,
    [switch]$DryRun,
    [switch]$SkipTools
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python 3.10+ não encontrado no PATH.' }

$cmdArgs = @(
    (Join-Path $repoRoot 'scripts\skill_hub.py'),
    'install',
    '--home', $UserHome,
    '--agents', $Agents,
    '--mode', $Mode
)
if ($DryRun) { $cmdArgs += '--dry-run' }
if ($SkipTools) { $cmdArgs += '--skip-tools' }

& python @cmdArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (-not $DryRun) {
    & python (Join-Path $repoRoot 'scripts\skill_hub.py') doctor --home $UserHome
}
exit $LASTEXITCODE
