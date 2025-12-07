# Telethon Full MTProto API Capabilities Guide

## What This Means for Your Project

Your project uses **Telethon**, which is a Python library that provides **full access to Telegram's MTProto API**. This means you have access to **ALL** features available to regular Telegram users, not just the limited Bot API features.

### Current Implementation

Your `app.py` currently implements:
- ✅ Basic authentication
- ✅ Get chats/dialogs
- ✅ Get messages
- ✅ Send text messages
- ✅ Connection status

### What You Can Add

Since you're using Telethon, you can add **ANY** feature that the official Telegram app has:

---

## Complete Telethon Method Reference

### 📱 Messaging Capabilities

#### Send Messages
```python
# Text message
await client.send_message(entity, "Hello!")

# With formatting
await client.send_message(entity, "**Bold** and *italic*", parse_mode='md')

# Reply to specific message
await client.send_message(entity, "Reply", reply_to=message_id)

# Schedule message
await client.send_message(entity, "Scheduled", schedule=datetime.now() + timedelta(hours=1))

# Silent message
await client.send_message(entity, "Silent", silent=True)

# With buttons
from telethon import Button
await client.send_message(entity, "Choose:", buttons=[
    [Button.inline("Option 1", b"opt1"), Button.inline("Option 2", b"opt2")]
])
```

#### Send Media
```python
# Photo
await client.send_file(entity, 'photo.jpg', caption="My photo")

# Video
await client.send_file(entity, 'video.mp4', caption="My video")

# Document
await client.send_file(entity, 'document.pdf', caption="My document")

# Audio
await client.send_file(entity, 'audio.mp3', voice_note=True)

# Voice message
await client.send_file(entity, 'voice.ogg', voice_note=True)

# Video note (circular)
await client.send_file(entity, 'video_note.mp4', video_note=True)

# Location
await client.send_file(entity, file=types.InputMediaGeoPoint(
    types.InputGeoPoint(lat=37.7749, long=-122.4194)
))

# Contact
await client.send_contact(entity, phone="+1234567890", first_name="John")

# Poll
await client.send_file(entity, file=types.InputMediaPoll(
    poll=types.Poll(
        id=123,
        question="Favorite color?",
        answers=[
            types.PollAnswer(text="Red", option=b"red"),
            types.PollAnswer(text="Blue", option=b"blue")
        ]
    )
))
```

#### Edit Messages
```python
# Edit text
await client.edit_message(entity, message_id, "Edited text")

# Edit media caption
await client.edit_message(entity, message_id, file='new_photo.jpg', text="New caption")
```

#### Delete Messages
```python
# Delete single message
await client.delete_messages(entity, message_id)

# Delete multiple messages
await client.delete_messages(entity, [msg1_id, msg2_id, msg3_id])

# Delete for everyone (revoke)
await client.delete_messages(entity, message_id, revoke=True)
```

#### Forward Messages
```python
# Forward single message
await client.forward_messages(target_entity, message_id, from_peer=source_entity)

# Forward multiple
await client.forward_messages(target_entity, [msg1, msg2], from_peer=source_entity)
```

#### Pin Messages
```python
# Pin message
await client.pin_message(entity, message_id)

# Unpin
await client.unpin_message(entity)

# Unpin specific message
await client.unpin_message(entity, message_id)
```

#### Message Reactions
```python
# Add reaction
await client.send_reaction(entity, message_id, reaction="👍")

# Remove reaction
await client.send_reaction(entity, message_id, reaction=None)
```

#### Read Messages
```python
# Mark as read
await client.send_read_acknowledge(entity, max_id=message_id)

# Mark entire chat as read
await client.send_read_acknowledge(entity)
```

---

### 💬 Chat Management

#### Get Chats
```python
# Get all dialogs
dialogs = await client.get_dialogs(limit=100)

# Get specific chat
chat = await client.get_entity('username')
chat = await client.get_entity(chat_id)
chat = await client.get_entity('+1234567890')  # Phone number

# Get chat history
messages = await client.get_messages(entity, limit=50)

# Iterate messages (memory efficient)
async for message in client.iter_messages(entity, limit=100):
    print(message.text)
```

