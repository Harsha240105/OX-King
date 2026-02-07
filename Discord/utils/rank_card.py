from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import discord
import os

CARD_WIDTH = 900
CARD_HEIGHT = 300

# Use absolute path for assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")


def load_font(size):
    """Load font with fallback support for cross-platform compatibility."""
    try:
        # Try common Linux system fonts first
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "C:\\Windows\\Fonts\\arial.ttf",  # Windows
            os.path.join(ASSETS_DIR, "DejaVuSans.ttf"),  # Project assets
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
    except Exception as e:
        print(f"⚠️ Font loading error: {e}. Using default font.")
    
    # Fallback to default PIL font
    return ImageFont.load_default()


async def load_image_from_url(url):
    """Load image from URL with error handling for network failures."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.read()
                return Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception as e:
        print(f"⚠️ Failed to load avatar from URL: {e}. Using fallback.")
        # Return a fallback gradient image (purple circle)
        fallback = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        fallback_draw = ImageDraw.Draw(fallback)
        fallback_draw.ellipse((0, 0, 180, 180), fill=(128, 0, 255, 255))
        return fallback


async def generate_rank_card(user, xp, level, next_xp, display_name):
    """Generate rank card with comprehensive error handling."""
    try:
        # Load images with absolute paths
        bg_path = os.path.join(ASSETS_DIR, "bg.png")
        bar_empty_path = os.path.join(ASSETS_DIR, "bar_empty.png")
        bar_fill_path = os.path.join(ASSETS_DIR, "bar_fill.png")
        
        try:
            bg = Image.open(bg_path).convert("RGBA").resize((CARD_WIDTH, CARD_HEIGHT))
            bar_empty = Image.open(bar_empty_path).convert("RGBA")
            bar_fill = Image.open(bar_fill_path).convert("RGBA")
        except FileNotFoundError as e:
            print(f"❌ Asset file not found: {e}")
            return None
        except Exception as e:
            print(f"❌ Error loading assets: {e}")
            return None

        # Create base canvas
        card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
        card.paste(bg, (0, 0))

        draw = ImageDraw.Draw(card)

        # ============================
        # USER AVATAR (round + glow)
        # ============================
        avatar_size = 180
        avatar = await load_image_from_url(user.display_avatar.url)
        avatar = avatar.resize((avatar_size, avatar_size))

        # Create circular mask
        mask = Image.new("L", (avatar_size, avatar_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)

        # Glow behind avatar
        glow = Image.new("RGBA", (avatar_size + 40, avatar_size + 40), (128, 0, 255, 180))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse((0, 0, avatar_size + 40, avatar_size + 40), fill=(128, 0, 255, 100))
        card.paste(glow, (50 - 20, 60 - 20), glow)

        # Paste avatar
        card.paste(avatar, (50, 60), mask)

        # ============================
        # TEXT
        # ============================
        font_large = load_font(48)
        font_small = load_font(32)

        # Display name
        draw.text((260, 40), display_name, font=font_large, fill=(255, 255, 255))

        # Level + XP text
        draw.text((260, 110), f"Level: {level}", font=font_small, fill=(255, 255, 255))
        draw.text((260, 160), f"XP: {int(xp)} / {int(next_xp)}", font=font_small, fill=(200, 200, 200))

        # ============================
        # XP BAR
        # ============================
        bar_x = 260
        bar_y = 210

        card.paste(bar_empty, (bar_x, bar_y), bar_empty)

        progress = min(xp / next_xp, 1)
        fill_width = int(bar_fill.width * progress)

        bar_progress = bar_fill.crop((0, 0, fill_width, bar_fill.height))
        card.paste(bar_progress, (bar_x, bar_y), bar_progress)

        # ============================
        # OUTPUT
        # ============================
        buffer = io.BytesIO()
        card.save(buffer, "PNG")
        buffer.seek(0)

        return discord.File(fp=buffer, filename=f"{user.name}_rank.png")
    
    except Exception as e:
        print(f"❌ Error generating rank card: {e}")
        return None
