# Quick Access Guide

## 🌐 Accessing the App

The server is configured to listen on **all network interfaces** (`0.0.0.0`), but you **cannot** access it using `0.0.0.0` in your browser.

### ✅ Correct URLs to Use:

- **http://localhost:8001** ← Use this!
- **http://127.0.0.1:8001** ← Alternative

### ❌ Don't Use:

- ~~http://0.0.0.0:8001~~ ← This won't work in browsers!

## 🔍 Why?

- `0.0.0.0` means "listen on all network interfaces" (server configuration)
- `localhost` or `127.0.0.1` is what browsers use to connect to your local machine
- They're different things!

## 🚀 Starting the Server

```bash
npm start
```

After authentication, the server will start and you'll see:
```
🌐 Server is starting...
📱 Open your browser and go to: http://localhost:8001
```

## ✅ Verify Server is Running

Check if port 8001 is in use:
```bash
# Windows
netstat -ano | findstr :8001

# Linux/Mac
lsof -i :8001
```

If you see output, the server is running!

## 🐛 Troubleshooting

### Server won't start?
- Check if port 8001 is already in use
- Make sure virtual environment is activated
- Verify all dependencies are installed

### Can't access localhost?
- Try `127.0.0.1:8001` instead
- Check firewall settings
- Make sure server actually started (check terminal output)

### Connection refused?
- Server might not be running
- Check terminal for error messages
- Verify authentication completed successfully

---

**Remember: Always use `localhost` or `127.0.0.1`, never `0.0.0.0`!**
