"""
Test script for Telegram Web App API
Run this to test all endpoints
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8001"

def test_status():
    """Test status endpoint"""
    print("Testing /api/status...")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_chats():
    """Test get chats endpoint"""
    print("\nTesting /api/chats...")
    try:
        response = requests.get(f"{BASE_URL}/api/chats?limit=10")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('chats', []))} chats")
        if data.get('chats'):
            print(f"First chat: {data['chats'][0]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_messages(chat_id):
    """Test get messages endpoint"""
    print(f"\nTesting /api/messages/{chat_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/messages/{chat_id}?limit=5")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('messages', []))} messages")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_send_message(chat_id, message="Test message from API"):
    """Test send message endpoint"""
    print(f"\nTesting /api/messages/send...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/messages/send",
            json={
                "chat_id": chat_id,
                "message": message
            }
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200 and data.get('status') == 'success'
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_account():
    """Test account info endpoint"""
    print("\nTesting /api/account...")
    try:
        response = requests.get(f"{BASE_URL}/api/account")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Account: {data.get('first_name')} {data.get('last_name')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_contacts():
    """Test contacts endpoint"""
    print("\nTesting /api/contacts...")
    try:
        response = requests.get(f"{BASE_URL}/api/contacts")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data.get('contacts', []))} contacts")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Telegram Web App API Test Suite")
    print("=" * 50)
    
    # Test status
    if not test_status():
        print("\n❌ Status check failed. Is the server running?")
        print("Start the server with: python app.py")
        sys.exit(1)
    
    # Test account
    test_account()
    
    # Test chats
    if test_chats():
        # Get first chat ID for testing
        try:
            response = requests.get(f"{BASE_URL}/api/chats?limit=1")
            data = response.json()
            if data.get('chats') and len(data['chats']) > 0:
                first_chat_id = data['chats'][0]['id']
                
                # Test messages
                test_get_messages(first_chat_id)
                
                # Test send message (commented out to avoid spam)
                # test_send_message(first_chat_id, "🧪 API Test Message")
        except Exception as e:
            print(f"Error testing with chat: {e}")
    
    # Test contacts
    test_contacts()
    
    print("\n" + "=" * 50)
    print("✅ Basic tests completed!")
    print("=" * 50)
    print("\nTo test more features:")
    print("1. Open http://localhost:8001 in your browser")
    print("2. Use the web interface to test all features")
    print("3. Check the browser console for WebSocket messages")

if __name__ == "__main__":
    main()

