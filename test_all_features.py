#!/usr/bin/env python3
"""
Comprehensive Test Suite for All Features
Tests automation, security, custom features, and integrations
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_URL", "http://localhost:8001")
API_KEY = os.getenv("API_KEY", None)

def get_headers():
    """Get request headers"""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    return headers

def log_test(feature, success, message=""):
    """Log test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {feature} - {message}")

def test_api_status():
    """Test API status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/status", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            log_test("API Status", True, f"Status: {data.get('status')}")
            return True, data
        else:
            log_test("API Status", False, f"HTTP {response.status_code}")
            return False, None
    except Exception as e:
        log_test("API Status", False, str(e))
        return False, None

def test_security_rate_limit():
    """Test rate limiting"""
    print("\n🔒 Testing Security Features...")
    try:
        # Make rapid requests to trigger rate limit
        for i in range(105):  # Exceed default limit of 100
            response = requests.get(f"{BASE_URL}/api/status", headers=get_headers(), timeout=5)
            if response.status_code == 429:
                log_test("Rate Limiting", True, f"Rate limit triggered after {i+1} requests")
                return True
        log_test("Rate Limiting", False, "Rate limit not triggered (may be disabled)")
        return False
    except Exception as e:
        log_test("Rate Limiting", False, str(e))
        return False

def test_templates():
    """Test message templates"""
    print("\n📝 Testing Message Templates...")
    try:
        # Create template
        template_data = {
            "name": "test_greeting",
            "content": "Hello! This is a test template."
        }
        response = requests.post(
            f"{BASE_URL}/api/templates",
            headers=get_headers(),
            json=template_data,
            timeout=10
        )
        if response.status_code == 200:
            log_test("Create Template", True, "Template created")
        else:
            log_test("Create Template", False, f"HTTP {response.status_code}")
            return False
        
        # List templates
        response = requests.get(f"{BASE_URL}/api/templates", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            templates = data.get("templates", [])
            if "test_greeting" in templates:
                log_test("List Templates", True, f"Found {len(templates)} templates")
            else:
                log_test("List Templates", False, "Template not found in list")
                return False
        else:
            log_test("List Templates", False, f"HTTP {response.status_code}")
            return False
        
        # Get template
        response = requests.get(f"{BASE_URL}/api/templates/test_greeting", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("content") == template_data["content"]:
                log_test("Get Template", True, "Template retrieved correctly")
            else:
                log_test("Get Template", False, "Template content mismatch")
                return False
        else:
            log_test("Get Template", False, f"HTTP {response.status_code}")
            return False
        
        return True
    except Exception as e:
        log_test("Templates", False, str(e))
        return False

def test_reminders():
    """Test message reminders"""
    print("\n⏰ Testing Message Reminders...")
    try:
        # Create reminder
        reminder_data = {
            "chat_id": "123456789",  # Test chat ID
            "message_id": 1,
            "reminder_time": "2025-12-31T12:00:00",
            "note": "Test reminder"
        }
        response = requests.post(
            f"{BASE_URL}/api/reminders",
            headers=get_headers(),
            json=reminder_data,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            reminder_id = data.get("reminder_id")
            log_test("Create Reminder", True, f"Reminder ID: {reminder_id}")
        else:
            log_test("Create Reminder", False, f"HTTP {response.status_code}")
            return False
        
        # List reminders
        response = requests.get(f"{BASE_URL}/api/reminders", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            reminders = data.get("reminders", [])
            log_test("List Reminders", True, f"Found {len(reminders)} reminders")
            return True
        else:
            log_test("List Reminders", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("Reminders", False, str(e))
        return False

def test_tags():
    """Test message tags"""
    print("\n🏷️  Testing Message Tags...")
    try:
        # Add tags
        tag_data = {
            "message_id": 123,
            "tags": ["important", "work", "test"]
        }
        response = requests.post(
            f"{BASE_URL}/api/messages/123/tags",
            headers=get_headers(),
            json=tag_data,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            tags = data.get("tags", [])
            if "important" in tags and "work" in tags:
                log_test("Add Tags", True, f"Tags added: {tags}")
            else:
                log_test("Add Tags", False, "Tags not added correctly")
                return False
        else:
            log_test("Add Tags", False, f"HTTP {response.status_code}")
            return False
        
        # Get tags
        response = requests.get(f"{BASE_URL}/api/messages/123/tags", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            tags = data.get("tags", [])
            if len(tags) >= 3:
                log_test("Get Tags", True, f"Retrieved {len(tags)} tags")
            else:
                log_test("Get Tags", False, "Tags not retrieved correctly")
                return False
        else:
            log_test("Get Tags", False, f"HTTP {response.status_code}")
            return False
        
        # List all tags
        response = requests.get(f"{BASE_URL}/api/tags", headers=get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            all_tags = data.get("tags", [])
            log_test("List All Tags", True, f"Found {len(all_tags)} unique tags")
            return True
        else:
            log_test("List All Tags", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        log_test("Tags", False, str(e))
        return False

def test_automation_scripts():
    """Test automation scripts (check if they can be imported)"""
    print("\n🤖 Testing Automation Scripts...")
    results = []
    
    scripts = [
        "scripts/auto_responder.py",
        "scripts/message_forwarder.py",
        "scripts/backup_messages.py"
    ]
    
    for script in scripts:
        try:
            if os.path.exists(script):
                # Try to compile the script
                with open(script, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, script, 'exec')
                log_test(f"Script: {script}", True, "Script is valid Python")
                results.append(True)
            else:
                log_test(f"Script: {script}", False, "File not found")
                results.append(False)
        except SyntaxError as e:
            log_test(f"Script: {script}", False, f"Syntax error: {e}")
            results.append(False)
        except Exception as e:
            log_test(f"Script: {script}", False, str(e))
            results.append(False)
    
    return all(results)

def test_integrations():
    """Test integration templates"""
    print("\n🔌 Testing Integration Templates...")
    try:
        if os.path.exists("integrations/webhook_handler.py"):
            with open("integrations/webhook_handler.py", 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, "integrations/webhook_handler.py", 'exec')
            log_test("Webhook Handler", True, "Integration template is valid")
            return True
        else:
            log_test("Webhook Handler", False, "File not found")
            return False
    except Exception as e:
        log_test("Webhook Handler", False, str(e))
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 COMPREHENSIVE FEATURE TEST SUITE")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print()
    
    results = {}
    
    # Test API status first
    status_ok, status_data = test_api_status()
    if not status_ok:
        print("\n❌ API is not accessible. Make sure the server is running!")
        print("   Start server with: npm start")
        return
    
    # Test security features
    results["rate_limit"] = test_security_rate_limit()
    
    # Test custom features
    results["templates"] = test_templates()
    results["reminders"] = test_reminders()
    results["tags"] = test_tags()
    
    # Test automation scripts
    results["automation"] = test_automation_scripts()
    
    # Test integrations
    results["integrations"] = test_integrations()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for feature, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {feature.replace('_', ' ').title()}")
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

