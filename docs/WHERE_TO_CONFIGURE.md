# Where to Configure Telegram MCP in Cursor

## Exact Location

After adding your credentials to the `.env` file, configure Cursor here:

### **Method 1: Cursor Settings UI (Easiest)**

1. **Open Cursor Settings:**
   - Press `Ctrl+,` (Control + Comma)
   - OR go to: `File` → `Preferences` → `Settings`

2. **Search for MCP:**
   - In the settings search bar at the top, type: `MCP`
   - OR search for: `Model Context Protocol`

3. **Add Telegram Server:**
   - Look for "MCP Servers" or "Model Context Protocol Servers" section
   - Click "Add Server" or the `+` button
   - Configure as shown below

### **Method 2: Edit Settings File Directly (If UI doesn't work)**

**File Location:**
```
C:\Users\baltz\AppData\Roaming\Cursor\User\settings.json
```

**Quick Access:**
1. Press `Win + R`
2. Type: `%APPDATA%\Cursor\User\settings.json`
3. Press Enter
4. The file will open in Cursor

**Add this configuration to the file:**

```json
{
  "mcp": {
    "servers": {
      "telegram": {
        "command": "python",
        "args": ["-m", "mcp_telegram"],
        "env": {
          "TELEGRAM_API_ID": "YOUR_API_ID_HERE",
          "TELEGRAM_API_HASH": "YOUR_API_HASH_HERE",
          "TELEGRAM_PHONE_NUMBER": "YOUR_PHONE_NUMBER_HERE",
          "MCP_NONINTERACTIVE": "true"
        }
      }
    }
  }
}
```

**Important:**
- Replace `YOUR_API_ID_HERE`, `YOUR_API_HASH_HERE`, and `YOUR_PHONE_NUMBER_HERE` with your actual values from the `.env` file
- Make sure the JSON is valid (no trailing commas, proper quotes)
- Save the file after editing

## Step-by-Step Configuration

### Step 1: Get Your Credentials from .env
Open your `.env` file and copy:
- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `TELEGRAM_PHONE_NUMBER`

### Step 2: Configure in Cursor

**Option A: Via Settings UI**
1. `Ctrl+,` → Search "MCP" → Add server → Paste configuration

**Option B: Via settings.json**
1. Open: `%APPDATA%\Cursor\User\settings.json`
2. Add the configuration above
3. Replace placeholders with your actual values
4. Save

### Step 3: Restart Cursor
- Close Cursor completely
- Reopen it
- The MCP server should connect automatically

## Verification

After restarting Cursor:
1. Check the bottom status bar for MCP connection status
2. Open Cursor's AI chat
3. Try asking: "List my Telegram chats" or "Send a test message"
4. If it works, you're configured correctly!

## Troubleshooting

**If settings.json doesn't have "mcp" section:**
- Add it at the root level of the JSON object
- Make sure it's properly formatted

**If you get errors:**
- Check that Python is in your PATH: `python --version`
- Verify mcp-telegram is installed: `pip list | findstr mcp-telegram`
- Check Cursor's output panel for error messages

## Quick Reference

| Item | Location |
|------|----------|
| Cursor Settings UI | `Ctrl+,` then search "MCP" |
| Settings File | `%APPDATA%\Cursor\User\settings.json` |
| **Your Settings File** | **`C:\Users\baltz\AppData\Roaming\Cursor\User\settings.json`** |
| Your AppData | `C:\Users\baltz\AppData\Roaming` |
| .env File | `D:\Nuxt Projects\telegram\.env` |

## Exact Steps for Your System

### Step 1: Open Your Settings File
**Quick way:**
1. Press `Win + R`
2. Type: `%APPDATA%\Cursor\User\settings.json`
3. Press Enter
4. File opens in Cursor

**Or manually navigate to:**
```
C:\Users\baltz\AppData\Roaming\Cursor\User\settings.json
```

### Step 2: Add MCP Configuration
Add this configuration **before the closing brace** `}` at the end of the file:

```json
  "mcp": {
    "servers": {
      "telegram": {
        "command": "python",
        "args": ["-m", "mcp_telegram"],
        "env": {
          "TELEGRAM_API_ID": "YOUR_API_ID_HERE",
          "TELEGRAM_API_HASH": "YOUR_API_HASH_HERE",
          "TELEGRAM_PHONE_NUMBER": "YOUR_PHONE_NUMBER_HERE",
          "MCP_NONINTERACTIVE": "true"
        }
      }
    }
  },
```

**Important:**
- Add a comma after the `}` if it's not the last item
- Replace the placeholder values with your actual credentials from `.env`
- Make sure JSON is valid (use a JSON validator if unsure)

### Step 3: Save and Restart
1. Save the file (`Ctrl+S`)
2. Close Cursor completely
3. Reopen Cursor
4. The MCP server should connect automatically

---

**Next:** After configuration, restart Cursor and authenticate with Telegram when prompted!
