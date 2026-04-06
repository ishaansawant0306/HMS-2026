# Start backend and frontend development servers from the repo root.
# Usage: .\start-dev.ps1

Set-Location $PSScriptRoot

# Start Flask backend in a new PowerShell window
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd ./Backend; python app.py'

# Free port 3000 if a stale Node process is listening there
$port = 3000
$existing = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    $pid = $existing.OwningProcess
    $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
    if ($process -and $process.ProcessName -eq 'node') {
        Write-Host "Stopping stale Node process $pid on port $port"
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
}

# Start Vue frontend in a new PowerShell window
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd ./Frontend; npm install; npm run dev'

# Give servers a moment to start, then open the browser
Start-Sleep -Seconds 3
Start-Process 'http://localhost:3000'
