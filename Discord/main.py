from flask import Flask
from threading import Thread
import discord
from discord.ext import tasks, commands
import asyncio
import os

from utils.db import setup_db, add_xp, get_xp, get_top
from utils.rank_card import generate_rank_card
from utils.leaderboard import generate_leaderboard

# -----------------------------
# KEEP ALIVE (Render)
# -----------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# -----------------------------
# DISCORD BOT
# -----------------------------
TOKEN = os.getenv("BOT_TOKEN")
VOICE_CHANNEL_NAME = "Anime"
XP_PER_MINUTE = 0.833

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# XP LOOP
@tasks.loop(minutes=1)
async def xp_loop():
    await bot.wait_until_ready()
    guild = bot.guilds[0]
    channel = discord.utils.get(guild.voice_channels, name=VOICE_CHANNEL_NAME)

    if not channel:
        print("Voice channel not found.")
        return

    for member in channel.members:
        if not member.bot:
            await add_xp(member.id, XP_PER_MINUTE)
            print(f"Gave {XP_PER_MINUTE} XP to {member.name}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await setup_db()
    xp_loop.start()

# COMMAND: Level
@bot.command()
async def level(ctx):
    xp = await get_xp(ctx.author.id)
    path = await generate_rank_card(ctx.author, xp)
    await ctx.send(file=discord.File(path))

# COMMAND: Leaderboard
@bot.command()
async def top(ctx):
    data = await get_top(10)
    path = await generate_leaderboard(data, ctx.guild)
    await ctx.send(file=discord.File(path))

# START BOT
keep_alive()
bot.run(TOKEN)
