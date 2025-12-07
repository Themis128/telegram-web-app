# Quick Start Guide - Telegram MCP Server

## Fast Setup (5 minutes)

### 1. Get Telegram API Credentials (2 min)
- Visit: https://my.telegram.org/apps
- Log in with your phone number
- Create an application
- Copy your **API ID** and **API Hash**

### 2. Install Package (1 min)
```powershell
pip install mcp-telegram
```

### 3. Create .env File (1 min)
```powershell
Copy-Item env.example .env
```

Then edit `.env` and add your credentials:
```
TELEGRAM_API_ID=your_actual_api_id
TELEGRAM_API_HASH=your_actual_api_hash
TELEGRAM_PHONE_NUMBER=+1234567890
```

### 4. Configure Cursor (1 min)

**Option A: Use the setup script**
```powershell
.\setup-telegram-mcp.ps1
```

**Option B: Manual configuration**

1. Open Cursor Settings (`Ctrl+,`)
2. Search for "MCP"
3. Add Telegram MCP server configuration (see `CURSOR_MCP_CONFIG.md` for details)

### 5. Test Connection

1. Restart Cursor
2. The MCP server will prompt for authentication on first run
3. Enter the code sent to your Telegram app
4. You're ready to use Telegram through Cursor!

## What You Can Do

Once configured, you can:
- ✅ Send messages via Telegram
- ✅ Read messages from chats
- ✅ List your contacts and chats
- ✅ Use Telegram features through Cursor's AI assistant

## Need Help?

- See `README.md` for detailed instructions
- See `CURSOR_MCP_CONFIG.md` for Cursor-specific configuration
- Check troubleshooting section in `README.md`
