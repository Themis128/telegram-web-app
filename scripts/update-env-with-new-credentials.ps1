# Update .env file with new Telegram credentials

Write-Host "Updating .env file with your new credentials..." -ForegroundColor Green

$envContent = @"
# Telegram API Credentials
# Get these from https://my.telegram.org/apps
TELEGRAM_API_ID=39954819
TELEGRAM_API_HASH=0068902be7634b2ee5076321410f0e65

# Phone number (with country code, e.g., +1234567890)
TELEGRAM_PHONE_NUMBER=+306977777838

# Session string (optional - will be generated on first run)
# TELEGRAM_SESSION_STRING=

# MCP Server Configuration
MCP_NONINTERACTIVE=true
"@

$envContent | Out-File -FilePath .env -Encoding utf8

Write-Host "`n✅ .env file updated successfully!" -ForegroundColor Green
Write-Host "`nYour credentials:" -ForegroundColor Cyan
Write-Host "  API ID: 39954819" -ForegroundColor White
Write-Host "  API Hash: 0068902be7634b2ee5076321410f0e65" -ForegroundColor White
Write-Host "  Phone: +306977777838" -ForegroundColor White
Write-Host "`nNext step: Update Cursor's settings.json (see UPDATE_CURSOR_CONFIG.md)" -ForegroundColor Yellow
