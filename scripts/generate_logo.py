from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Vibrant Medical Palette
BG_OUTER = "#0F2027"
BG_INNER = "#2C5364"
HEART_COLOR = "#FF416C"  # Vibrant Pink/Red
TECH_LINE = "#FFFFFF"    # White for the pulse
NODE_COLOR = "#41D4FF"   # Cyan for the nodes

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

def create_gradient(size: int, inner: str, outer: str) -> Image.Image:
    base = Image.new("RGB", (size, size), outer)
    inner_rgb = hex_to_rgb(inner)
    outer_rgb = hex_to_rgb(outer)
    pixels = base.load()
    center = size / 2
    max_dist = size / 1.4
    
    for y in range(size):
        for x in range(size):
            dx = x - center
            dy = y - center
            dist = math.sqrt(dx*dx + dy*dy)
            ratio = min(1.0, dist / max_dist)
            
            r = int(inner_rgb[0] * (1 - ratio) + outer_rgb[0] * ratio)
            g = int(inner_rgb[1] * (1 - ratio) + outer_rgb[1] * ratio)
            b = int(inner_rgb[2] * (1 - ratio) + outer_rgb[2] * ratio)
            pixels[x, y] = (r, g, b)
    return base

def draw_heart(draw, center_x, center_y, size, color):
    points = []
    # Parametric heart equation
    for t in range(0, 628): # 0 to 2pi * 100
        t_val = t / 100.0
        # x = 16sin^3(t)
        # y = 13cos(t) - 5cos(2t) - 2cos(3t) - cos(4t)
        x = size * (16 * math.sin(t_val)**3) / 35
        y = -size * (13 * math.cos(t_val) - 5 * math.cos(2*t_val) - 2 * math.cos(3*t_val) - math.cos(4*t_val)) / 35
        points.append((center_x + x, center_y + y))
    
    draw.polygon(points, fill=color)

def draw_logo(size: int) -> Image.Image:
    # 1. Background Gradient
    img = create_gradient(size, BG_INNER, BG_OUTER)
    draw = ImageDraw.Draw(img, "RGBA")
    
    center = size // 2
    
    # 2. Subtle Glow (simulated with a semi-transparent circle)
    glow_radius = size * 0.45
    left_up = center - glow_radius
    right_down = center + glow_radius
    draw.ellipse([left_up, left_up, right_down, right_down], fill=(255, 255, 255, 10))

    # 3. The Heart
    heart_size = size * 0.7
    # Offset y slightly to center the heart visually
    draw_heart(draw, center, center + size * 0.05, heart_size, HEART_COLOR)

    # 4. Tech/Pulse Line (ECG Style)
    line_width = int(size * 0.03)
    y_base = center + size * 0.05
    
    # Points for the heartbeat line
    points = [
        (center - size*0.35, y_base),
        (center - size*0.15, y_base),
        (center - size*0.08, y_base - size*0.18), # Peak up
        (center + size*0.08, y_base + size*0.18), # Peak down
        (center + size*0.15, y_base),
        (center + size*0.35, y_base)
    ]
    draw.line(points, fill=TECH_LINE, width=line_width, joint="curve")
    
    # 5. Tech Nodes (Dots at key points)
    dot_radius = size * 0.025
    for i, (px, py) in enumerate(points):
        # Draw dots on start, peaks, and end
        if i in [0, 2, 3, 5]: 
            draw.ellipse([px-dot_radius, py-dot_radius, px+dot_radius, py+dot_radius], fill=NODE_COLOR)

    # 6. Apply Circular Mask
    img = img.convert("RGBA")
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, size, size), fill=255)
    img.putalpha(mask)

    return img

def main() -> None:
    # Render at high resolution
    base = draw_logo(1024)
    
    # Save required sizes
    base.resize((180, 180), Image.LANCZOS).save(ASSETS_DIR / "logo.png")
    base.resize((192, 192), Image.LANCZOS).save(ASSETS_DIR / "icon-192x192.png")
    base.resize((512, 512), Image.LANCZOS).save(ASSETS_DIR / "icon-512x512.png")
    
    print("✅ Created new attractive medical heart logo")

if __name__ == "__main__":
    main()
