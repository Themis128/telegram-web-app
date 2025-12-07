# PWA Auto-Update Guide

Your PWA now automatically updates when you make changes! Here's how it works:

## 🚀 How Auto-Update Works

1. **Version-Based Caching**: The service worker uses version numbers to manage cache
2. **Automatic Update Detection**: The app checks for updates every 60 seconds
3. **Immediate Activation**: New service workers activate immediately when detected
4. **Auto-Reload**: The app automatically reloads when updates are available

## 📝 Making Changes

### Option 1: Automatic Version Update (Recommended)

Run the version update script after making changes:

```bash
python update_version.py
```

This will:
- Generate a new version number (timestamp-based)
- Update `sw.js` with the new version
- Update `manifest.json` with the new version
- Force all users to get the update on next page load

### Option 2: Manual Version Update

1. Edit `sw.js` and change the `VERSION` constant:
   ```javascript
   const VERSION = '2.0.2';  // Increment this
   ```

2. Edit `manifest.json` and update:
   ```json
   {
     "version": "2.0.2",
     "start_url": "/?v=2.0.2"
   }
   ```

3. Restart your server - users will get the update automatically!

## 🔄 Update Behavior

### For Users:
- **Automatic**: Updates are detected in the background
- **Seamless**: App reloads automatically when update is ready
- **Notification**: Users see "App updated! Reloading..." message
- **No Action Required**: Everything happens automatically

### Update Frequency:
- Checks for updates every **60 seconds**
- Checks immediately on page load
- Checks when service worker is installed

## 🎯 Best Practices

1. **Update Version After Changes**: Always run `update_version.py` after making changes
2. **Test Updates**: Test in a new browser window/incognito mode
3. **Version Format**: Use semantic versioning (e.g., `2.0.1`, `2.0.2`)
4. **Cache Strategy**: HTML files always fetch fresh from network first

## 🔍 How to Verify Updates

1. **Open DevTools** → Application → Service Workers
2. **Check Status**: Should show "activated and is running"
3. **Check Version**: Look at console logs for version number
4. **Test Update**: Make a change, update version, reload page

## 🐛 Troubleshooting

### Updates Not Working?

1. **Clear Cache**:
   - DevTools → Application → Clear Storage → Clear site data
   - Or hard refresh: `Ctrl+Shift+R` (Windows) / `Cmd+Shift+R` (Mac)

2. **Check Service Worker**:
   - DevTools → Application → Service Workers
   - Click "Update" button
   - Click "Unregister" if needed, then reload

3. **Check Version**:
   - Ensure `sw.js` and `manifest.json` have matching versions
   - Check browser console for version logs

4. **Force Update**:
   - Change version number in `sw.js`
   - Restart server
   - Hard refresh browser

## 📋 Files Updated

- ✅ `sw.js` - Service worker with version-based caching
- ✅ `manifest.json` - PWA manifest with version
- ✅ `index.html` - Auto-update detection and reload logic
- ✅ `update_version.py` - Helper script to update versions

## 🎉 Result

Now when you make changes:
1. Update the version (run `update_version.py`)
2. Restart your server
3. Users automatically get the update within 60 seconds
4. No manual intervention needed!
