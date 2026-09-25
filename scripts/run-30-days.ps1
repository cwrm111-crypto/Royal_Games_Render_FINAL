$ErrorActionPreference="Stop"; Set-Location $PSScriptRoot\..
$end=(Get-Date).AddDays(30)
while((Get-Date) -lt $end){
  $proc=Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","$PWD\scripts\start.ps1" -PassThru
  Start-Sleep -Seconds 6
  $bot=Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","$PWD\scripts\start-bot.ps1" -PassThru
  while((Get-Date) -lt $end){
    Start-Sleep -Seconds 20
    if($proc.HasExited){break}
    if($bot.HasExited){$bot=Start-Process powershell -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","$PWD\scripts\start-bot.ps1" -PassThru}
  }
  try{$proc.CloseMainWindow()}catch{};try{$bot.CloseMainWindow()}catch{}
}
