"""
Quick script to generate placeholder meme images for testing.
Run this once to create test images.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_meme(filename, text, color=(255, 0, 255)):
    """Creates a simple placeholder meme image"""
    # Create image with transparency
    img = Image.new('RGBA', (400, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw a colored circle
    padding = 50
    draw.ellipse([padding, padding, 400-padding, 400-padding],
                 fill=color + (200,),  # color with alpha
                 outline=color + (255,), width=5)

    # Try to use a font, fall back to default if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Draw text
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text
    x = (400 - text_width) // 2
    y = (400 - text_height) // 2

    # Draw text with outline
    for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=(0, 0, 0, 255))
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    # Save
    filepath = os.path.join('assets', 'memes', filename)
    img.save(filepath)
    print(f"Created: {filepath}")

def main():
    os.makedirs('assets/memes', exist_ok=True)

    print("Generating placeholder meme images...")

    # Define memes with colors
    memes = [
        ('sigma_stare.png', 'SIGMA', (138, 43, 226)),      # purple
        ('peace_sign.png', 'PEACE', (0, 255, 127)),        # green
        ('skibidi_salute.gif', 'SKIBIDI', (255, 20, 147)), # pink
        ('tpose.png', 'T-POSE', (255, 215, 0)),            # gold
        ('pointing.png', 'POINT', (0, 191, 255)),          # blue
        ('open_palm.png', 'STOP', (255, 69, 0)),           # red-orange
        ('arms_crossed.png', 'BOSS', (50, 205, 50)),       # lime
        ('double_hand.png', 'BOTH', (255, 0, 255)),        # magenta
    ]

    for filename, text, color in memes:
        create_placeholder_meme(filename, text, color)

    print(f"\n✅ Generated {len(memes)} placeholder meme images!")
    print("Add your own meme images to assets/memes/ to replace these.")

if __name__ == '__main__':
    main()
