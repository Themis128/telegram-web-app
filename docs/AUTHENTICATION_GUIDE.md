# Telegram MCP Authentication Guide

## 🔐 How Authentication Works

### What Happens When Cursor Starts

1. **Cursor launches** and connects to the MCP server
2. **MCP server starts** and tries to authenticate with Telegram
3. **Telegram sends a code** to your Telegram app
4. **You enter the code** to complete authentication

## 📱 Where You'll See the Code

The code will appear in your **Telegram app** (on your phone or desktop):

- **Location:** Usually in a message from "Telegram" or "Telegram Desktop"
- **Format:** Usually 5-6 digits (e.g., `12345` or `ABC123`)
- **Message:** Something like "Your login code is: 12345"

## 💻 Where to Enter the Code

### Option 1: Cursor's Output Panel

1. **Open Output Panel:**
   - View → Output (or `Ctrl+Shift+U`)
   - Select "MCP" or "Telegram" from the dropdown

2. **Look for prompts:**
   - You might see: "Enter code:" or "Verification code:"
   - Type the code and press Enter

### Option 2: Cursor's Terminal

1. **Open Terminal:**
   - View → Terminal (or `` Ctrl+` ``)
   - Look for prompts asking for the code

### Option 3: Cursor's Notification/Popup

- Cursor might show a popup asking for the code
- Enter it in the popup dialog

### Option 4: Command Palette

1. Press `Ctrl+Shift+P`
2. Search for "MCP" or "Telegram"
3. Look for authentication commands

## 🔑 Step-by-Step Authentication

### First Time Setup

1. **Restart Cursor**
   - Close all Cursor windows
   - Reopen Cursor

2. **Wait for Connection**
   - Cursor will try to connect to Telegram
   - This may take 10-30 seconds

3. **Check Your Telegram App**
   - Open Telegram on your phone/desktop
   - Look for a code message
   - Code is usually 5-6 characters

4. **Enter the Code**
   - Find where Cursor is asking for it (Output panel, Terminal, or popup)
   - Type the code exactly as shown
   - Press Enter

5. **2FA (If Enabled)**
   - If you have Two-Factor Authentication enabled
   - You'll be prompted for your 2FA password
   - Enter your Telegram account password

6. **Success!**
   - Session will be saved
   - You won't need to authenticate again (unless session expires)

## 📍 Where to Look for Prompts

### Check These Locations:

1. **Cursor Output Panel:**
   ```
   View → Output → Select "MCP" or "Telegram"
   ```

2. **Cursor Terminal:**
   ```
   View → Terminal
   ```

3. **Cursor Status Bar:**
   - Bottom of Cursor window
   - May show MCP connection status

4. **Cursor Notifications:**
   - Bottom-right corner
   - May show authentication prompts

5. **Developer Console:**
   - Help → Toggle Developer Tools
   - Check Console tab

## ⚠️ Troubleshooting

### Code Not Received

- **Check Telegram app** is open and connected
- **Check phone number** is correct: `+306977777838`
- **Wait a bit longer** (can take 30-60 seconds)
- **Check spam/other chats** in Telegram

### Code Expired

- Codes expire after a few minutes
- **Restart Cursor** to get a new code
- The MCP server will request a new code automatically

### Can't Find Where to Enter Code

1. **Check Output Panel:**
   - View → Output
   - Look for MCP/Telegram output

2. **Check Terminal:**
   - View → Terminal
   - Look for prompts

3. **Check for Errors:**
   - Look for error messages
   - They might indicate what's wrong

### Authentication Fails

- **Verify credentials** in `.env` and `settings.json` match
- **Check API ID and Hash** are correct
- **Try restarting Cursor** again
- **Check Cursor's logs** for detailed error messages

## 🔄 After Authentication

Once authenticated:
- ✅ Session is saved locally
- ✅ You won't need to authenticate again (usually)
- ✅ MCP server will connect automatically on future starts
- ✅ You can start using Telegram commands immediately

## 📝 Session Storage

The session is typically saved in:
- Project directory or
- User home directory
- As a `.session` file or similar

**Don't delete session files** - they keep you logged in!

## 🎯 Quick Checklist

- [ ] Cursor restarted
- [ ] Telegram app open and connected
- [ ] Code received in Telegram
- [ ] Code entered in Cursor
- [ ] 2FA password entered (if applicable)
- [ ] Authentication successful

---

**After authentication, you're ready to use Telegram through Cursor!** 🚀
