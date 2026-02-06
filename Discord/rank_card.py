from PIL import Image, ImageDraw, ImageFont
import discord
import os

async def generate_rank_card(user: discord.Member, xp: float):
    bg = Image.open("assets/bg.png").convert("RGBA")

    draw = ImageDraw.Draw(bg)
    font_big = ImageFont.truetype("arial.ttf", 60)
    font_small = ImageFont.truetype("arial.ttf", 40)

    # User name
    draw.text((260, 40), f"{user.name}", font=font_big, fill="white")

    # XP text
    draw.text((260, 130), f"XP: {round(xp, 2)}", font=font_small, fill="white")

    # Progress bar
    bar_empty = Image.open("assets/bar_empty.png").convert("RGBA")
    bar_fill = Image.open("assets/bar_fill.png").convert("RGBA")

    bg.paste(bar_empty, (260, 200), bar_empty)

    fill_amt = min(550, int((xp % 100) * 5.5))
    bar_fill = bar_fill.crop((0, 0, fill_amt, 50))
    bg.paste(bar_fill, (260, 200), bar_fill)

    # User avatar
    avatar_asset = user.display_avatar.replace(size=256)
    avatar_bytes = await avatar_asset.read()
    avatar = Image.open(BytesIO(avatar_bytes)).resize((200, 200))
    bg.paste(avatar, (30, 40))

    path = f"rank_{user.id}.png"
    bg.save(path)
    return path
