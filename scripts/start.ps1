$ErrorActionPreference="Stop"
Set-Location $PSScriptRoot\..
if (!(Test-Path ".venv\Scripts\python.exe")) { .\scripts\install.ps1 }
$port = if ($env:PORT) { $env:PORT } else { 8091 }
& ".\.venv\Scripts\python.exe" -m uvicorn backend.app:application --host 0.0.0.0 --port $port
