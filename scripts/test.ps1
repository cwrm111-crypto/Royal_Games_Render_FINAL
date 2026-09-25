Set-Location $PSScriptRoot\..
& ".\.venv\Scripts\python.exe" -m compileall backend bot
if ($LASTEXITCODE -ne 0){exit 1}
Write-Host "PYTHON COMPILE OK" -ForegroundColor Green
