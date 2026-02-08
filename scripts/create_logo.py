#!/usr/bin/env python3
"""
Create antique-style fancy 3D animated logo for Men's Boutique
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import os

def create_antique_logo():
    """Create a stylish antique 3D logo."""

    # Logo dimensions
    width, height = 800, 400

    # Create image with gradient background (antique gold-brown)
    img = Image.new('RGB', (width, height), color=(245, 240, 220))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Add antique texture/pattern
    for i in range(width):
        for j in range(height):
            if (i + j) % 20 == 0:
                draw.point((i, j), fill=(200, 190, 170, 20))

    # Draw decorative border (ornate frame)
    border_color = (139, 69, 19)  # Saddle brown
    draw.rectangle([10, 10, width-10, height-10], outline=border_color, width=3)
    draw.rectangle([15, 15, width-15, height-15], outline=(184, 134, 11), width=1)  # Dark goldenrod

    # Draw corner decorations (antique style)
    corner_size = 30
    corners = [(20, 20), (width-20, 20), (20, height-20), (width-20, height-20)]
    for cx, cy in corners:
        draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill=(184, 134, 11), outline=border_color)

    # Main text: "Men's Boutique"
    text_main = "MEN'S BOUTIQUE"

    # Try to use a fancy font, fallback to default
    try:
        font_large = ImageFont.truetype("arial.ttf", 72)
        font_small = ImageFont.truetype("arial.ttf", 32)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw 3D shadow effect (depth)
    shadow_offset = 4
    text_bbox = draw.textbbox((0, 0), text_main, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 80

    # Shadow layer (creates 3D effect)
    shadow_color = (100, 80, 60, 150)
    for offset in range(shadow_offset, 0, -1):
        alpha = int(150 * (1 - offset / shadow_offset))
        draw.text((text_x + offset, text_y + offset), text_main,
                 font=font_large, fill=(100, 80, 60, alpha))

    # Main text with gradient effect (golden)
    draw.text((text_x, text_y), text_main, font=font_large,
             fill=(184, 134, 11))  # Dark goldenrod

    # Add accent line under text
    line_y = text_y + 90
    draw.line([(width//4, line_y), (3*width//4, line_y)],
             fill=(139, 69, 19), width=2)

    # Subtitle: Fancy text
    subtitle = "Premium Menswear Collection"
    text_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    text_width = text_bbox[2] - text_bbox[0]
    subtitle_x = (width - text_width) // 2
    subtitle_y = line_y + 30

    draw.text((subtitle_x, subtitle_y), subtitle, font=font_small,
             fill=(139, 69, 19))  # Saddle brown

    # Add decorative elements (stars/flourishes)
    flourish_y = subtitle_y + 50
    flourish_x_positions = [width//4, width//2, 3*width//4]

    for flourish_x in flourish_x_positions:
        # Draw decorative diamond shapes
        diamond_size = 8
        draw.polygon(
            [(flourish_x, flourish_y - diamond_size),
             (flourish_x + diamond_size, flourish_y),
             (flourish_x, flourish_y + diamond_size),
             (flourish_x - diamond_size, flourish_y)],
            fill=(184, 134, 11), outline=(139, 69, 19)
        )

    # Apply slight blur for antique effect
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

    # Save logo
    logo_path = "D:\\HACKATON-III\\Reusable-ecommerce-shop\\learnflow-app\\public\\logo.png"
    img.save(logo_path, 'PNG')

    print("[SUCCESS] Antique logo created:")
    print(f"  Location: {logo_path}")
    print(f"  Dimensions: {width}x{height}px")
    print(f"  Style: Antique gold with 3D shadow effect")
    print(f"  Colors: Saddle brown, dark goldenrod, antique cream")

    return logo_path

def create_3d_animated_svg():
    """Create SVG with 3D CSS animation for logo."""

    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @keyframes rotate3D {
        0% { transform: rotateY(0deg) rotateX(0deg); }
        50% { transform: rotateY(180deg) rotateX(10deg); }
        100% { transform: rotateY(360deg) rotateX(0deg); }
      }

      @keyframes shine {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
      }

      .antique-bg {
        fill: #f5f0dc;
      }

      .logo-text {
        font-family: Georgia, serif;
        font-size: 72px;
        font-weight: bold;
        fill: #b8860b;
        text-anchor: middle;
        filter: drop-shadow(3px 3px 6px rgba(100,80,60,0.5));
        animation: rotate3D 4s infinite ease-in-out;
      }

      .subtitle {
        font-family: Georgia, serif;
        font-size: 32px;
        fill: #8b4513;
        text-anchor: middle;
      }

      .shine-effect {
        fill: #d4af37;
        opacity: 0.3;
        animation: shine 2s infinite;
      }

      .border-rect {
        fill: none;
        stroke: #8b4513;
        stroke-width: 3;
      }
    </style>
  </defs>

  <!-- Antique background -->
  <rect class="antique-bg" width="800" height="400"/>

  <!-- Border frame -->
  <rect class="border-rect" x="10" y="10" width="780" height="380"/>
  <rect class="border-rect" x="15" y="15" width="770" height="370" stroke="#b8860b" stroke-width="1"/>

  <!-- Corner decorations -->
  <circle cx="30" cy="30" r="10" fill="#b8860b" stroke="#8b4513"/>
  <circle cx="770" cy="30" r="10" fill="#b8860b" stroke="#8b4513"/>
  <circle cx="30" cy="370" r="10" fill="#b8860b" stroke="#8b4513"/>
  <circle cx="770" cy="370" r="10" fill="#b8860b" stroke="#8b4513"/>

  <!-- Main logo text with 3D animation -->
  <text class="logo-text" x="400" y="120">MEN'S BOUTIQUE</text>

  <!-- Shine effect -->
  <ellipse class="shine-effect" cx="400" cy="100" rx="150" ry="30"/>

  <!-- Decorative line -->
  <line x1="200" y1="180" x2="600" y2="180" stroke="#8b4513" stroke-width="2"/>

  <!-- Subtitle -->
  <text class="subtitle" x="400" y="240">Premium Menswear Collection</text>

  <!-- Decorative flourishes -->
  <polygon points="200,300 210,310 200,320 190,310" fill="#b8860b" stroke="#8b4513"/>
  <polygon points="400,300 410,310 400,320 390,310" fill="#b8860b" stroke="#8b4513"/>
  <polygon points="600,300 610,310 600,320 590,310" fill="#b8860b" stroke="#8b4513"/>

  <!-- Bottom text -->
  <text class="subtitle" x="400" y="370" style="font-size: 18px;">Est. 2026</text>
</svg>'''

    svg_path = "D:\\HACKATON-III\\Reusable-ecommerce-shop\\learnflow-app\\public\\logo-animated.svg"
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

    print("[SUCCESS] Animated 3D SVG logo created:")
    print(f"  Location: {svg_path}")
    print(f"  Animation: 3D rotation, shine effect, smooth transitions")
    print(f"  Format: SVG with CSS animations")

    return svg_path

def create_favicon():
    """Create favicon version of logo."""

    # Create small 256x256 version for favicon
    img = Image.new('RGB', (256, 256), color=(245, 240, 220))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Border
    draw.rectangle([5, 5, 251, 251], outline=(139, 69, 19), width=2)

    # Try font
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    # Main letter "M" (for Men's Boutique)
    draw.text((128, 128), "M", font=font, fill=(184, 134, 11),
             anchor="mm")

    # Save favicon
    favicon_path = "D:\\HACKATON-III\\Reusable-ecommerce-shop\\learnflow-app\\public\\favicon.ico"
    img.save(favicon_path, 'ICO')

    print("[SUCCESS] Favicon created:")
    print(f"  Location: {favicon_path}")
    print(f"  Size: 256x256px")

    return favicon_path

def main():
    """Create all logo variants."""
    print("=" * 70)
    print("[LOGO GENERATOR] CREATING ANTIQUE FANCY 3D LOGO")
    print("=" * 70)

    logo_png = create_antique_logo()
    print()
    svg_logo = create_3d_animated_svg()
    print()
    favicon = create_favicon()

    print("\n" + "=" * 70)
    print("[COMPLETE] All logos created successfully!")
    print("=" * 70)
    print("\nLogo Assets:")
    print(f"  1. PNG Static Logo: logo.png (800x400px)")
    print(f"  2. Animated 3D SVG: logo-animated.svg (with 3D rotation)")
    print(f"  3. Favicon: favicon.ico (256x256px)")
    print("\nUsage:")
    print("  - HTML <img src='/logo.png'>")
    print("  - HTML <object data='/logo-animated.svg'>")
    print("  - Favicon in <head>: <link rel='icon' href='/favicon.ico'>")

if __name__ == "__main__":
    main()
