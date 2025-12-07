# PowerShell script to set up Telegram MCP Server for Cursor

Write-Host "Setting up Telegram MCP Server..." -ForegroundColor Green

# Check if Python is installed
Write-Host "`nChecking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Install mcp-telegram
Write-Host "`nInstalling mcp-telegram package..." -ForegroundColor Yellow
pip install mcp-telegram
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install mcp-telegram" -ForegroundColor Red
    exit 1
}
Write-Host "mcp-telegram installed successfully!" -ForegroundColor Green

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "`nCreating .env file from template..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host ".env file created. Please edit it with your Telegram credentials." -ForegroundColor Yellow
    Write-Host "Get your credentials from: https://my.telegram.org/apps" -ForegroundColor Cyan
} else {
    Write-Host "`.env file already exists. Skipping creation." -ForegroundColor Yellow
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your Telegram API credentials" -ForegroundColor White
Write-Host "2. Configure Cursor to use the MCP server (see README.md)" -ForegroundColor White
Write-Host "3. Restart Cursor" -ForegroundColor White
