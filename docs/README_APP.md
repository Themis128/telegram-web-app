# Telegram Web Application

A modern web application for managing your Telegram account through a beautiful web interface.

## Features

- 📱 **View Chats**: Browse all your Telegram chats and conversations
- 💬 **Send Messages**: Send messages to any chat directly from the web
- 📨 **Read Messages**: View message history for any conversation
- 🔐 **Secure Authentication**: Uses Telegram's official API with session management
- 🎨 **Modern UI**: Beautiful, responsive interface

## Prerequisites

- Python 3.8 or higher
- Telegram API credentials (API ID and API Hash)
- Your phone number registered with Telegram

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Make sure your `.env` file contains:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE_NUMBER=+1234567890
```

### 3. Run the Application

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Application

Open your browser and navigate to:

```
http://localhost:8000
```

## First Time Setup

1. When you first run the app, you'll need to authenticate
2. Enter the verification code sent to your Telegram app
3. If you have 2FA enabled, enter your password when prompted
4. Your session will be saved for future use

## Usage

### Viewing Chats

- All your chats will appear in the left sidebar
- Click on any chat to view its messages

### Sending Messages

1. Select a chat from the sidebar
2. Type your message in the input field
3. Press Enter or click the Send button

### Reading Messages

- Messages are automatically loaded when you select a chat
- Scroll to see older messages

## API Endpoints

- `GET /api/status` - Get connection status
- `POST /api/authenticate` - Authenticate with code
- `GET /api/chats` - Get list of chats
- `GET /api/messages/{chat_id}` - Get messages from a chat
- `POST /api/send` - Send a message

## Security Notes

- Session files are stored locally in your project directory
- Never share your `.env` file or session files
- The application runs locally by default

## Troubleshooting

### Connection Issues

- Make sure your `.env` file has correct credentials
- Check that Python and all dependencies are installed
- Verify your internet connection

### Authentication Problems

- Ensure you enter the code within the time limit
- Check that your phone number is correct (with country code)
- If 2FA is enabled, make sure to enter the password

### Session Expired

- Delete the session file (usually named `telegram_session_*.session`)
- Restart the application and authenticate again

## Development

To run in development mode with auto-reload:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## License

This project is for personal use. Make sure to comply with Telegram's Terms of Service.
