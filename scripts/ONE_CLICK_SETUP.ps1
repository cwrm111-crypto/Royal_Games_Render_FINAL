$ErrorActionPreference="Stop"
Set-Location $PSScriptRoot\..
Set-ExecutionPolicy -Scope Process Bypass -Force
.\scripts\install.ps1
.\scripts\test.ps1
if (!(Test-Path ".env")){Copy-Item ".env.example" ".env"}
Write-Host "Launching local backend in a new window..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","$PWD\scripts\start.ps1"
Write-Host "Setup complete. Open http://127.0.0.1:8091" -ForegroundColor Green
Write-Host "For Telegram bot run .\scripts\configure-telegram.ps1 then .\scripts\start-bot.ps1" -ForegroundColor Yellow
