"""
Generate PWA icons for Telegram Web App
Creates icon-192.png and icon-512.png in the project root
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("PIL/Pillow not found. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True

def create_icon(size):
    """Create a Telegram-style icon"""
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='#3390ec')
    draw = ImageDraw.Draw(img)

    # Create gradient effect
    for i in range(size):
        # Gradient from #3390ec to #0088cc
        ratio = i / size
        r = int(51 * (1 - ratio) + 0 * ratio)
        g = int(144 * (1 - ratio) + 136 * ratio)
        b = int(236 * (1 - ratio) + 204 * ratio)
        draw.rectangle([(0, i), (size, i+1)], fill=(r, g, b))

    # Draw Telegram paper plane icon
    center_x, center_y = size // 2, size // 2
    scale = size / 200

    # Plane body (triangle)
    plane_points = [
        (center_x - 40 * scale, center_y - 20 * scale),  # Top left
        (center_x + 60 * scale, center_y),                # Right point
        (center_x - 40 * scale, center_y + 20 * scale),   # Bottom left
        (center_x - 20 * scale, center_y),                # Back point
    ]
    draw.polygon(plane_points, fill='white')

    # Wing
    wing_points = [
        (center_x - 20 * scale, center_y),
        (center_x + 20 * scale, center_y - 15 * scale),
        (center_x + 20 * scale, center_y + 15 * scale),
    ]
    draw.polygon(wing_points, fill='white')

    return img

def main():
    """Generate both icon sizes"""
    print("Generating PWA icons...")

    # Generate 192x192 icon
    print("Creating icon-192.png...")
    icon_192 = create_icon(192)
    icon_192.save('icon-192.png', 'PNG')
    print("✅ icon-192.png created")

    # Generate 512x512 icon
    print("Creating icon-512.png...")
    icon_512 = create_icon(512)
    icon_512.save('icon-512.png', 'PNG')
    print("✅ icon-512.png created")

    print("\n🎉 Icons generated successfully!")
    print("Files saved to project root:")
    print("  - icon-192.png")
    print("  - icon-512.png")

if __name__ == "__main__":
    main()
