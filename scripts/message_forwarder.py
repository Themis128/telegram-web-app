#!/usr/bin/env python3
"""
Message Forwarder Script
Automatically forwards messages from one chat to another based on rules.
"""

import requests
import time
import json
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8001")
API_KEY = os.getenv("API_KEY", None)

# Forwarding rules: source_chat_id -> [target_chat_ids]
FORWARDING_RULES = {
    # Example: Forward messages from chat "123456" to chats "789012" and "345678"
    # "123456": ["789012", "345678"],
}

# Filter rules: only forward messages matching these conditions
FILTER_KEYWORDS = []  # Only forward if message contains these keywords (empty = forward all)
FILTER_SENDERS = []   # Only forward from these sender IDs (empty = forward from all)

# Track processed messages
processed_messages = set()


def get_headers():
    """Get request headers"""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    return headers


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


def forward_message(from_chat_id: str, to_chat_id: str, message_ids: List[int]):
    """Forward messages from one chat to another"""
    try:
        response = requests.post(
            f"{API_URL}/api/messages/forward",
            headers=get_headers(),
            json={
                "from_chat_id": from_chat_id,
                "to_chat_id": to_chat_id,
                "message_ids": message_ids
            },
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error forwarding message: {e}")
        return False


def should_forward(message: Dict) -> bool:
    """Check if message should be forwarded based on filters"""
    # Check sender filter
    if FILTER_SENDERS:
        sender_id = message.get("sender_id")
        if sender_id and str(sender_id) not in FILTER_SENDERS:
            return False
    
    # Check keyword filter
    if FILTER_KEYWORDS:
        message_text = message.get("text", "").lower()
        if not any(keyword.lower() in message_text for keyword in FILTER_KEYWORDS):
            return False
    
    return True


def process_forwarding_rules():
    """Process all forwarding rules"""
    for source_chat_id, target_chat_ids in FORWARDING_RULES.items():
        if not target_chat_ids:
            continue
        
        messages = get_messages(source_chat_id, limit=10)
        
        for msg in messages:
            msg_id = msg.get("id")
            msg_key = f"{source_chat_id}_{msg_id}"
            
            # Skip if already processed
            if msg_key in processed_messages:
                continue
            
            # Skip outgoing messages
            if msg.get("is_out"):
                processed_messages.add(msg_key)
                continue
            
            # Check if should forward
            if not should_forward(msg):
                processed_messages.add(msg_key)
                continue
            
            # Forward to all target chats
            for target_chat_id in target_chat_ids:
                print(f"Forwarding message {msg_id} from {source_chat_id} to {target_chat_id}")
                if forward_message(source_chat_id, target_chat_id, [msg_id]):
                    print(f"✓ Forwarded successfully")
                else:
                    print(f"✗ Failed to forward")
            
            processed_messages.add(msg_key)


def main():
    """Main loop"""
    print("📨 Message Forwarder Started")
    print(f"API URL: {API_URL}")
    print(f"Forwarding Rules: {len(FORWARDING_RULES)}")
    print(f"Filter Keywords: {FILTER_KEYWORDS or 'None (forward all)'}")
    print(f"Filter Senders: {FILTER_SENDERS or 'None (forward from all)'}")
    print("-" * 50)
    
    if not FORWARDING_RULES:
        print("⚠️  No forwarding rules configured!")
        print("Edit FORWARDING_RULES in this script to add rules.")
        return
    
    while True:
        try:
            process_forwarding_rules()
            
            # Clean up old processed messages
            if len(processed_messages) > 1000:
                processed_messages.clear()
            
            time.sleep(5)  # Check every 5 seconds
            
        except KeyboardInterrupt:
            print("\n\n👋 Message Forwarder Stopped")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)


if __name__ == "__main__":
    main()

