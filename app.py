"""
Telegram Web Application
A modern web interface for Telegram using Telethon with full MTProto API capabilities
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
import tempfile
import shutil
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
from telethon.errors import SessionPasswordNeededError
from telethon.tl import types
from telethon.tl.types import InputPhoneContact
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from datetime import datetime, timedelta
import io

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    try:
        result = await init_client()
        print(f"Telegram client: {result}")
        if result.get("status") == "connected":
            await setup_event_handlers()
    except Exception as e:
        print(f"Error initializing client: {e}")

    yield

    # Shutdown
    global client
    if client:
        await client.disconnect()
        print("Telegram client disconnected")

app = FastAPI(
    title="Telegram Web App - Full API",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global client instance
client: Optional[TelegramClient] = None
websocket_connections: List[WebSocket] = []

# ============================================================================
# Pydantic Models
# ============================================================================

class MessageRequest(BaseModel):
    chat_id: str
    message: str
    reply_to: Optional[int] = None
    parse_mode: Optional[str] = None
    silent: Optional[bool] = False
    schedule: Optional[str] = None  # ISO datetime string

class EditMessageRequest(BaseModel):
    chat_id: str
    message_id: int
    text: str

class DeleteMessageRequest(BaseModel):
    chat_id: str
    message_ids: List[int]
    revoke: Optional[bool] = False

class ForwardMessageRequest(BaseModel):
    from_chat_id: str
    to_chat_id: str
    message_ids: List[int]

class PinMessageRequest(BaseModel):
    chat_id: str
    message_id: int
    unpin: Optional[bool] = False

class ReactionRequest(BaseModel):
    chat_id: str
    message_id: int
    reaction: Optional[str] = None  # None to remove reaction

class CreateGroupRequest(BaseModel):
    title: str
    users: List[str]  # List of usernames or user IDs

class CreateChannelRequest(BaseModel):
    title: str
    about: Optional[str] = None
    megagroup: Optional[bool] = False

class EditChatRequest(BaseModel):
    chat_id: str
    title: Optional[str] = None
    about: Optional[str] = None

class AddMembersRequest(BaseModel):
    chat_id: str
    users: List[str]

class RemoveMembersRequest(BaseModel):
    chat_id: str
    users: List[str]

class ContactRequest(BaseModel):
    phone: str
    first_name: str
    last_name: Optional[str] = None

class SearchRequest(BaseModel):
    chat_id: Optional[str] = None  # None for global search
    query: str
    limit: Optional[int] = 20

class UpdateProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    about: Optional[str] = None

class LocationRequest(BaseModel):
    chat_id: str
    latitude: float
    longitude: float
    caption: Optional[str] = None

class ContactMessageRequest(BaseModel):
    chat_id: str
    phone: str
    first_name: str
    last_name: Optional[str] = None

# ============================================================================
# Helper Functions
# ============================================================================

def check_client_connected():
    """Check if client is connected"""
    if client is None or not client.is_connected():
        raise HTTPException(status_code=503, detail="Not connected to Telegram")

async def get_entity_safe(identifier: str):
    """Safely get entity from identifier (ID, username, or phone)"""
    try:
        # Try as integer ID first
        if identifier.isdigit() or (identifier.startswith('-') and identifier[1:].isdigit()):
            return await client.get_entity(int(identifier))
        # Try as username
        elif identifier.startswith('@'):
            return await client.get_entity(identifier)
        # Try as phone number
        elif identifier.startswith('+'):
            return await client.get_entity(identifier)
        else:
            # Try as integer
            return await client.get_entity(int(identifier))
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Entity not found: {str(e)}")

async def broadcast_to_websockets(data: dict):
    """Broadcast data to all connected WebSocket clients"""
    disconnected = []
    for ws in websocket_connections:
        try:
            await ws.send_json(data)
        except:
            disconnected.append(ws)

    # Remove disconnected clients
    for ws in disconnected:
        if ws in websocket_connections:
            websocket_connections.remove(ws)

# ============================================================================
# Client Initialization
# ============================================================================

async def init_client():
    """Initialize Telegram client"""
    global client

    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    phone = os.getenv("TELEGRAM_PHONE_NUMBER")

    if not all([api_id, api_hash, phone]):
        raise ValueError("Missing Telegram credentials in .env file")

    # Store session files in data directory
    os.makedirs("data", exist_ok=True)
    session_name = f"data/telegram_session_{phone.replace('+', '')}"
    client = TelegramClient(session_name, int(api_id), api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        return {"status": "not_authorized", "message": "Please run scripts/auth_cli.py first to authenticate"}

    return {"status": "connected", "message": "Successfully connected to Telegram"}

async def setup_event_handlers():
    """Setup Telegram event handlers for real-time updates"""
    if not client or not client.is_connected():
        return

    @client.on(events.NewMessage)
    async def new_message_handler(event):
        """Handle new messages"""
        try:
            message_data = {
                "type": "new_message",
                "chat_id": str(event.chat_id),
                "message": {
                    "id": event.message.id,
                    "text": event.message.text or "",
                    "date": event.message.date.isoformat() if event.message.date else None,
                    "sender_id": event.message.sender_id if hasattr(event.message, 'sender_id') else None,
                    "is_out": event.message.out if hasattr(event.message, 'out') else False
                }
            }
            await broadcast_to_websockets(message_data)
        except Exception as e:
            print(f"Error in new_message_handler: {e}")

    @client.on(events.MessageEdited)
    async def message_edited_handler(event):
        """Handle edited messages"""
        try:
            message_data = {
                "type": "message_edited",
                "chat_id": str(event.chat_id),
                "message": {
                    "id": event.message.id,
                    "text": event.message.text or "",
                    "date": event.message.date.isoformat() if event.message.date else None
                }
            }
            await broadcast_to_websockets(message_data)
        except Exception as e:
            print(f"Error in message_edited_handler: {e}")

    @client.on(events.MessageDeleted)
    async def message_deleted_handler(event):
        """Handle deleted messages"""
        try:
            message_data = {
                "type": "message_deleted",
                "chat_id": str(event.chat_id),
                "deleted_ids": event.deleted_ids
            }
            await broadcast_to_websockets(message_data)
        except Exception as e:
            print(f"Error in message_deleted_handler: {e}")

    @client.on(events.ChatAction)
    async def chat_action_handler(event):
        """Handle chat actions (user joined, left, etc.)"""
        try:
            action_data = {
                "type": "chat_action",
                "chat_id": str(event.chat_id),
                "action": "user_joined" if event.user_joined else "user_left" if event.user_left else "unknown"
            }
            await broadcast_to_websockets(action_data)
        except Exception as e:
            print(f"Error in chat_action_handler: {e}")

# ============================================================================
# Basic Routes
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/manifest.json")
async def get_manifest():
    """Serve PWA manifest"""
    with open("manifest.json", "r", encoding="utf-8") as f:
        return JSONResponse(content=json.load(f))

@app.get("/sw.js")
async def get_service_worker():
    """Serve service worker"""
    with open("sw.js", "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="application/javascript")

@app.get("/icon-192.png")
async def get_icon_192():
    """Serve 192x192 icon - returns placeholder if not found"""
    if os.path.exists("icon-192.png"):
        return FileResponse("icon-192.png", media_type="image/png")
    else:
        # Return a simple SVG placeholder
        svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="192" height="192" viewBox="0 0 192 192">
            <rect width="192" height="192" fill="#3390ec"/>
            <text x="96" y="120" font-size="80" fill="white" text-anchor="middle" font-family="Arial">T</text>
        </svg>'''
        return Response(content=svg, media_type="image/svg+xml")

@app.get("/icon-512.png")
async def get_icon_512():
    """Serve 512x512 icon - returns placeholder if not found"""
    if os.path.exists("icon-512.png"):
        return FileResponse("icon-512.png", media_type="image/png")
    else:
        # Return a simple SVG placeholder
        svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
            <rect width="512" height="512" fill="#3390ec"/>
            <text x="256" y="320" font-size="200" fill="white" text-anchor="middle" font-family="Arial">T</text>
        </svg>'''
        return Response(content=svg, media_type="image/svg+xml")

@app.get("/api/status")
async def get_status():
    """Get connection status"""
    global client

    if client is None:
        return {"status": "disconnected", "message": "Client not initialized"}

    if client.is_connected():
        try:
            me = await client.get_me()
            return {
                "status": "connected",
                "user": {
                    "id": me.id,
                    "first_name": me.first_name,
                    "last_name": me.last_name or "",
                    "username": me.username or "",
                    "phone": me.phone or ""
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    else:
        return {"status": "disconnected", "message": "Not connected to Telegram"}

@app.post("/api/authenticate")
async def authenticate(request: Request):
    """Authenticate with code"""
    global client

    data = await request.json()
    code = data.get("code")
    password = data.get("password")

    if not code:
        raise HTTPException(status_code=400, detail="Code is required")

    try:
        api_id = os.getenv("TELEGRAM_API_ID")
        api_hash = os.getenv("TELEGRAM_API_HASH")
        phone = os.getenv("TELEGRAM_PHONE_NUMBER")

        # Store session files in data directory
        os.makedirs("data", exist_ok=True)
        session_name = f"data/telegram_session_{phone.replace('+', '')}"
        client = TelegramClient(session_name, int(api_id), api_hash)
        await client.connect()

        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            if not password:
                return {"status": "password_required", "message": "2FA password required"}
            await client.sign_in(password=password)

        me = await client.get_me()
        await setup_event_handlers()

        return {
            "status": "success",
            "user": {
                "id": me.id,
                "first_name": me.first_name,
                "username": me.username or ""
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# Chat Management
# ============================================================================

@app.get("/api/chats")
async def get_chats(limit: int = 50):
    """Get list of chats"""
    check_client_connected()

    try:
        dialogs = await client.get_dialogs(limit=limit)
        chats = []

        for dialog in dialogs:
            chat_info = {
                "id": str(dialog.id),
                "name": dialog.name,
                "unread_count": dialog.unread_count,
                "last_message": None,
                "is_group": dialog.is_group,
                "is_channel": dialog.is_channel,
                "is_user": dialog.is_user
            }

            if dialog.message:
                chat_info["last_message"] = dialog.message.text[:100] if dialog.message.text else None
                chat_info["last_message_date"] = dialog.message.date.isoformat() if dialog.message.date else None

            chats.append(chat_info)

        return {"chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chats/{chat_id}")
async def get_chat_info(chat_id: str):
    """Get detailed chat information"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)

        chat_info = {
            "id": entity.id,
            "title": getattr(entity, 'title', None) or getattr(entity, 'first_name', ''),
            "username": getattr(entity, 'username', None),
            "is_group": isinstance(entity, (types.Chat, types.Channel)) and getattr(entity, 'megagroup', False),
            "is_channel": isinstance(entity, types.Channel) and not getattr(entity, 'megagroup', False),
            "is_user": isinstance(entity, types.User),
            "participants_count": getattr(entity, 'participants_count', None),
            "about": getattr(entity, 'about', None)
        }

        return chat_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/create-group")
