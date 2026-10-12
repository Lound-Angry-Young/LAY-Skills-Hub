param(
    [ValidateSet('all','codex','claude','antigravity')]
    [string]$Agents = 'all',
    [string]$UserHome = $env:USERPROFILE
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python 3.10+ não encontrado no PATH.' }
& python (Join-Path $repoRoot 'scripts\skill_hub.py') install --home $UserHome --agents $Agents
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& python (Join-Path $repoRoot 'scripts\skill_hub.py') doctor --home $UserHome
exit $LASTEXITCODE
