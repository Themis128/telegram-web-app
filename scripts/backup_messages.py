#!/usr/bin/env python3
"""
Message Backup Script
Backs up all messages from chats to JSON files.
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8001")
API_KEY = os.getenv("API_KEY", None)
BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")


def get_headers():
    """Get request headers"""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    return headers


def get_chats():
    """Get list of all chats"""
    try:
        response = requests.get(f"{API_URL}/api/chats?limit=1000", headers=get_headers(), timeout=30)
        if response.status_code == 200:
            return response.json().get("chats", [])
        return []
    except Exception as e:
        print(f"Error getting chats: {e}")
        return []


def get_all_messages(chat_id: str, limit: int = 100):
    """Get all messages from a chat (with pagination)"""
    all_messages = []
    offset_id = 0
    
    while True:
        try:
            response = requests.get(
                f"{API_URL}/api/messages/{chat_id}?limit={limit}&offset_id={offset_id}",
                headers=get_headers(),
                timeout=30
            )
            if response.status_code != 200:
                break
            
            messages = response.json().get("messages", [])
            if not messages:
                break
            
            all_messages.extend(messages)
            
            # Update offset for next batch
            if len(messages) < limit:
                break
            offset_id = messages[-1].get("id", 0)
            
        except Exception as e:
            print(f"Error getting messages: {e}")
            break
    
    return all_messages


def backup_chat(chat: Dict):
    """Backup all messages from a chat"""
    chat_id = str(chat.get("id"))
    chat_name = chat.get("name", f"chat_{chat_id}")
    
    # Sanitize filename
    safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in chat_name)
    
    print(f"Backing up chat: {chat_name} ({chat_id})")
    
    messages = get_all_messages(chat_id)
    
    if not messages:
        print(f"  No messages found")
        return
    
    # Create backup data
    backup_data = {
        "chat": chat,
        "backup_date": datetime.now().isoformat(),
        "message_count": len(messages),
        "messages": messages
    }
    
    # Save to file
    os.makedirs(BACKUP_DIR, exist_ok=True)
    filename = f"{BACKUP_DIR}/{safe_name}_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Backed up {len(messages)} messages to {filename}")


def main():
    """Main backup function"""
    print("💾 Message Backup Started")
    print(f"API URL: {API_URL}")
    print(f"Backup Directory: {BACKUP_DIR}")
    print("-" * 50)
    
    chats = get_chats()
    print(f"Found {len(chats)} chats to backup")
    print()
    
    for i, chat in enumerate(chats, 1):
        print(f"[{i}/{len(chats)}] ", end="")
        try:
            backup_chat(chat)
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()
    
    print("✅ Backup Complete!")


if __name__ == "__main__":
    main()

