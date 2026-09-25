Set-Location $PSScriptRoot\..
if (!(Test-Path ".env")) { Copy-Item ".env.example" ".env" }
$token=Read-Host "New Telegram Bot Token (input locally; do not paste into chat)"
$url=Read-Host "Public HTTPS Mini App URL"
$lines=Get-Content ".env"
$lines=@($lines | Where-Object {$_ -notmatch '^TELEGRAM_BOT_TOKEN=' -and $_ -notmatch '^MINI_APP_URL=' -and $_ -notmatch '^ROYAL_GAMES_APP_URL='})
$lines+="TELEGRAM_BOT_TOKEN=$token"
$lines+="MINI_APP_URL=$url"
$lines+="ROYAL_GAMES_APP_URL=$url"
Set-Content ".env" $lines -Encoding UTF8
Write-Host "Telegram settings saved locally." -ForegroundColor Green
