$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Script = Join-Path $RepoRoot "scripts\skillhub.py"

if (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 $Script install @args
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python $Script install @args
}
else {
    throw "Python 3 was not found."
}
