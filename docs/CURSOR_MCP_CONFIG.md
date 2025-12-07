# Cursor MCP Configuration for Telegram

This guide explains how to configure the Telegram MCP server in Cursor IDE.

## Configuration Location

Cursor stores MCP server configurations in your user settings. The configuration file is typically located at:

**Windows:**
```
C:\Users\<YourUsername>\AppData\Roaming\Cursor\User\settings.json
```

## Configuration Steps

### Option 1: Using Cursor Settings UI

1. Open Cursor Settings:
   - Press `Ctrl+,` (or `Cmd+,` on Mac)
   - Or go to `File > Preferences > Settings`

2. Search for "MCP" in the settings search bar

3. Look for MCP server configuration options and add the Telegram server

### Option 2: Manual JSON Configuration

If Cursor supports direct MCP configuration, add the following to your `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "telegram": {
        "command": "python",
        "args": [
          "-m",
          "mcp_telegram"
        ],
        "env": {
          "TELEGRAM_API_ID": "YOUR_API_ID",
          "TELEGRAM_API_HASH": "YOUR_API_HASH",
          "TELEGRAM_PHONE_NUMBER": "YOUR_PHONE_NUMBER",
          "MCP_NONINTERACTIVE": "true"
        }
      }
    }
  }
}
```

**Note:** Replace the placeholder values with your actual credentials from the `.env` file.

### Option 3: Using Environment Variables

If Cursor reads from environment variables, you can set them in your system or use the `.env` file. Make sure Cursor can access these variables.

## Alternative: Using tgmcp

If you prefer using `tgmcp` instead of `mcp-telegram`, the configuration would be:

```json
{
  "mcp": {
    "servers": {
      "telegram": {
        "command": "tgmcp",
        "args": ["start"],
        "env": {
          "TELEGRAM_API_ID": "YOUR_API_ID",
          "TELEGRAM_API_HASH": "YOUR_API_HASH",
          "TELEGRAM_SESSION_STRING": "YOUR_SESSION_STRING",
          "MCP_NONINTERACTIVE": "true"
        }
      }
    }
  }
}
```

## Verification

After configuration:

1. Restart Cursor completely
2. Check Cursor's output/logs for MCP connection status
3. Try using Telegram-related commands in Cursor's AI chat

## Troubleshooting

### MCP Server Not Found
- Ensure Python is in your system PATH
- Verify the package is installed: `pip list | findstr mcp-telegram`
- Check that the command path is correct

### Authentication Issues
- Make sure your `.env` file contains valid credentials
- Verify your phone number includes the country code
- Check that you've completed the initial authentication

### Connection Errors
- Review Cursor's developer console for error messages
- Ensure the MCP server can be started manually: `python -m mcp_telegram`
- Check firewall settings if using network connections

## Additional Notes

- The exact configuration format may vary depending on your Cursor version
- Some Cursor versions may require the MCP server to be running as a separate process
- Check Cursor's documentation for the latest MCP configuration format
