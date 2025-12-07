# 📱 Telegram Web App

A modern, full-featured Telegram web client built with **FastAPI** and **Telethon**, featuring a beautiful UI and **Progressive Web App (PWA)** support.

![Telegram Web App](https://img.shields.io/badge/Telegram-Web%20App-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)
![PWA](https://img.shields.io/badge/PWA-Enabled-purple)

## ✨ Features

### 🚀 Core Features
- **Full MTProto API Access** - Complete Telegram functionality via Telethon
- **Modern UI** - Beautiful Telegram-inspired interface
- **Progressive Web App** - Installable, works offline
- **Real-time Updates** - WebSocket support for live message updates
- **Media Support** - Send photos, videos, documents, voice messages
- **Message Management** - Edit, delete, forward, pin, react to messages
- **Chat Management** - Create groups/channels, manage members
- **Contact Management** - Add, delete, block contacts
- **Search** - Search messages across all chats
- **Account Management** - Update profile, change photo

### 📱 PWA Features
- ✅ Installable on desktop and mobile
- ✅ Offline support with service worker
- ✅ App-like experience (standalone mode)
- ✅ Fast loading with intelligent caching
- ✅ Push notifications ready

## 🛠️ Tech Stack

- **Backend**: FastAPI, Telethon, Python
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **PWA**: Service Worker, Web App Manifest
- **Real-time**: WebSocket

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram API credentials from [my.telegram.org/apps](https://my.telegram.org/apps)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-web-app.git
cd telegram-web-app
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy the example environment file:
   ```bash
   # Windows
   copy env.example .env
   
   # Linux/Mac
   cp env.example .env
   ```

2. Edit `.env` and add your Telegram credentials:
   ```env
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_PHONE_NUMBER=+1234567890
   ```

3. Get your API credentials from [my.telegram.org/apps](https://my.telegram.org/apps)

### 4. Authenticate

Run the authentication script:
```bash
python scripts/auth_cli.py
```

Enter the verification code sent to your Telegram app.

### 5. Generate PWA Icons (Optional)

```bash
python generate_icons.py
```

### 6. Start the Server

```bash
python app.py
```

The app will be available at `http://localhost:8001`

## 📖 Usage

### Web Interface

1. Open `http://localhost:8001` in your browser
2. Authenticate with your verification code (if needed)
3. Start using all Telegram features!

### Install as PWA

1. Visit the app in a supported browser (Chrome, Edge, Safari)
2. Click the install banner or use browser menu
3. The app will be installed and work offline

### API Endpoints

The app provides a comprehensive REST API. See [API Documentation](docs/API_DOCUMENTATION.md) for details.

**Key Endpoints:**
- `GET /api/status` - Connection status
- `GET /api/chats` - List all chats
- `GET /api/messages/{chat_id}` - Get messages
- `POST /api/messages/send` - Send message
- `POST /api/messages/send-media` - Send media
- `POST /api/messages/edit` - Edit message
- `POST /api/messages/delete` - Delete message
- `POST /api/messages/react` - Add reaction
- And 40+ more endpoints!

## 📁 Project Structure

```
telegram-web-app/
├── app.py                 # FastAPI backend application
├── index.html             # Frontend UI
├── manifest.json          # PWA manifest
├── sw.js                  # Service worker
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from env.example)
├── generate_icons.py      # Icon generator script
├── scripts/
│   ├── auth_cli.py        # Authentication CLI
│   └── test_app.py        # API test script
├── docs/                  # Documentation
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=+1234567890
```

### PWA Configuration

Edit `manifest.json` to customize:
- App name and description
- Theme colors
- Icons
- Display mode

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md) - Complete API reference
- [PWA Implementation](PWA_IMPLEMENTATION.md) - PWA setup guide
- [Quick Start Testing](QUICK_START_TESTING.md) - Testing guide
- [Implementation Complete](IMPLEMENTATION_COMPLETE.md) - Feature list

## 🎯 Features in Detail

### Messaging
- Send text messages with formatting
- Send media (photos, videos, documents, voice)
- Send locations and contacts
- Edit and delete messages
- Forward messages
- Pin/unpin messages
- Add reactions
- Scheduled messages
- Reply to messages

### Chat Management
- Create groups and channels
- Edit chat information
- Manage members
- Set chat photos
- Create invite links
- Get chat statistics

### Contacts & Users
- Manage contacts
- Block/unblock users
- View profile photos
- Get user information

### Search
- Search messages in specific chats
- Global message search

### Account
- Update profile information
- Change profile photo
- View account details

## 🔒 Security

- Session files are stored locally
- API credentials in `.env` (not committed)
- HTTPS recommended for production
- Service worker uses secure caching

## 🐛 Troubleshooting

### Authentication Issues
- Make sure your phone number includes country code
- Verify API credentials are correct
- Check internet connectivity

### Server Won't Start
- Check if port 8001 is available
- Verify virtual environment is activated
- Ensure all dependencies are installed

### PWA Not Working
- Use HTTPS in production (required for service worker)
- Check browser console for errors
- Verify manifest.json is accessible

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Telethon](https://github.com/LonamiWebs/Telethon) - Python Telegram client
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Telegram](https://telegram.org/) - For the amazing platform

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `docs/` folder
- Review troubleshooting section

## 🚀 Roadmap

- [ ] Push notifications
- [ ] Voice/video calls
- [ ] Stories support
- [ ] Secret chats
- [ ] Multi-account support
- [ ] Themes customization
- [ ] Advanced search filters

---

**Made with ❤️ using Telegram MTProto API**

⭐ Star this repo if you find it useful!
