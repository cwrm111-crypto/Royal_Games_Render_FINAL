$project=(Resolve-Path "$PSScriptRoot\..").Path
$action=New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$project\scripts\run-30-days.ps1`""
$trigger=New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName "RoyalGamesUltimateV5-30Day" -Action $action -Trigger $trigger -Description "Royal Games Ultimate V5 local watchdog" -Force
Write-Host "Scheduled task registered." -ForegroundColor Green
