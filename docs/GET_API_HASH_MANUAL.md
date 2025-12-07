# Getting Your API Hash - Manual Method

## ⚠️ Tool Issue

The automated tool says your account has been temporarily restricted (too many attempts). You'll need to wait 8 hours OR use the manual method below.

## ✅ Manual Method (Recommended)

### Step 1: Go to Telegram API Portal

1. Open your browser
2. Go to: **https://my.telegram.org/apps**
3. Log in with your phone number: `+306977777838`

### Step 2: Enter Verification Code

1. You'll receive a code in your Telegram app
2. Enter the code on the website

### Step 3: Create/View Your Application

1. If you don't have an app yet, click **"Create application"**
2. Fill in:
   - **App title:** (any name, e.g., "My MCP App")
   - **Short name:** (any short name)
   - **Platform:** Choose any (e.g., "Desktop")
   - **Description:** (optional)

3. Click **"Create application"**

### Step 4: Get Your Credentials

You'll see:
- **App api_id:** `7017840434` (you already have this!)
- **App api_hash:** `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` ← **COPY THIS!**

### Step 5: Update Your .env File

1. Open: `D:\Nuxt Projects\telegram\.env`
2. Replace `YOUR_API_HASH_HERE` with your actual API Hash
3. Save the file

## Your Current Status

✅ **API ID:** `7017840434`  
✅ **Phone:** `+306977777838`  
⏳ **API Hash:** Get from https://my.telegram.org/apps

## After Getting API Hash

1. ✅ Update `.env` file with API Hash
2. ⏳ Configure Cursor's `settings.json` (see `WHERE_TO_CONFIGURE.md`)
3. ⏳ Restart Cursor
4. ⏳ Authenticate with Telegram

## Alternative: Wait and Retry Tool

If you prefer to use the automated tool:
- Wait 8 hours
- Then run: `cd Apis-Telegram; python Apis.py`

But the manual method is usually faster and more reliable!

---

**Quick Link:** https://my.telegram.org/apps


