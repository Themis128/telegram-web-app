# PowerShell wrapper script to run the Telegram MCP setup test
# Usage: .\test-telegram-mcp-setup.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Telegram MCP Setup Test Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if Python is available
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Found Python at: $($pythonCmd.Path)" -ForegroundColor Green
Write-Host "Python version:" -ForegroundColor Yellow
& $pythonCmd.Path --version

# Check if test script exists
$scriptPath = Join-Path $PSScriptRoot "test_telegram_mcp_setup.py"
if (-not (Test-Path $scriptPath)) {
    Write-Host "`nERROR: test_telegram_mcp_setup.py not found" -ForegroundColor Red
    Write-Host "Make sure you're running this script from the project root directory" -ForegroundColor Yellow
    exit 1
}

# Run the test script
Write-Host "`nRunning test script...`n" -ForegroundColor Cyan
& $pythonCmd.Path $scriptPath

# Check exit code
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nTest script exited with code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "`nTest completed!" -ForegroundColor Green
