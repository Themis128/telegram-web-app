#!/usr/bin/env python3
"""
Quick Feature Test - Tests all new features
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_URL", "http://localhost:8001")

def test_endpoint(method, endpoint, data=None, description=""):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=5)
        
        status = "✅" if response.status_code in [200, 201] else "❌"
        print(f"{status} {description}: HTTP {response.status_code}")
        if response.status_code not in [200, 201]:
            print(f"   Response: {response.text[:100]}")
        return response.status_code in [200, 201]
    except requests.exceptions.ConnectionError:
        print(f"❌ {description}: Connection refused (server not running?)")
        return False
    except Exception as e:
        print(f"❌ {description}: {str(e)}")
        return False

print("🧪 Quick Feature Tests\n")

# Test Templates
print("📝 Templates:")
test_endpoint("POST", "/api/templates", {"name": "test", "content": "Hello"}, "Create template")
test_endpoint("GET", "/api/templates", None, "List templates")
test_endpoint("GET", "/api/templates/test", None, "Get template")

# Test Reminders
print("\n⏰ Reminders:")
test_endpoint("POST", "/api/reminders", {
    "chat_id": "123",
    "message_id": 1,
    "reminder_time": "2025-12-31T12:00:00",
    "note": "Test"
}, "Create reminder")
test_endpoint("GET", "/api/reminders", None, "List reminders")

# Test Tags
print("\n🏷️  Tags:")
test_endpoint("POST", "/api/messages/123/tags", {"message_id": 123, "tags": ["test", "important"]}, "Add tags")
test_endpoint("GET", "/api/messages/123/tags", None, "Get tags")
test_endpoint("GET", "/api/tags", None, "List all tags")

print("\n✅ Quick tests complete!")

