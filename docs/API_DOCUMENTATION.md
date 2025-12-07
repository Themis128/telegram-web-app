# Telegram Web App API Documentation

Complete API reference for the Telegram Web Application with full MTProto API capabilities.

## Base URL
```
http://localhost:8001
```

## Authentication
Most endpoints require an authenticated Telegram session. Use `/api/authenticate` to authenticate first.

---

## 📋 Table of Contents

1. [Basic Routes](#basic-routes)
2. [Chat Management](#chat-management)
3. [Message Management](#message-management)
4. [File Operations](#file-operations)
5. [Search](#search)
6. [Contacts & Users](#contacts--users)
7. [Account Management](#account-management)
8. [WebSocket](#websocket)

---

## Basic Routes

### GET `/`
Serve the main HTML page.

### GET `/api/status`
Get connection status and user information.

**Response:**
```json
{
  "status": "connected",
  "user": {
    "id": 123456789,
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "phone": "+1234567890"
  }
}
```

### POST `/api/authenticate`
Authenticate with Telegram verification code.

**Request Body:**
```json
{
  "code": "12345",
  "password": "2fa_password" // Optional, only if 2FA is enabled
}
```

**Response:**
```json
{
  "status": "success",
  "user": {
    "id": 123456789,
    "first_name": "John",
    "username": "johndoe"
  }
}
```

---

## Chat Management

### GET `/api/chats`
Get list of all chats/dialogs.

**Query Parameters:**
- `limit` (int, default: 50): Maximum number of chats to return

**Response:**
```json
{
  "chats": [
    {
      "id": "123456789",
      "name": "Chat Name",
      "unread_count": 5,
      "last_message": "Last message text",
      "last_message_date": "2024-01-01T12:00:00",
      "is_group": false,
      "is_channel": false,
      "is_user": true
    }
  ]
}
```

### GET `/api/chats/{chat_id}`
Get detailed chat information.

**Response:**
```json
{
  "id": 123456789,
  "title": "Chat Title",
  "username": "chat_username",
  "is_group": false,
  "is_channel": false,
  "is_user": true,
  "participants_count": 10,
  "about": "Chat description"
}
```

### POST `/api/chats/create-group`
Create a new group.

**Request Body:**
```json
{
  "title": "My Group",
  "users": ["@username1", "@username2", "123456789"]
}
```

**Response:**
```json
{
  "status": "success",
  "group_id": "123456789",
  "group_name": "My Group"
}
```

### POST `/api/chats/create-channel`
Create a new channel or supergroup.

**Request Body:**
```json
{
  "title": "My Channel",
  "about": "Channel description",
  "megagroup": false  // true for supergroup, false for channel
}
```

**Response:**
```json
{
  "status": "success",
  "channel_id": "123456789",
  "channel_name": "My Channel",
  "is_supergroup": false
}
```

### PUT `/api/chats/{chat_id}`
Edit chat information.

**Request Body:**
```json
{
  "title": "New Title",
  "about": "New description"
}
```

### POST `/api/chats/{chat_id}/photo`
Set chat photo.

**Request:** Multipart form data
- `file`: Image file

### GET `/api/chats/{chat_id}/members`
Get chat members list.

**Query Parameters:**
- `limit` (int, default: 100): Maximum number of members

**Response:**
```json
{
  "members": [
    {
      "id": 123456789,
      "first_name": "John",
      "last_name": "Doe",
      "username": "johndoe",
      "is_bot": false
    }
  ],
  "count": 10
}
```

### POST `/api/chats/{chat_id}/members/add`
Add members to chat.

**Request Body:**
```json
{
  "users": ["@username1", "@username2"]
}
```

### POST `/api/chats/{chat_id}/members/remove`
Remove members from chat.

**Request Body:**
```json
{
  "users": ["@username1", "@username2"]
}
```

### GET `/api/chats/{chat_id}/invite-link`
Get or create invite link.

**Response:**
```json
{
  "invite_link": "https://t.me/joinchat/..."
}
```

---

## Message Management

### GET `/api/messages/{chat_id}`
Get messages from a chat.

**Query Parameters:**
- `limit` (int, default: 20): Number of messages to retrieve
- `offset_id` (int, default: 0): Offset message ID for pagination

**Response:**
```json
{
  "messages": [
    {
      "id": 123,
      "text": "Message text",
      "date": "2024-01-01T12:00:00",
      "sender_id": 123456789,
      "is_out": true,
      "is_reply": false,
      "reply_to_msg_id": null,
      "has_media": false,
      "media_type": null
    }
  ]
}
```

### POST `/api/messages/send`
Send a text message.

**Request Body:**
```json
{
  "chat_id": "123456789",
  "message": "Hello!",
  "reply_to": 123,  // Optional: message ID to reply to
  "parse_mode": "md",  // Optional: "md" or "html"
  "silent": false,  // Optional: send silently
  "schedule": "2024-01-01T12:00:00Z"  // Optional: ISO datetime for scheduling
}
```

**Response:**
```json
{
  "status": "success",
  "message_id": 123,
  "text": "Hello!",
  "date": "2024-01-01T12:00:00"
}
```

### POST `/api/messages/send-media`
Send media file (photo, video, document, etc.).

**Request:** Multipart form data
- `chat_id` (string): Chat ID
- `file`: Media file
- `caption` (string, optional): Caption for media
- `voice_note` (bool, optional): Send as voice note
- `video_note` (bool, optional): Send as video note (circular)

**Response:**
```json
{
  "status": "success",
  "message_id": 123,
  "caption": "Media caption",
  "has_media": true
}
```

### POST `/api/messages/send-location`
Send location.

**Request Body:**
```json
{
  "chat_id": "123456789",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "caption": "My location"  // Optional
}
```

### POST `/api/messages/send-contact`
Send contact card.

**Request Body:**
```json
{
  "chat_id": "123456789",
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe"  // Optional
}
```

### PUT `/api/messages/edit`
Edit a message.

**Request Body:**
```json
{
  "chat_id": "123456789",
  "message_id": 123,
  "text": "Edited text"
}
```

### DELETE `/api/messages/delete`
Delete messages.

**Request Body:**
```json
{
  "chat_id": "123456789",
  "message_ids": [123, 124, 125],
  "revoke": false  // Optional: delete for everyone
}
```

**Response:**
```json
{
  "status": "success",
  "deleted_count": 3
}
```

### POST `/api/messages/forward`
Forward messages.

**Request Body:**
```json
{
  "from_chat_id": "123456789",
  "to_chat_id": "987654321",
  "message_ids": [123, 124]
}
```

**Response:**
```json
{
  "status": "success",
  "forwarded_count": 2
}
```

### POST `/api/messages/pin`
Pin or unpin a message.

**Request Body:**
```json
{
  "chat_id": "123456789",
  "message_id": 123,
  "unpin": false  // true to unpin
}
```

### POST `/api/messages/react`
Add or remove reaction to message.

**Request Body:**
```json
{
  "chat_id": "123456789",
  "message_id": 123,
  "reaction": "👍"  // null to remove reaction
}
```

### POST `/api/messages/mark-read`
Mark messages as read.

**Query Parameters:**
- `chat_id` (string): Chat ID
- `message_id` (int, optional): Message ID to mark up to (marks all if not provided)

---

## File Operations

### GET `/api/files/download/{chat_id}/{message_id}`
Download media from a message.

**Response:** File download stream

---

## Search

### POST `/api/search`
Search messages.

**Request Body:**
```json
{
  "chat_id": "123456789",  // Optional: null for global search
  "query": "search keyword",
  "limit": 20  // Optional
}
```

**Response:**
```json
{
  "messages": [
    {
      "id": 123,
      "text": "Message with keyword",
      "date": "2024-01-01T12:00:00",
      "chat_id": "123456789"
    }
  ],
  "count": 10
}
```

---

## Contacts & Users

### GET `/api/contacts`
Get contacts list.

**Response:**
```json
{
  "contacts": [
    {
      "id": 123456789,
      "first_name": "John",
      "last_name": "Doe",
      "username": "johndoe",
      "phone": "+1234567890"
    }
  ]
}
```

### POST `/api/contacts/add`
Add contact.

**Request Body:**
```json
{
  "phone": "+1234567890",
  "first_name": "John",
  "last_name": "Doe"  // Optional
}
```

### DELETE `/api/contacts/{user_id}`
Delete contact.

### GET `/api/users/{user_id}`
Get user information.

**Response:**
```json
{
  "id": 123456789,
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "phone": "+1234567890",
  "is_bot": false,
  "is_verified": false
}
```

### GET `/api/users/{user_id}/photos`
Get user profile photos.

**Query Parameters:**
- `limit` (int, default: 10): Maximum number of photos

**Response:**
```json
{
  "photos": [
    {
      "id": 123,
      "date": "2024-01-01T12:00:00"
    }
  ]
}
```

### POST `/api/users/{user_id}/block`
Block user.

### POST `/api/users/{user_id}/unblock`
Unblock user.

### GET `/api/users/blocked`
Get blocked users list.

**Response:**
```json
{
  "blocked": [
    {
      "id": 123456789,
      "first_name": "John",
      "last_name": "Doe",
      "username": "johndoe"
    }
  ]
}
```

---

## Account Management

### GET `/api/account`
Get own account information.

**Response:**
```json
{
  "id": 123456789,
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "phone": "+1234567890",
  "is_bot": false,
  "is_verified": false,
  "is_premium": false
}
```

### PUT `/api/account/profile`
Update profile information.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",  // Optional
  "about": "Bio text"  // Optional
}
```

### POST `/api/account/photo`
Update profile photo.

**Request:** Multipart form data
- `file`: Image file

### DELETE `/api/account/photo`
Delete profile photo.

---

## WebSocket

### WebSocket `/ws`
Real-time updates via WebSocket.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8001/ws');
```

**Message Types:**

1. **Connected:**
```json
{
  "type": "connected",
  "status": "success",
  "message": "WebSocket connected"
}
```

2. **New Message:**
```json
{
  "type": "new_message",
  "chat_id": "123456789",
  "message": {
    "id": 123,
    "text": "Message text",
    "date": "2024-01-01T12:00:00",
    "sender_id": 123456789,
    "is_out": false
  }
}
```

3. **Message Edited:**
```json
{
  "type": "message_edited",
  "chat_id": "123456789",
  "message": {
    "id": 123,
    "text": "Edited text",
    "date": "2024-01-01T12:00:00"
  }
}
```

4. **Message Deleted:**
```json
{
  "type": "message_deleted",
  "chat_id": "123456789",
  "deleted_ids": [123, 124]
}
```

5. **Chat Action:**
```json
{
  "type": "chat_action",
  "chat_id": "123456789",
  "action": "user_joined"  // or "user_left"
}
```

6. **Ping:**
```json
{
  "type": "ping",
  "status": "alive"
}
```

---

## Error Responses

All endpoints may return error responses:

**503 Service Unavailable:**
```json
{
  "detail": "Not connected to Telegram"
}
```

**404 Not Found:**
```json
{
  "detail": "Entity not found: ..."
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error message"
}
```

**400 Bad Request:**
```json
{
  "detail": "Error message"
}
```

---

## Notes

1. **Chat ID Format:** Chat IDs can be:
   - Integer ID: `123456789`
   - Username: `@username`
   - Phone number: `+1234567890`

2. **File Uploads:** Use `multipart/form-data` for file uploads.

3. **Real-time Updates:** Connect to WebSocket endpoint for real-time message and event updates.

4. **Rate Limiting:** Be mindful of Telegram's rate limits. The API handles some rate limiting automatically.

5. **Authentication:** Most endpoints require an authenticated session. Use `/api/authenticate` first.

---

## Example Usage

### Send a message:
```bash
curl -X POST http://localhost:8001/api/messages/send \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "123456789",
    "message": "Hello from API!"
  }'
```

### Send a photo:
```bash
curl -X POST http://localhost:8001/api/messages/send-media \
  -F "chat_id=123456789" \
  -F "file=@photo.jpg" \
  -F "caption=My photo"
```

### Get chats:
```bash
curl http://localhost:8001/api/chats?limit=20
```

---

*Last Updated: Based on app.py v2.0.0*
