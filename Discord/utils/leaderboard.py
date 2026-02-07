from PIL import Image, ImageDraw, ImageFont
import discord
import io
import os

CARD_WIDTH = 900
CARD_HEIGHT = 700

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


async def generate_leaderboard(guild, db):
    """Generate leaderboard with comprehensive error handling."""
    try:
        # Fetch leaderboard data
        rows = await db.get_leaderboard(limit=10)

        # Create card
        img = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (10, 10, 35, 255))
        draw = ImageDraw.Draw(img)

        # Title - Load fonts with fallback
        font_title = load_font(60)
        font_header = load_font(40)
        font_body = load_font(32)

        # Glow behind title
        glow = Image.new("RGBA", (CARD_WIDTH, 150), (128, 0, 255, 80))
        img.paste(glow, (0, 0), glow)

        draw.text((CARD_WIDTH//2 - 200, 20), "OXK Ranking", font=font_title, fill=(255, 255, 255))

        # Column Headers
        draw.text((50, 140), "Rank", font=font_header, fill=(200, 200, 255))
        draw.text((200, 140), "User", font=font_header, fill=(200, 200, 255))
        draw.text((550, 140), "Level", font=font_header, fill=(200, 200, 255))
        draw.text((750, 140), "XP", font=font_header, fill=(200, 200, 255))

        # Leaderboard entries
        y = 200
        rank = 1

        for user_id, xp in rows:
            try:
                # Safely convert XP to level
                level, next_xp = db.xp_to_level(xp)
            except Exception as e:
                print(f"⚠️ Error calculating level for user {user_id}: {e}")
                level = 0

            # Get user (might not be cached)
            user = guild.get_member(user_id)
            name = user.display_name if user else f"User {user_id}"

            try:
                # Rank number
                draw.text((60, y), f"#{rank}", font=font_body, fill=(255, 255, 255))

                # Username
                draw.text((200, y), name, font=font_body, fill=(255, 255, 255))

                # Level
                draw.text((550, y), str(level), font=font_body, fill=(255, 255, 255))

                # XP
                draw.text((750, y), str(int(xp)), font=font_body, fill=(255, 255, 255))
            except Exception as e:
                print(f"⚠️ Error drawing leaderboard row for {name}: {e}")

            y += 60
            rank += 1

        # Output as file
        buffer = io.BytesIO()
        img.save(buffer, "PNG")
        buffer.seek(0)

        return discord.File(fp=buffer, filename="leaderboard.png")
    
    except Exception as e:
        print(f"❌ Error generating leaderboard: {e}")
        return None
