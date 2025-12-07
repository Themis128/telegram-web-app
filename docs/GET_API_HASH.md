# Getting Your API Hash Using Apis-Telegram Tool

## ✅ Tool Installed!

I've cloned the `Apis-Telegram` tool to help you get your API Hash easily.

## How to Use It

### Step 1: Navigate to the Tool Directory

```powershell
cd Apis-Telegram
```

### Step 2: Run the Tool

```powershell
python Apis.py
```

### Step 3: Follow the Prompts

1. **Enter your phone number** with country code:
   - Example: `+306977777838` (your number)

2. **Enter the code** sent to your Telegram app

3. **Get your APIs!**
   - The tool will display your `api_id` and `api_hash`

## What You'll Get

The tool will output something like:
```
API ID: 7017840434
API Hash: abcdef1234567890abcdef1234567890
```

## After Getting Your API Hash

1. **Copy your API Hash**

2. **Update your .env file:**
   - Open: `D:\Nuxt Projects\telegram\.env`
   - Replace `YOUR_API_HASH_HERE` with your actual API Hash

3. **Continue with Cursor configuration:**
   - See `WHERE_TO_CONFIGURE.md` for next steps

## Quick Command

```powershell
cd Apis-Telegram
python Apis.py
```

Then follow the prompts!

---

**Note:** If you get an error about "It is not possible to get APIs", the tool may need an update. In that case, you can still get your API Hash manually from https://my.telegram.org/apps