#### Create Chats
```python
# Create group
group = await client.create_group("My Group", users=['user1', 'user2'])

# Create channel
channel = await client.create_channel("My Channel", "Channel description", megagroup=False)

# Create supergroup
supergroup = await client.create_channel("My Supergroup", megagroup=True)
```

#### Edit Chat Info
```python
# Edit title
await client.edit_title(entity, "New Title")

# Edit about/description
await client.edit_admin(entity, about="New description")

# Change photo
await client.edit_photo(entity, 'new_photo.jpg')
```

#### Manage Members
```python
# Add members
await client.add_participants(entity, ['user1', 'user2'])

# Remove members
await client.delete_participants(entity, ['user1'])

# Get participants
participants = await client.get_participants(entity)

# Get admins
admins = await client.get_participants(entity, filter=types.ChannelParticipantsAdmins)
```

#### Chat Permissions
```python
from telethon.tl.types import ChatBannedRights

# Set default banned rights
rights = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

await client.edit_admin(entity, user, change_info=False, post_messages=True,
                       edit_messages=True, delete_messages=True, ban_users=True,
                       invite_users=True, pin_messages=True, add_admins=True)
```

#### Invite Links
```python
# Create invite link
link = await client.export_chat_invite_link(entity)

# Get invite links
links = await client.get_admin_log(entity, events_filter=types.ChannelAdminLogEventsFilter())

# Revoke invite link
await client.revoke_chat_invite_link(entity, invite_link)
```

---

### 👤 User & Contact Management

#### Get User Info
```python
# Get own info
me = await client.get_me()

# Get user info
user = await client.get_entity('username')
user = await client.get_entity(user_id)

# Get profile photos
photos = await client.get_profile_photos(user)

# Download profile photo
await client.download_profile_photo(user, file='profile.jpg')
```

#### Contacts
```python
# Get contacts
contacts = await client.get_contacts()

# Add contact
await client.add_contact(user, first_name="John", last_name="Doe", phone="+1234567890")

# Delete contact
await client.delete_contacts([user])

# Import contacts
from telethon.tl.types import InputPhoneContact
contacts = [InputPhoneContact(client_id=0, phone="+1234567890", first_name="John", last_name="Doe")]
result = await client.import_contacts(contacts)
```

#### Block/Unblock
```python
# Block user
await client.block(user)

# Unblock user
await client.unblock(user)

# Get blocked users
blocked = await client.get_blocked()
```

---

### 📁 File Operations

#### Upload Files
```python
# Upload file
file = await client.upload_file('large_file.zip')

# Upload with progress
async def callback(current, total):
    print(f'Uploaded {current}/{total}')

file = await client.upload_file('file.zip', progress_callback=callback)

# Upload to specific DC
file = await client.upload_file('file.zip', file_size=1024*1024, dc_id=2)
```

#### Download Files
```python
# Download media
await client.download_media(message, file='downloaded_file.jpg')

# Download with progress
async def callback(current, total):
    print(f'Downloaded {current}/{total}')

await client.download_media(message, file='file.jpg', progress_callback=callback)

# Download to memory
file_bytes = await client.download_media(message, file=bytes)
```

---

### 📞 Calls (if supported)

```python
# Note: Voice/Video calls require additional setup
# This is a complex feature that may need additional libraries
```

---

### 📸 Stories

```python
# Upload story
story = await client.send_file('@me', 'photo.jpg',
                              file=types.InputMediaUploadedPhoto(
                                  file=await client.upload_file('photo.jpg')
                              ))

# Get stories
stories = await client.get_stories(user)
```

---

### 🔍 Search

```python
# Search messages
messages = await client.get_messages(entity, search="keyword", limit=10)

# Search globally
results = await client.get_messages(None, search="keyword", limit=10)

# Search by user
messages = await client.get_messages(entity, from_user=user, limit=10)
```

