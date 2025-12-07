#!/usr/bin/env python3
"""
Auto-Responder Script
Automatically responds to messages based on keywords or patterns.
"""

import requests
import time
import json
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8001")
API_KEY = os.getenv("API_KEY", None)  # Optional API key
CHECK_INTERVAL = 5  # Check every 5 seconds

# Response rules: keyword -> response message
RESPONSE_RULES = {
    "help": "Here's how I can help you:\n- Type 'info' for information\n- Type 'contact' for contact details",
    "info": "This is an automated Telegram client with full API access.",
    "contact": "You can reach us at support@example.com",
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What can I do for you?",
}

# Track processed messages to avoid duplicate responses
processed_messages = set()


def get_headers():
    """Get request headers with optional API key"""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    return headers


def get_chats():
    """Get list of all chats"""
    try:
        response = requests.get(f"{API_URL}/api/chats", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json().get("chats", [])
        return []
    except Exception as e:
        print(f"Error getting chats: {e}")
        return []


def get_messages(chat_id: str, limit: int = 10):
    """Get recent messages from a chat"""
    try:
        response = requests.get(
            f"{API_URL}/api/messages/{chat_id}?limit={limit}",
            headers=get_headers(),
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("messages", [])
        return []
    except Exception as e:
        print(f"Error getting messages: {e}")
        return []


def send_message(chat_id: str, message: str):
    """Send a message to a chat"""
    try:
        response = requests.post(
            f"{API_URL}/api/messages/send",
            headers=get_headers(),
            json={"chat_id": chat_id, "message": message},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending message: {e}")
        return False


def should_respond(message_text: str) -> tuple[bool, str]:
    """Check if we should respond and what to respond with"""
    if not message_text:
        return False, ""

    message_lower = message_text.lower().strip()

    # Check for exact keyword matches
    for keyword, response in RESPONSE_RULES.items():
        if message_lower == keyword or message_lower.startswith(f"{keyword} "):
            return True, response

    # Check for keyword in message
    for keyword, response in RESPONSE_RULES.items():
        if keyword in message_lower:
            return True, response

    return False, ""


def process_chat(chat_id: str):
    """Process messages in a chat and respond if needed"""
    messages = get_messages(chat_id, limit=5)

    for msg in messages:
        msg_id = msg.get("id")
        msg_key = f"{chat_id}_{msg_id}"

        # Skip if already processed
        if msg_key in processed_messages:
            continue

        # Skip outgoing messages (from us)
        if msg.get("is_out"):
            processed_messages.add(msg_key)
            continue

        # Check if we should respond
        message_text = msg.get("text", "")
        should, response = should_respond(message_text)

        if should:
            print(f"Responding to message in chat {chat_id}: {message_text[:50]}...")
            if send_message(chat_id, response):
                processed_messages.add(msg_key)
                print(f"✓ Sent response: {response[:50]}...")
            else:
                print(f"✗ Failed to send response")


def main():
    """Main loop"""
    print("🤖 Auto-Responder Started")
    print(f"API URL: {API_URL}")
    print(f"Response Rules: {len(RESPONSE_RULES)} keywords")
    print(f"Check Interval: {CHECK_INTERVAL} seconds")
    print("-" * 50)

    while True:
        try:
            chats = get_chats()
            print(f"Checking {len(chats)} chats...")

            for chat in chats:
                chat_id = str(chat.get("id"))
                process_chat(chat_id)

            # Clean up old processed messages (keep last 1000)
            if len(processed_messages) > 1000:
                processed_messages.clear()

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n👋 Auto-Responder Stopped")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
