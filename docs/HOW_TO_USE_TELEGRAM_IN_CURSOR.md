# How to Use Telegram Through Cursor's AI

## 🚀 Getting Started

### Step 1: Restart Cursor (If Not Done Yet)

1. **Close Cursor completely** (all windows)
2. **Reopen Cursor**
3. Wait for Cursor to initialize

### Step 2: First-Time Authentication

When Cursor starts, the MCP server will try to connect. You may see:

1. **A prompt in Cursor** asking for authentication
2. **OR** you'll receive a code in your Telegram app
3. **Enter the code** when prompted
4. If you have 2FA enabled, enter your password too

### Step 3: Verify Connection

Check if the MCP server is connected:
- Look at Cursor's status bar (bottom)
- Check Cursor's output/logs panel
- Look for any MCP connection messages

## 💬 How to Use Telegram Through Cursor

### Basic Commands

Just ask Cursor's AI chat in natural language:

**List your chats:**
```
List my Telegram chats
```
or
```
Show me all my Telegram conversations
```

**Send a message:**
```
Send a message to [username or chat name] saying "Hello!"
```
or
```
Send "Test message" to my saved messages
```

**Read messages:**
```
Read the last 10 messages from [chat name]
```
or
```
What are the recent messages in [chat name]?
```

**Get chat information:**
```
Get information about chat [name]
```
or
```
Show me details about [username]
```

**Search messages:**
```
Search for messages containing "keyword" in [chat name]
```

## 📋 Example Conversations

### Example 1: Check Your Chats
**You:** "List my Telegram chats"

**Cursor AI:** Will show you all your chats/dialogs

### Example 2: Send a Message
**You:** "Send a message to saved messages saying 'Hello from Cursor!'"

**Cursor AI:** Will send the message via Telegram

### Example 3: Read Messages
**You:** "Read the last 5 messages from [friend's name]"

**Cursor AI:** Will fetch and display the messages

### Example 4: Get Profile Info
**You:** "Get my Telegram profile information"

**Cursor AI:** Will show your account details

## 🎯 Available Features

The MCP server typically provides:

✅ **Messaging:**
- Send text messages
- Send media (photos, videos, files)
- Reply to messages
- Edit messages
- Delete messages

✅ **Reading:**
- Read message history
- Search messages
- Get unread messages
- Read specific chats

✅ **Chat Management:**
- List all chats
- Get chat information
- Get chat participants
- Manage contacts

✅ **User Operations:**
- Get user information
- Search for users
- Get profile details

## ⚠️ Troubleshooting

### MCP Server Not Connecting

1. **Check Python is installed:**
   ```powershell
   python --version
   ```

2. **Verify mcp-telegram is installed:**
   ```powershell
   pip list | findstr mcp-telegram
   ```

3. **Check Cursor's output panel:**
   - View → Output
   - Look for MCP or Telegram errors

4. **Verify settings.json:**
   - Make sure the configuration is correct
   - Check JSON syntax is valid

### Authentication Issues

- Make sure you enter the code from Telegram
- Check your phone number is correct: `+306977777838`
- Verify API credentials in `.env` and `settings.json` match

### "Command not found" Errors

- Ensure Python is in your system PATH
- Try using full path to Python in settings.json

## 🔍 Check MCP Server Status

In Cursor:
1. Open Command Palette (`Ctrl+Shift+P`)
2. Search for "MCP" or "Model Context Protocol"
3. Look for connection status

## 📝 Tips

- **Be specific:** "Send message to @username" works better than "send a message"
- **Use chat names:** You can use chat names or usernames
- **Saved messages:** Use "saved messages" to send to yourself
- **Natural language:** Just ask naturally, the AI will translate to Telegram commands

## 🎉 You're Ready!

Once Cursor restarts and you authenticate, you can start using Telegram through natural language conversations with Cursor's AI!

---

**Try it now:** Restart Cursor, authenticate, then ask "List my Telegram chats"! 🚀

