# Quick Start & Testing Guide

## 🚀 Starting the Application

### 1. Activate Virtual Environment
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Or if that doesn't work:
venv\Scripts\activate
```

### 2. Start the Server
```powershell
python app.py
```

The server will start on `http://localhost:8001`

### 3. Open in Browser
Open your browser and navigate to:
```
http://localhost:8001
```

## ✅ Testing the Application

### Option 1: Use the Web Interface
1. Open `http://localhost:8001` in your browser
2. Authenticate with your Telegram verification code
3. Test all features through the UI:
   - ✅ View chats
   - ✅ Send messages
   - ✅ Send media (photos, videos, documents)
   - ✅ Edit messages
   - ✅ Delete messages
   - ✅ React to messages
   - ✅ Pin messages
   - ✅ Real-time updates via WebSocket

### Option 2: Use the Test Script
```powershell
# Make sure server is running first
python test_app.py
```

### Option 3: Test with cURL or Postman

#### Get Status
```bash
curl http://localhost:8001/api/status
```

#### Get Chats
```bash
curl http://localhost:8001/api/chats?limit=10
```

#### Send Message
```bash
curl -X POST http://localhost:8001/api/messages/send \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "YOUR_CHAT_ID", "message": "Hello!"}'
```

#### Send Media
```bash
curl -X POST http://localhost:8001/api/messages/send-media \
  -F "chat_id=YOUR_CHAT_ID" \
  -F "file=@photo.jpg" \
  -F "caption=My photo"
```

## 🔧 Features Available

### Messaging
- ✅ Send text messages
- ✅ Send media (photos, videos, documents, voice)
- ✅ Send locations
- ✅ Send contacts
- ✅ Edit messages
- ✅ Delete messages
- ✅ Forward messages
- ✅ Pin/unpin messages
- ✅ Add reactions
- ✅ Mark as read
- ✅ Scheduled messages

### Chat Management
- ✅ View all chats
- ✅ Create groups
- ✅ Create channels/supergroups
- ✅ Edit chat info
- ✅ Set chat photo
- ✅ Manage members
- ✅ Get invite links

### Contacts & Users
- ✅ View contacts
- ✅ Add/delete contacts
- ✅ Get user info
- ✅ Block/unblock users
- ✅ View profile photos

### Account
- ✅ View account info
- ✅ Update profile
- ✅ Update profile photo

### Real-time Updates
- ✅ WebSocket connection
- ✅ New message notifications
- ✅ Message edited notifications
- ✅ Message deleted notifications
- ✅ Chat action notifications

## 🐛 Troubleshooting

### Server won't start
1. Check if port 8001 is available
2. Make sure virtual environment is activated
3. Check if all dependencies are installed: `pip install -r requirements.txt`

### Authentication fails
1. Make sure you've run `auth_cli.py` first to create a session
2. Check your `.env` file has correct credentials
3. Try running `auth_cli.py` again

### WebSocket not connecting
1. Check browser console for errors
2. Make sure server is running
3. Check firewall settings

### API errors
1. Check server logs in terminal
2. Verify you're authenticated
3. Check API endpoint URLs

## 📝 Next Steps

1. **Customize the UI**: Edit `index.html` to match your preferences
2. **Add more features**: Use the API documentation to add more endpoints
3. **Deploy**: Consider deploying to a server for remote access
4. **Security**: Add authentication/authorization for production use

## 🔗 Useful Links

- API Documentation: See `TELETHON_FULL_CAPABILITIES.md`
- Telethon Docs: https://docs.telethon.dev/
- FastAPI Docs: https://fastapi.tiangolo.com/

---

**Happy Testing! 🎉**
