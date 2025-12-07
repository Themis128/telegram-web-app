#!/usr/bin/env python3
"""
Script to add security dependencies to all API endpoints in app.py
"""

import re

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match API endpoints (excluding WebSocket and static files)
pattern = r'@app\.(get|post|put|delete)\(["\'](/api/[^"\']+)["\']'

def add_dependency(match):
    method = match.group(1)
    path = match.group(2)
    
    # Skip if already has dependencies
    if 'dependencies=' in content[content.find(match.group(0)):content.find(match.group(0))+200]:
        return match.group(0)
    
    # Add dependencies parameter
    return f'@app.{method}("{path}", dependencies=[Depends(security_dependencies)])'

# Replace all matches
new_content = re.sub(pattern, add_dependency, content)

# Write back
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Security dependencies added to all API endpoints")

