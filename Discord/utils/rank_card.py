from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
import discord

CARD_WIDTH = 900
CARD_HEIGHT = 300

ASSETS = "Discord/assets/"


async def load_image_from_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            return Image.open(io.BytesIO(data)).convert("RGBA")


async def generate_rank_card(user, xp, level, next_xp, display_name):
    # Load images
    bg = Image.open(f"{ASSETS}bg.png").convert("RGBA").resize((CARD_WIDTH, CARD_HEIGHT))
    bar_empty = Image.open(f"{ASSETS}bar_empty.png").convert("RGBA")
    bar_fill = Image.open(f"{ASSETS}bar_fill.png").convert("RGBA")

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
    font_large = ImageFont.truetype("arial.ttf", 48)
    font_small = ImageFont.truetype("arial.ttf", 32)

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