async def create_group(request: CreateGroupRequest):
    """Create a new group"""
    check_client_connected()

    try:
        user_entities = []
        for user_identifier in request.users:
            entity = await get_entity_safe(user_identifier)
            user_entities.append(entity)

        group = await client.create_group(request.title, users=user_entities)

        return {
            "status": "success",
            "group_id": str(group.id),
            "group_name": group.title
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/create-channel")
async def create_channel(request: CreateChannelRequest):
    """Create a new channel or supergroup"""
    check_client_connected()

    try:
        channel = await client.create_channel(
            request.title,
            about=request.about or "",
            megagroup=request.megagroup
        )

        return {
            "status": "success",
            "channel_id": str(channel.id),
            "channel_name": channel.title,
            "is_supergroup": request.megagroup
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/chats/{chat_id}")
async def edit_chat(chat_id: str, request: EditChatRequest):
    """Edit chat information"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)

        if request.title:
            await client.edit_title(entity, request.title)

        if request.about:
            # For channels, use edit_about
            if isinstance(entity, types.Channel):
                await client.edit_admin(entity, about=request.about)

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/{chat_id}/photo")
async def set_chat_photo(chat_id: str, file: UploadFile = File(...)):
    """Set chat photo"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name

        try:
            await client.edit_photo(entity, tmp_path)
            return {"status": "success"}
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chats/{chat_id}/members")
async def get_chat_members(chat_id: str, limit: int = 100):
    """Get chat members"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)
        participants = await client.get_participants(entity, limit=limit)

        members = []
        for participant in participants:
            members.append({
                "id": participant.id,
                "first_name": participant.first_name,
                "last_name": participant.last_name or "",
                "username": participant.username or "",
                "is_bot": participant.bot if hasattr(participant, 'bot') else False
            })

        return {"members": members, "count": len(members)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/{chat_id}/members/add")
async def add_members(chat_id: str, request: AddMembersRequest):
    """Add members to chat"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)
        user_entities = []

        for user_identifier in request.users:
            user_entity = await get_entity_safe(user_identifier)
            user_entities.append(user_entity)

        await client.add_participants(entity, user_entities)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/{chat_id}/members/remove")
async def remove_members(chat_id: str, request: RemoveMembersRequest):
    """Remove members from chat"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)
        user_entities = []

        for user_identifier in request.users:
            user_entity = await get_entity_safe(user_identifier)
            user_entities.append(user_entity)

        await client.delete_participants(entity, user_entities)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chats/{chat_id}/invite-link")
async def get_invite_link(chat_id: str):
    """Get or create invite link"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)
        
        # Check if it's a group or channel
        if not isinstance(entity, (types.Channel, types.Chat)):
            raise HTTPException(status_code=400, detail="Only groups and channels have invite links")
        
        link = await client.export_chat_invite_link(entity)
        return {"invite_link": link}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Message Management
# ============================================================================

@app.get("/api/messages/{chat_id}")
async def get_messages(chat_id: str, limit: int = 20, offset_id: int = 0):
    """Get messages from a chat"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)
        messages = await client.get_messages(entity, limit=limit, offset_id=offset_id)

        message_list = []
        for msg in messages:
            message_data = {
                "id": msg.id,
                "text": msg.text or "",
                "date": msg.date.isoformat() if msg.date else None,
                "sender_id": msg.sender_id if hasattr(msg, 'sender_id') else None,
                "is_out": msg.out if hasattr(msg, 'out') else False,
                "is_reply": msg.is_reply if hasattr(msg, 'is_reply') else False,
                "reply_to_msg_id": msg.reply_to.reply_to_msg_id if hasattr(msg, 'reply_to') and msg.reply_to else None
            }

            # Add media info if present
            if msg.media:
                message_data["has_media"] = True
                message_data["media_type"] = type(msg.media).__name__

                # Get media details based on media type
                media = msg.media

                # Check for photo
                if isinstance(media, types.MessageMediaPhoto):
                    message_data["media_category"] = "photo"
                # Check for document (which can be video, audio, image, or file)
                elif isinstance(media, types.MessageMediaDocument):
                    doc = media.document
                    message_data["mime_type"] = getattr(doc, 'mime_type', None) or ""

                    # Get file name from attributes
                    file_name = None
                    if hasattr(doc, 'attributes'):
                        for attr in doc.attributes:
                            if isinstance(attr, types.DocumentAttributeFilename):
                                file_name = attr.file_name
                                break
                            elif isinstance(attr, types.DocumentAttributeAudio):
                                if hasattr(attr, 'title') and attr.title:
                                    file_name = f"{attr.title}.mp3"
                                break

                    message_data["file_name"] = file_name

                    # Determine category based on mime type and attributes
                    if message_data["mime_type"].startswith('video/'):
                        message_data["media_category"] = "video"
                    elif message_data["mime_type"].startswith('audio/') or message_data["mime_type"] == 'audio/ogg':
                        message_data["media_category"] = "audio"
                    elif message_data["mime_type"].startswith('image/'):
                        message_data["media_category"] = "image"
                    else:
                        message_data["media_category"] = "document"

                    # Check for video note (circular video)
                    if hasattr(doc, 'attributes'):
                        for attr in doc.attributes:
                            if isinstance(attr, types.DocumentAttributeVideo):
                                if hasattr(attr, 'round_message') and attr.round_message:
                                    message_data["media_category"] = "video_note"
                                break
                # Check for geo location
                elif isinstance(media, types.MessageMediaGeo):
                    message_data["media_category"] = "location"
                # Check for contact
                elif isinstance(media, types.MessageMediaContact):
                    message_data["media_category"] = "contact"
                # Check for poll
                elif isinstance(media, types.MessageMediaPoll):
                    message_data["media_category"] = "poll"
                else:
                    message_data["media_category"] = "unknown"

                # Store message ID for media download
                message_data["media_message_id"] = msg.id
            else:
                message_data["has_media"] = False

            message_list.append(message_data)

        return {"messages": message_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/send")
async def send_message(request: MessageRequest):
    """Send a text message"""
    check_client_connected()

    try:
        entity = await get_entity_safe(request.chat_id)

        kwargs = {}
        if request.reply_to:
            kwargs['reply_to'] = request.reply_to
        if request.parse_mode:
            kwargs['parse_mode'] = request.parse_mode
        if request.silent:
            kwargs['silent'] = True
        if request.schedule:
            schedule_time = datetime.fromisoformat(request.schedule.replace('Z', '+00:00'))
            kwargs['schedule'] = schedule_time

        message = await client.send_message(entity, request.message, **kwargs)

        return {
            "status": "success",
            "message_id": message.id,
            "text": message.text,
            "date": message.date.isoformat() if message.date else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/send-media")
async def send_media(
    chat_id: str = Form(...),
    file: UploadFile = File(...),
    caption: Optional[str] = Form(None),
    voice_note: Optional[bool] = Form(False),
    video_note: Optional[bool] = Form(False)
):
    """Send media file (photo, video, document, etc.)"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name

        try:
            kwargs = {}
            if caption:
                kwargs['caption'] = caption
            if voice_note:
                kwargs['voice_note'] = True
            if video_note:
                kwargs['video_note'] = True

            message = await client.send_file(entity, tmp_path, **kwargs)

            return {
                "status": "success",
                "message_id": message.id,
                "caption": message.message or "",
                "has_media": True
            }
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/send-location")
async def send_location(request: LocationRequest):
    """Send location"""
    check_client_connected()

    try:
        entity = await get_entity_safe(request.chat_id)

        from telethon.tl.types import InputMediaGeoPoint, InputGeoPoint

        location = InputMediaGeoPoint(
            InputGeoPoint(lat=request.latitude, long=request.longitude, accuracy_radius=None)
        )

        message = await client.send_file(entity, file=location, caption=request.caption)

        return {
            "status": "success",
            "message_id": message.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/send-contact")
async def send_contact(request: ContactMessageRequest):
    """Send contact"""
    check_client_connected()

    try:
        entity = await get_entity_safe(request.chat_id)
        message = await client.send_contact(
            entity,
            phone=request.phone,
            first_name=request.first_name,
            last_name=request.last_name
        )

        return {
            "status": "success",
            "message_id": message.id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/messages/edit")
async def edit_message(request: EditMessageRequest):
    """Edit a message"""
    check_client_connected()

    try:
        entity = await get_entity_safe(request.chat_id)
        message = await client.edit_message(entity, request.message_id, request.text)

        return {
            "status": "success",
            "message_id": message.id,
            "text": message.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/messages/delete")
async def delete_messages(request: DeleteMessageRequest):
    """Delete messages"""
    check_client_connected()

    try:
        entity = await get_entity_safe(request.chat_id)
        await client.delete_messages(entity, request.message_ids, revoke=request.revoke)

        return {"status": "success", "deleted_count": len(request.message_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/forward")
async def forward_messages(request: ForwardMessageRequest):
    """Forward messages"""
    check_client_connected()

    try:
        from_entity = await get_entity_safe(request.from_chat_id)
        to_entity = await get_entity_safe(request.to_chat_id)

        await client.forward_messages(to_entity, request.message_ids, from_peer=from_entity)

        return {"status": "success", "forwarded_count": len(request.message_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/pin")
async def pin_message(request: PinMessageRequest):
    """Pin or unpin a message"""
    check_client_connected()

    try:
        entity = await get_entity_safe(request.chat_id)

        if request.unpin:
            await client.unpin_message(entity, request.message_id)
        else:
            await client.pin_message(entity, request.message_id)

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/react")
async def react_to_message(request: ReactionRequest):
    """Add or remove reaction to message"""
    check_client_connected()

    try:
        entity = await get_entity_safe(request.chat_id)
        await client.send_reaction(entity, request.message_id, reaction=request.reaction)

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/mark-read")
async def mark_read(chat_id: str, message_id: Optional[int] = None):
    """Mark messages as read"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)
        await client.send_read_acknowledge(entity, max_id=message_id)

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# File Operations
# ============================================================================

@app.get("/api/files/download/{chat_id}/{message_id}")
async def download_media(chat_id: str, message_id: int):
    """Download media from a message"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)
        messages = await client.get_messages(entity, ids=message_id)

        if not messages or not messages[0].media:
            raise HTTPException(status_code=404, detail="Message not found or has no media")

        message = messages[0]

        # Download to memory
        file_bytes = await client.download_media(message, file=bytes)

        # Determine filename
        filename = getattr(message.media, 'file_name', None) or f"file_{message_id}"

        return StreamingResponse(
            io.BytesIO(file_bytes),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/preview/{chat_id}/{message_id}")
async def preview_media(chat_id: str, message_id: int):
    """Preview media from a message (for display in UI)"""
    check_client_connected()

    try:
        entity = await get_entity_safe(chat_id)
        messages = await client.get_messages(entity, ids=message_id)

        if not messages or not messages[0].media:
            raise HTTPException(status_code=404, detail="Message not found or has no media")

        message = messages[0]

        # Download to memory
        file_bytes = await client.download_media(message, file=bytes)

        # Determine media type and filename
        media_type = "application/octet-stream"
        filename = f"file_{message_id}"

        if isinstance(message.media, types.MessageMediaPhoto):
            media_type = "image/jpeg"
            filename = f"photo_{message_id}.jpg"
        elif isinstance(message.media, types.MessageMediaDocument):
            doc = message.media.document
            if hasattr(doc, 'mime_type') and doc.mime_type:
                media_type = doc.mime_type
            if hasattr(doc, 'attributes') and doc.attributes:
                for attr in doc.attributes:
                    if isinstance(attr, types.DocumentAttributeFilename):
                        filename = attr.file_name
                        break
                    elif isinstance(attr, types.DocumentAttributeAudio):
                        if hasattr(attr, 'title') and attr.title:
                            filename = f"{attr.title}.mp3"
                        break

        return Response(
            content=file_bytes,
            media_type=media_type,
            headers={
                "Content-Disposition": f'inline; filename="{filename}"',
                "Cache-Control": "public, max-age=3600"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Search
# ============================================================================

@app.post("/api/search")
async def search_messages(request: SearchRequest):
    """Search messages"""
    check_client_connected()

    try:
        entity = None
        if request.chat_id:
            entity = await get_entity_safe(request.chat_id)

        messages = await client.get_messages(entity, search=request.query, limit=request.limit)

        message_list = []
        for msg in messages:
            message_list.append({
                "id": msg.id,
                "text": msg.text or "",
                "date": msg.date.isoformat() if msg.date else None,
                "chat_id": str(msg.chat_id) if hasattr(msg, 'chat_id') else None
            })

        return {"messages": message_list, "count": len(message_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# Contacts & Users
# ============================================================================

@app.get("/api/contacts")
async def get_contacts():
    """Get contacts list"""
    check_client_connected()

    try:
        # Get contacts using GetContactsRequest
        from telethon.tl.functions.contacts import GetContactsRequest
        result = await client(GetContactsRequest(hash=0))
        
        contact_list = []
        for contact in result.users:
            if not contact.bot:  # Exclude bots
                contact_list.append({
                    "id": contact.id,
                    "first_name": contact.first_name,
                    "last_name": contact.last_name or "",
                    "username": contact.username or "",
                    "phone": contact.phone or ""
                })

        return {"contacts": contact_list}
    except Exception as e:
        # If GetContactsRequest fails, try getting from dialogs
        try:
            dialogs = await client.get_dialogs()
            contact_list = []
            for dialog in dialogs:
                entity = dialog.entity
                if isinstance(entity, types.User) and not entity.bot and not entity.deleted:
                    contact_list.append({
                        "id": entity.id,
                        "first_name": entity.first_name,
                        "last_name": entity.last_name or "",
                        "username": entity.username or "",
                        "phone": entity.phone or ""
                    })
            return {"contacts": contact_list}
        except Exception as e2:
            raise HTTPException(status_code=500, detail=str(e2))

@app.post("/api/contacts/add")
async def add_contact(request: ContactRequest):
    """Add contact"""
    check_client_connected()

    try:
        # Try to get user first
        try:
            user = await client.get_entity(request.phone)
        except:
            user = None

        if user:
            await client.add_contact(
                user,
                first_name=request.first_name,
                last_name=request.last_name or "",
                phone=request.phone
            )
        else:
            # Import contact if user doesn't exist
            contact = InputPhoneContact(
                client_id=0,
                phone=request.phone,
                first_name=request.first_name,
                last_name=request.last_name or ""
            )
            await client.import_contacts([contact])

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/contacts/{user_id}")
async def delete_contact(user_id: str):
    """Delete contact"""
    check_client_connected()

    try:
        user = await get_entity_safe(user_id)
        await client.delete_contacts([user])
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_id}")
async def get_user_info(user_id: str):
    """Get user information"""
    check_client_connected()

    try:
        user = await get_entity_safe(user_id)

        user_info = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name or "",
            "username": user.username or "",
            "phone": user.phone or "",
            "is_bot": user.bot if hasattr(user, 'bot') else False,
            "is_verified": user.verified if hasattr(user, 'verified') else False
        }

        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{user_id}/photos")
async def get_user_photos(user_id: str, limit: int = 10):
    """Get user profile photos"""
    check_client_connected()

    try:
        user = await get_entity_safe(user_id)
        photos = await client.get_profile_photos(user, limit=limit)

        photo_list = []
        for photo in photos:
            photo_list.append({
                "id": photo.id,
                "date": photo.date.isoformat() if photo.date else None
            })

        return {"photos": photo_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/users/{user_id}/block")
async def block_user(user_id: str):
    """Block user"""
    check_client_connected()

    try:
        user = await get_entity_safe(user_id)
        await client.block(user)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/users/{user_id}/unblock")
async def unblock_user(user_id: str):
    """Unblock user"""
    check_client_connected()

    try:
        user = await get_entity_safe(user_id)
        await client.unblock(user)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/blocked")
async def get_blocked_users():
    """Get blocked users list"""
    check_client_connected()

    try:
        # Use GetBlockedRequest
        from telethon.tl.functions.contacts import GetBlockedRequest
        result = await client(GetBlockedRequest(offset=0, limit=100))
        
        blocked_list = []
        for user in result.users:
            blocked_list.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name or "",
                "username": user.username or ""
            })

        return {"blocked": blocked_list}
    except Exception as e:
        # Return empty list if no blocked users or error
        return {"blocked": []}

# ============================================================================
# Account Management
# ============================================================================

@app.get("/api/account")
async def get_account_info():
    """Get own account information"""
    check_client_connected()

    try:
        me = await client.get_me()

        return {
            "id": me.id,
            "first_name": me.first_name,
            "last_name": me.last_name or "",
            "username": me.username or "",
            "phone": me.phone or "",
            "is_bot": me.bot if hasattr(me, 'bot') else False,
            "is_verified": me.verified if hasattr(me, 'verified') else False,
            "is_premium": me.premium if hasattr(me, 'premium') else False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/account/profile")
async def update_profile(request: UpdateProfileRequest):
    """Update profile information"""
    check_client_connected()

    try:
        kwargs = {}
        if request.first_name:
            kwargs['first_name'] = request.first_name
        if request.last_name:
            kwargs['last_name'] = request.last_name
        if request.about:
            kwargs['about'] = request.about

        await client.update_profile(**kwargs)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/account/photo")
async def update_profile_photo(file: UploadFile = File(...)):
    """Update profile photo"""
    check_client_connected()

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name

        try:
            await client.upload_profile_photo(tmp_path)
            return {"status": "success"}
        finally:
            os.unlink(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/account/photo")
async def delete_profile_photo():
    """Delete profile photo"""
    check_client_connected()

    try:
        photos = await client.get_profile_photos('me')
        if photos:
            await client.delete_photos(photos)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# WebSocket for Real-time Updates
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    websocket_connections.append(websocket)

    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connected",
            "status": "success",
            "message": "WebSocket connected"
        })

        # Keep connection alive
        while True:
            try:
                # Wait for client message or timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # Echo back or handle client messages
                await websocket.send_json({"type": "echo", "data": data})
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_json({"type": "ping", "status": "alive"})
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in websocket_connections:
            websocket_connections.remove(websocket)

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
