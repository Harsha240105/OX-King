import os
import discord
from discord.ext import commands, tasks
import aiosqlite
import asyncio

# Local files
from utils.db import Database
from utils.rank_card import generate_rank_card
from utils.leaderboard import generate_leaderboard

# ===============================
# FLASK KEEP ALIVE (Render.com)
# ===============================
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "OXK Ranking Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()


# ===============================
# DISCORD BOT SETUP
# ===============================
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

db = Database("database.db")


# ===============================
# BOT READY EVENT
# ===============================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await db.setup()
    voice_xp_loop.start()
    print("XP LOOP RUNNING...")


# ===============================
# VOICE XP LOOP (per minute)
# ===============================
VOICE_CHANNEL_NAME = "Anime"
XP_PER_MINUTE = 0.833   # = 50 XP / hour

@tasks.loop(minutes=1)
async def voice_xp_loop():
    await bot.wait_until_ready()

    if not bot.guilds:
        return

    guild = bot.guilds[0]
    channel = discord.utils.get(guild.voice_channels, name=VOICE_CHANNEL_NAME)

    if not channel:
        print(f"❌ Voice channel '{VOICE_CHANNEL_NAME}' not found")
        return

    for member in channel.members:
        if member.bot:
            continue

        await db.add_xp(member.id, XP_PER_MINUTE)
        print(f"🎉 Gave {XP_PER_MINUTE} XP → {member.name}")


# ===============================
# COMMAND: !level
# ===============================
@bot.command()
async def level(ctx):
    """Show your rank card"""
    xp, level, next_xp = await db.get_user_progress(ctx.author.id)

    file = await generate_rank_card(
        user=ctx.author,
        xp=xp,
        level=level,
        next_xp=next_xp,
        display_name="OXK"  # Your custom name
    )

    await ctx.send(file=file)


# ===============================
# COMMAND: !leaderboard
# ===============================
@bot.command(aliases=["lb"])
async def leaderboard(ctx):
    file = await generate_leaderboard(ctx.guild, db)
    await ctx.send(file=file)


# ===============================
# START BOT
# ===============================
keep_alive()
bot.run(TOKEN)
