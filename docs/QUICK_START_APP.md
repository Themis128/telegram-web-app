# Quick Start - Telegram Web App

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

**Windows (PowerShell):**
```powershell
.\start_app.ps1
```

**Linux/Mac:**
```bash
chmod +x start_app.sh
./start_app.sh
```

**Or manually:**
```bash
pip install -r requirements.txt
```

### Step 2: Configure Credentials

Make sure your `.env` file has your Telegram credentials:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=+1234567890
```

### Step 3: Run the App

```bash
python app.py
```

Then open: **http://localhost:8000**

## 📱 First Time Authentication

1. When you first open the app, you'll see an authentication form
2. Check your Telegram app for a verification code
3. Enter the code in the web app
4. If you have 2FA, enter your password when prompted
5. You're ready to use Telegram!

## ✨ Features

- ✅ View all your chats
- ✅ Send messages
- ✅ Read message history
- ✅ Beautiful modern UI
- ✅ Real-time updates

## 🎯 Usage Tips

- **Select a chat** from the left sidebar to view messages
- **Type and press Enter** to send messages
- **Scroll** to see older messages
- The app automatically saves your session

## 🔧 Troubleshooting

**Can't connect?**
- Check your `.env` file has correct credentials
- Make sure you're connected to the internet
- Verify your API credentials at https://my.telegram.org/apps

**Authentication failed?**
- Make sure you enter the code quickly (it expires)
- Check your phone number includes country code (+)
- If 2FA is enabled, enter your password

**Session expired?**
- Delete the `.session` file in the project directory
- Restart the app and authenticate again

---

**Enjoy your Telegram Web App!** 🎉