---

### 🔐 Secret Chats

```python
# Create secret chat
secret_chat = await client.create_secret_chat(user)

# Send message in secret chat
await client.send_message(secret_chat, "Secret message")

# Note: Secret chats have end-to-end encryption
```

---

### 📊 Channel Statistics

```python
# Get channel stats (requires admin rights)
stats = await client.get_stats(entity)

# Get message stats
message_stats = await client.get_stats(entity, message_id=123)
```

---

### 🎯 Event Handlers

```python
# Handle new messages
@client.on(events.NewMessage)
async def handler(event):
    print(f"New message: {event.message.text}")

# Handle edited messages
@client.on(events.MessageEdited)
async def handler(event):
    print(f"Message edited: {event.message.text}")

# Handle deleted messages
@client.on(events.MessageDeleted)
async def handler(event):
    print(f"Message deleted: {event.deleted_ids}")

# Handle user updates
@client.on(events.UserUpdate)
async def handler(event):
    print(f"User updated: {event}")

# Handle chat actions (typing, recording, etc.)
@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        print(f"{event.user_id} joined")
    elif event.user_left:
        print(f"{event.user_id} left")

# Handle callback queries (button clicks)
@client.on(events.CallbackQuery)
async def handler(event):
    await event.answer("Button clicked!")
```

---

### ⚙️ Settings & Preferences

#### Privacy Settings
```python
from telethon.tl.functions.account import SetPrivacyRequest
from telethon.tl.types import InputPrivacyValueAllowAll, InputPrivacyValueDisallowAll

# Set last seen privacy
await client(SetPrivacyRequest(
    key=types.InputPrivacyKeyStatusTimestamp(),
    rules=[InputPrivacyValueAllowAll()]
))
```

#### Account Settings
```python
# Update profile
await client.update_profile(first_name="New", last_name="Name", about="Bio")

# Update username
await client.update_username("newusername")

# Update profile photo
await client.upload_profile_photo('photo.jpg')

# Delete profile photo
photos = await client.get_profile_photos('me')
await client.delete_photos(photos)
```

---

### 📋 Advanced Features

#### Message Threading
```python
# Reply in thread
await client.send_message(entity, "Reply", reply_to=message_id,
                         reply_to_msg_id=thread_root_id)
```

#### Scheduled Messages
```python
from datetime import datetime, timedelta

# Schedule for later
await client.send_message(entity, "Scheduled",
                         schedule=datetime.now() + timedelta(hours=1))
```

#### Message Effects
```python
# Add effect (if available)
await client.send_message(entity, "Message", effect=types.MessageEffect())
```

#### Link Previews
```python
# Send with link preview
await client.send_message(entity, "Check https://example.com",
                         link_preview=True)

# Disable link preview
await client.send_message(entity, "Check https://example.com",
                         link_preview=False)
```

---

## Adding These to Your FastAPI App

### Example: Add Media Upload Endpoint

```python
from fastapi import UploadFile, File
from telethon.tl.types import InputMediaUploadedPhoto

@app.post("/api/send-media")
async def send_media(
    chat_id: str,
    file: UploadFile = File(...),
    caption: str = None
):
    """Send media file"""
    global client

    if client is None or not client.is_connected():
        raise HTTPException(status_code=503, detail="Not connected")

    try:
        # Save uploaded file temporarily
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Send file
        entity = await client.get_entity(int(chat_id))
        message = await client.send_file(entity, file_path, caption=caption)

        # Clean up
        os.remove(file_path)

        return {
            "status": "success",
            "message_id": message.id,
            "media_type": "file"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Example: Add Message Reactions

```python
@app.post("/api/react")
async def react_to_message(
    chat_id: str,
    message_id: int,
    reaction: str
):
    """Add reaction to message"""
    global client

    if client is None or not client.is_connected():
        raise HTTPException(status_code=503, detail="Not connected")

    try:
        entity = await client.get_entity(int(chat_id))
        await client.send_reaction(entity, message_id, reaction=reaction)

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Example: Add Chat Management

