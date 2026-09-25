$ErrorActionPreference="Stop"
Set-Location $PSScriptRoot\..
if (!(Test-Path ".venv\Scripts\python.exe")) { py -m venv .venv }
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
if (!(Test-Path ".env")) { Copy-Item ".env.example" ".env" }
& ".\.venv\Scripts\python.exe" -m compileall backend bot | Out-Null
Write-Host "ROYAL GAMES V5 INSTALL OK" -ForegroundColor Green
