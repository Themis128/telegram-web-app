#!/usr/bin/env python3
"""
Script to update PWA version across all files
Run this script whenever you make changes to ensure PWA updates automatically
"""

import re
import os
from datetime import datetime

def update_version():
    # Generate new version based on timestamp
    version = datetime.now().strftime("%Y.%m.%d.%H%M")
    # Or use a simpler versioning scheme
    # version = "2.0.2"  # Increment manually

    print(f"Updating PWA version to: {version}")

    # Update sw.js
    sw_file = "sw.js"
    if os.path.exists(sw_file):
        with open(sw_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update VERSION constant
        content = re.sub(
            r"const VERSION = '[^']+';",
            f"const VERSION = '{version}';",
            content
        )

        with open(sw_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated {sw_file}")

    # Update manifest.json
    manifest_file = "manifest.json"
    if os.path.exists(manifest_file):
        with open(manifest_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update version field
        content = re.sub(
            r'"version": "[^"]+"',
            f'"version": "{version}"',
            content
        )

        # Update start_url with version query
        content = re.sub(
            r'"start_url": "/\?v=[^"]+"',
            f'"start_url": "/?v={version}"',
            content
        )

        with open(manifest_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated {manifest_file}")

    print(f"\n✅ Version updated to {version}")
    print("The PWA will automatically update for users on next page load!")

if __name__ == "__main__":
    update_version()
