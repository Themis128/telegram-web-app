"""
CLI Authentication Script for Telegram
This script handles authentication via command line
"""

import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# Load environment variables
load_dotenv()

async def authenticate():
    """Authenticate with Telegram via CLI"""

    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    phone = os.getenv("TELEGRAM_PHONE_NUMBER")

    if not all([api_id, api_hash, phone]):
        print("❌ Error: Missing credentials in .env file")
        print("Please make sure you have:")
        print("  - TELEGRAM_API_ID")
        print("  - TELEGRAM_API_HASH")
        print("  - TELEGRAM_PHONE_NUMBER")
        return False

    print(f"📱 Connecting to Telegram for {phone}...")

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Create session file name (store in data directory)
    session_name = f"data/telegram_session_{phone.replace('+', '')}"

    # Create client
    client = TelegramClient(session_name, int(api_id), api_hash)

    try:
        await client.connect()

        # Check if already authorized
        if await client.is_user_authorized():
            me = await client.get_me()
            print(f"✅ Already authenticated as {me.first_name} (@{me.username})")
            print(f"📁 Session saved in: {session_name}.session")
            await client.disconnect()
            return True

        # Not authorized, need to authenticate
        print("\n🔐 Authentication required")
        print("📨 Sending verification code to your Telegram app...")

        await client.send_code_request(phone)

        # Get code from user
        code = input("\n✉️  Enter the verification code you received: ").strip()

        try:
            # Try to sign in with code
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            # 2FA is enabled
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
        print("\n🎉 You can now use the web app!")

        await client.disconnect()
        return True

    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")
        await client.disconnect()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Telegram CLI Authentication")
    print("=" * 50)
    print()

    success = asyncio.run(authenticate())

    if success:
        print("\n✅ Authentication complete! You can now start the web app.")
        print("   Run: python app.py")
    else:
        print("\n❌ Authentication failed. Please check your credentials and try again.")
        exit(1)
