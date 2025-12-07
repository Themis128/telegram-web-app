# Update Cursor Configuration with Your New Credentials

## ✅ Your New Credentials

- **API ID:** `39954819`
- **API Hash:** `0068902be7634b2ee5076321410f0e65`
- **Phone:** `+306977777838`

## 📝 Update Cursor Settings

### Step 1: Open Cursor Settings File

**Quick way:**
1. Press `Win + R`
2. Type: `%APPDATA%\Cursor\User\settings.json`
3. Press Enter

**Or navigate to:**
```
C:\Users\baltz\AppData\Roaming\Cursor\User\settings.json
```

### Step 2: Add MCP Configuration

Add this configuration **before the closing `}`** at the end of the file:

```json
  "mcp": {
    "servers": {
      "telegram": {
        "command": "python",
        "args": ["-m", "mcp_telegram"],
        "env": {
          "TELEGRAM_API_ID": "39954819",
          "TELEGRAM_API_HASH": "0068902be7634b2ee5076321410f0e65",
          "TELEGRAM_PHONE_NUMBER": "+306977777838",
          "MCP_NONINTERACTIVE": "true"
        }
      }
    }
  },
```

**Important:**
- Add a comma (`,`) after the `}` if it's not the last item
- Make sure JSON is valid (no trailing commas on last item)
- Save the file after editing

### Step 3: Verify .env File

Your `.env` file has been updated automatically with:
- ✅ API ID: `39954819`
- ✅ API Hash: `0068902be7634b2ee5076321410f0e65`
- ✅ Phone: `+306977777838`

## 🚀 Final Steps

1. ✅ **.env file updated** (done automatically!)
2. ⏳ **Update Cursor settings.json** (add MCP config above)
3. ⏳ **Restart Cursor** completely
4. ⏳ **Authenticate** when prompted (enter code from Telegram)

## 🎯 After Restart

1. Cursor will connect to the MCP server
2. You'll receive a code in your Telegram app
3. Enter the code when prompted
4. Session will be saved for future use

## ✅ Test It Works

After authentication, try asking Cursor's AI:
- "List my Telegram chats"
- "Send a test message to saved messages"
- "Get my Telegram profile info"

---

**You're almost done! Just update settings.json and restart Cursor!** 🚀
