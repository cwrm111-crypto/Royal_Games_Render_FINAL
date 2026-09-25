$ErrorActionPreference="Stop"
Set-Location $PSScriptRoot\..
if (!(Get-Command cloudflared -ErrorAction SilentlyContinue)) {
  Write-Host "cloudflared is not installed." -ForegroundColor Yellow
  Write-Host "Install Cloudflare Tunnel client first, then run this script again." -ForegroundColor Yellow
  exit 1
}
Write-Host "Starting Royal Games backend on 0.0.0.0:8091..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","$PWD\scripts\start.ps1"
Start-Sleep -Seconds 4
Write-Host "Starting temporary HTTPS tunnel. Keep this window open." -ForegroundColor Green
cloudflared tunnel --url http://127.0.0.1:8091
