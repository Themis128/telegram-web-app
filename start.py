"""
Startup script for Telegram Web App
Handles authentication check and starts the server
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Load environment variables
load_dotenv()

async def check_authentication():
    """Check if user is authenticated, prompt if not"""
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    phone = os.getenv("TELEGRAM_PHONE_NUMBER")

    if not all([api_id, api_hash, phone]):
        print("❌ Error: Missing Telegram credentials in .env file")
        print("Please make sure you have:")
        print("  - TELEGRAM_API_ID")
        print("  - TELEGRAM_API_HASH")
        print("  - TELEGRAM_PHONE_NUMBER")
        return False

    # Use same session location as app.py
    os.makedirs("data", exist_ok=True)
    session_name = f"data/telegram_session_{phone.replace('+', '')}"
    client = TelegramClient(session_name, int(api_id), api_hash)

    try:
        await client.connect()

        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ Authenticated as {me.first_name} (@{me.username or 'no username'})")
            await client.disconnect()
            return True
        else:
            print("\n🔐 Authentication required")
            print("📨 Sending verification code to your Telegram app...")

            await client.send_code_request(phone)

            # Get code from user
            code = input("\n✉️  Enter the verification code you received: ").strip()

            try:
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                print("\n🔒 Two-factor authentication is enabled")
                password = input("🔑 Enter your 2FA password: ").strip()
                await client.sign_in(password=password)

            # Get user info
            me = await client.get_me()
            print(f"\n✅ Successfully authenticated!")
            print(f"👤 Logged in as: {me.first_name} {me.last_name or ''}")
            print(f"📱 Username: @{me.username}" if me.username else "📱 No username")
            print(f"🆔 User ID: {me.id}")
            print(f"📁 Session saved in: {session_name}.session")
            print("\n🚀 Starting server...\n")

            await client.disconnect()
            return True

    except KeyboardInterrupt:
        print("\n\n❌ Authentication cancelled")
        await client.disconnect()
        return False
    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")
        await client.disconnect()
        return False

def main():
    """Main function to check auth and start server"""
    print("=" * 60)
    print("Telegram Web App - Starting...")
    print("=" * 60)

    # Check authentication
    try:
        authenticated = asyncio.run(check_authentication())
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    if not authenticated:
        print("\n❌ Authentication failed. Please try again.")
        sys.exit(1)

    # Start the FastAPI server
    print("=" * 60)
    print("Starting FastAPI server...")
    print("=" * 60)
    print("🌐 Server is starting...")
    print("📱 Open your browser and go to: http://localhost:8001")
    print("   (or http://127.0.0.1:8001)")
    print("\n⚠️  Note: Use 'localhost' or '127.0.0.1', NOT '0.0.0.0'")
    print("=" * 60)
    print()

    # Import and run the app
    import uvicorn
    from app import app

    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    main()
