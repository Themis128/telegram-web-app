# Script to update .env file with your credentials

Write-Host "Updating .env file with your credentials..." -ForegroundColor Green

$envContent = @"
# Telegram API Credentials
# Get these from https://my.telegram.org/apps
TELEGRAM_API_ID=7017840434
TELEGRAM_API_HASH=YOUR_API_HASH_HERE

# Phone number (with country code, e.g., +1234567890)
TELEGRAM_PHONE_NUMBER=+306977777838

# Session string (optional - will be generated on first run)
# TELEGRAM_SESSION_STRING=

# MCP Server Configuration
MCP_NONINTERACTIVE=true
"@

$envContent | Out-File -FilePath .env -Encoding utf8

Write-Host "`n.env file updated!" -ForegroundColor Green
Write-Host "`n⚠️  IMPORTANT: You still need to add your API Hash!" -ForegroundColor Yellow
Write-Host "`nTo get your API Hash:" -ForegroundColor Cyan
Write-Host "1. Go to: https://my.telegram.org/apps" -ForegroundColor White
Write-Host "2. Log in with your phone: +306977777838" -ForegroundColor White
Write-Host "3. Copy your api_hash" -ForegroundColor White
Write-Host "4. Edit .env and replace 'YOUR_API_HASH_HERE' with your actual hash" -ForegroundColor White
Write-Host "`nYour .env file is ready, just needs the API Hash!" -ForegroundColor Green
