from PIL import Image, ImageDraw, ImageFont
import discord
from io import BytesIO

async def generate_leaderboard(entries, guild):
    img = Image.new("RGB", (900, 100 + len(entries) * 70), "black")
    draw = ImageDraw.Draw(img)

    title = ImageFont.truetype("arial.ttf", 50)
    font = ImageFont.truetype("arial.ttf", 35)

    draw.text((250, 20), "ANIME BOOST LEADERBOARD", fill="cyan", font=title)

    y = 100
    for i, (user_id, xp) in enumerate(entries, start=1):
        user = guild.get_member(user_id)
        name = user.name if user else "Unknown"

        draw.text((50, y), f"{i}. {name}", fill="white", font=font)
        draw.text((600, y), f"{round(xp, 2)} XP", fill="yellow", font=font)

        y += 70

    path = "leaderboard.png"
    img.save(path)
    return path
