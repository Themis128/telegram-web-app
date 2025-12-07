# Telegram MCP Setup Test Script

This test script verifies your Telegram MCP setup and helps identify any configuration issues.

## Quick Start

### Windows (PowerShell)
```powershell
.\test-telegram-mcp-setup.ps1
```

### Windows/Linux/Mac (Python)
```bash
python test_telegram_mcp_setup.py
```

## What the Script Checks

The test script performs the following checks:

1. **Python Version** - Verifies Python 3.8+ is installed
2. **Environment Variables** - Checks `.env` file exists and contains:
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`
   - `TELEGRAM_PHONE_NUMBER`
3. **Python Packages** - Verifies required packages are installed:
   - `mcp-telegram` (or `tgmcp`)
   - `telethon` (usually required)
   - `mcp` (MCP protocol library)
4. **MCP Server Import** - Tests if the MCP server module can be imported
5. **MCP Tools** - Lists expected Telegram MCP tools
6. **Cursor Configuration** - Checks if Cursor settings file exists and contains MCP configuration

## Expected Output

When all checks pass, you should see:

```
Tests Passed: 6/6

✓ PASS - Python Version
✓ PASS - Environment Variables
✓ PASS - Python Packages
✓ PASS - MCP Server Import
✓ PASS - MCP Tools
✓ PASS - Cursor Configuration
```

## Troubleshooting

### Missing Environment Variables

If the script reports missing environment variables:

1. Copy `env.example` to `.env`:
   ```powershell
   Copy-Item env.example .env
   ```

2. Edit `.env` and fill in your credentials from [my.telegram.org/apps](https://my.telegram.org/apps)

### Missing Python Packages

If packages are missing, install them:

```bash
pip install mcp-telegram
```

Or if using the alternative:

```bash
pip install tgmcp
```

### Cursor Configuration Not Found

This is normal if you haven't configured Cursor yet. The script will still work, but you'll need to:

1. Configure Cursor's MCP settings (see `CURSOR_MCP_CONFIG.md`)
2. Restart Cursor
3. Run the test script again

## Available MCP Tools

When the MCP server is connected through Cursor, you should have access to tools like:

- `send_message` - Send text messages
- `get_messages` - Read messages from chats
- `list_chats` - List all your chats/dialogs
- `get_chat_info` - Get chat information
- `search_messages` - Search for messages
- `get_user_info` - Get user information
- `send_media` - Send media files
- `delete_message` - Delete messages
- `edit_message` - Edit messages

**Note:** The exact tools available depend on your `mcp-telegram` implementation. To see the actual tools available in Cursor, ask Cursor's AI: "What Telegram MCP tools are available?"

## Next Steps After Testing

1. **If all checks pass:**
   - Restart Cursor completely
   - Check Cursor's output panel for MCP connection status
   - Try asking: "List my Telegram chats"
   - Authenticate when prompted (you'll receive a code in Telegram)

2. **If some checks fail:**
   - Fix the issues reported by the script
   - Run the script again to verify
   - Check the troubleshooting section above

## Additional Resources

- `HOW_TO_USE_TELEGRAM_IN_CURSOR.md` - How to use Telegram through Cursor
- `MCP_TELEGRAM_CAPABILITIES.md` - What the MCP server can do
- `CURSOR_MCP_CONFIG.md` - How to configure Cursor
- `README.md` - Main project documentation

## Script Options

The script runs automatically and provides a comprehensive report. There are no command-line options currently, but you can modify the script to add custom checks if needed.

## Notes

- The script checks for tools but cannot directly access MCP tools from a standalone Python script
- MCP tools are only accessible when Cursor is connected to the MCP server
- The script provides expected tool names based on common MCP Telegram implementations
- Actual available tools may vary depending on your `mcp-telegram` version
