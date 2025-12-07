#!/usr/bin/env python3
"""
Webhook Handler
Receives webhooks from external services and forwards to Telegram.
"""

from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_API_URL = os.getenv("TELEGRAM_API_URL", "http://localhost:8001")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY", None)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key")

# Mapping: webhook_source -> telegram_chat_id
CHAT_MAPPINGS = {
    "github": "123456789",  # GitHub webhooks -> Telegram chat
    "slack": "987654321",   # Slack webhooks -> Telegram chat
    "jira": "456789123",    # Jira webhooks -> Telegram chat
}


def get_headers():
    """Get request headers for Telegram API"""
    headers = {"Content-Type": "application/json"}
    if TELEGRAM_API_KEY:
        headers["X-API-Key"] = TELEGRAM_API_KEY
    return headers


def send_to_telegram(chat_id: str, message: str):
    """Send message to Telegram"""
    try:
        response = requests.post(
            f"{TELEGRAM_API_URL}/api/messages/send",
            headers=get_headers(),
            json={"chat_id": chat_id, "message": message},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return False


@app.route('/webhook/<source>', methods=['POST'])
def handle_webhook(source: str):
    """Handle webhook from external service"""
    # Verify secret (optional)
    secret = request.headers.get('X-Webhook-Secret')
    if WEBHOOK_SECRET and secret != WEBHOOK_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    # Get chat ID for this source
    chat_id = CHAT_MAPPINGS.get(source)
    if not chat_id:
        return jsonify({"error": "Source not configured"}), 404

    # Process webhook data
    data = request.get_json() or {}

    # Format message based on source
    if source == "github":
        message = format_github_webhook(data)
    elif source == "slack":
        message = format_slack_webhook(data)
    elif source == "jira":
        message = format_jira_webhook(data)
    else:
        message = f"Webhook from {source}:\n{json.dumps(data, indent=2)}"

    # Send to Telegram
    if send_to_telegram(chat_id, message):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Failed to send to Telegram"}), 500


def format_github_webhook(data: dict) -> str:
    """Format GitHub webhook data"""
    action = data.get("action", "")
    repo = data.get("repository", {}).get("full_name", "Unknown")

    if "pull_request" in data:
        pr = data["pull_request"]
        return f"🔀 GitHub PR {action}\n\nRepo: {repo}\nPR: #{pr.get('number')} {pr.get('title')}\nAuthor: {pr.get('user', {}).get('login')}\nURL: {pr.get('html_url')}"

    if "issue" in data:
        issue = data["issue"]
        return f"📝 GitHub Issue {action}\n\nRepo: {repo}\nIssue: #{issue.get('number')} {issue.get('title')}\nAuthor: {issue.get('user', {}).get('login')}\nURL: {issue.get('html_url')}"

    if "push" in data:
        commits = data.get("commits", [])
        return f"📤 GitHub Push\n\nRepo: {repo}\nCommits: {len(commits)}\nBranch: {data.get('ref', '').replace('refs/heads/', '')}"

    return f"GitHub Webhook: {action}\nRepo: {repo}"


def format_slack_webhook(data: dict) -> str:
    """Format Slack webhook data"""
    text = data.get("text", "")
    user = data.get("user_name", "Unknown")
    channel = data.get("channel_name", "Unknown")

    return f"💬 Slack Message\n\nChannel: #{channel}\nUser: {user}\nMessage: {text}"


def format_jira_webhook(data: dict) -> str:
    """Format Jira webhook data"""
    issue = data.get("issue", {})
    webhook_event = data.get("webhookEvent", "")

    return f"🎫 Jira {webhook_event}\n\nIssue: {issue.get('key')} - {issue.get('fields', {}).get('summary')}\nStatus: {issue.get('fields', {}).get('status', {}).get('name')}"


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    port = int(os.getenv("WEBHOOK_PORT", 5000))
    print(f"🌐 Webhook Handler starting on port {port}")
    print(f"Telegram API: {TELEGRAM_API_URL}")
    print(f"Configured sources: {list(CHAT_MAPPINGS.keys())}")
    app.run(host='0.0.0.0', port=port, debug=True)