```python
@app.post("/api/create-group")
async def create_group(name: str, users: List[str]):
    """Create a new group"""
    global client

    if client is None or not client.is_connected():
        raise HTTPException(status_code=503, detail="Not connected")

    try:
        # Resolve user entities
        user_entities = []
        for user in users:
            entity = await client.get_entity(user)
            user_entities.append(entity)

        group = await client.create_group(name, users=user_entities)

        return {
            "status": "success",
            "group_id": group.id,
            "group_name": group.title
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Example: Real-time Event Handling

```python
import asyncio
from telethon import events

# Start event handler in background
async def start_event_handler():
    global client
    if client:
        @client.on(events.NewMessage)
        async def new_message_handler(event):
            # Process new messages
            print(f"New message: {event.message.text}")
            # You could emit this via WebSocket to frontend

        # Keep running
        await client.run_until_disconnected()

# Start in background on app startup
@app.on_event("startup")
async def startup_event():
    # ... existing code ...
    asyncio.create_task(start_event_handler())
```

---

## Complete Method List

### Core Methods
- `client.connect()` - Connect to Telegram
- `client.disconnect()` - Disconnect
- `client.is_connected()` - Check connection
- `client.get_me()` - Get own user info
- `client.get_entity()` - Get any entity (user/chat/channel)

### Messaging
- `client.send_message()` - Send text message
- `client.send_file()` - Send media
- `client.edit_message()` - Edit message
- `client.delete_messages()` - Delete messages
- `client.forward_messages()` - Forward messages
- `client.pin_message()` - Pin message
- `client.unpin_message()` - Unpin message
- `client.send_reaction()` - Add reaction
- `client.send_read_acknowledge()` - Mark as read
- `client.get_messages()` - Get messages
- `client.iter_messages()` - Iterate messages
- `client.search_messages()` - Search messages

### Chats
- `client.get_dialogs()` - Get all chats
- `client.create_group()` - Create group
- `client.create_channel()` - Create channel
- `client.edit_title()` - Edit chat title
- `client.edit_photo()` - Change chat photo
- `client.add_participants()` - Add members
- `client.delete_participants()` - Remove members
- `client.get_participants()` - Get members
- `client.edit_admin()` - Edit admin permissions
- `client.export_chat_invite_link()` - Create invite link

### Users & Contacts
- `client.get_contacts()` - Get contacts
- `client.add_contact()` - Add contact
- `client.delete_contacts()` - Delete contact
- `client.import_contacts()` - Import contacts
- `client.get_profile_photos()` - Get profile photos
- `client.block()` - Block user
- `client.unblock()` - Unblock user
- `client.get_blocked()` - Get blocked users

### Files
- `client.upload_file()` - Upload file
- `client.download_media()` - Download media
- `client.download_profile_photo()` - Download profile photo

### Account
- `client.update_profile()` - Update profile
- `client.update_username()` - Update username
- `client.upload_profile_photo()` - Update profile photo
- `client.delete_photos()` - Delete profile photos

### Advanced
- `client.create_secret_chat()` - Create secret chat
- `client.get_stats()` - Get channel stats
- `client.get_stories()` - Get stories
- `client.send_code_request()` - Request auth code
- `client.sign_in()` - Sign in
- `client.sign_up()` - Sign up

---

## Resources

- **Telethon Documentation**: https://docs.telethon.dev/
- **Telethon Examples**: https://github.com/LonamiWebs/Telethon/tree/master/telethon_examples
- **Telegram API Schema**: https://core.telegram.org/schema
- **MTProto API Docs**: https://core.telegram.org/api

---

## Next Steps

1. **Review your current implementation** in `app.py`
2. **Choose features** you want to add from this guide
3. **Implement endpoints** using the examples above
4. **Test thoroughly** before deploying
5. **Handle errors** gracefully (rate limits, permissions, etc.)

---

*This guide covers the major capabilities. Telethon has access to 100+ API methods. Refer to the official documentation for complete reference.*
