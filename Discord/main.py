from flask import Flask
from threading import Thread

# -------------------------------
# KEEP ALIVE SERVER
# -------------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


# -------------------------------
# IMPORTS
# -------------------------------
import os
import discord
from discord.ext import tasks, commands
import aiosqlite
import asyncio


# -------------------------------
# CONFIG
# -------------------------------
TOKEN = os.getenv("BOT_TOKEN")      # Load token safely from Render environment
VOICE_CHANNEL_NAME = "Anime"        # Channel to track XP in
XP_PER_MINUTE = 0.833               # XP given per minute


# -------------------------------
# INTENTS
# -------------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


# -------------------------------
# DATABASE
# -------------------------------
async def setup_db():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS levels (
                user_id INTEGER PRIMARY KEY,
                xp REAL DEFAULT 0
            )
        """)
        await db.commit()

async def add_xp(user_id, amount):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            INSERT INTO levels (user_id, xp) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET xp = xp + ?
        """, (user_id, amount, amount))
        await db.commit()

async def get_level(user_id):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT xp FROM levels WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return round(row[0], 2)
            return 0


# -------------------------------
# XP LOOP
# -------------------------------
@tasks.loop(minutes=1)
async def voice_xp_loop():
    await bot.wait_until_ready()

    if not bot.guilds:
        print("Bot not in server yet.")
        return

    guild = bot.guilds[0]
    channel = discord.utils.get(guild.voice_channels, name=VOICE_CHANNEL_NAME)

    if not channel:
        print(f"Voice channel '{VOICE_CHANNEL_NAME}' not found.")
        return

    for member in channel.members:
        if not member.bot:
            await add_xp(member.id, XP_PER_MINUTE)
            print(f"Gave {XP_PER_MINUTE} XP to {member.name}")


# -------------------------------
# EVENTS
# -------------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await setup_db()
    voice_xp_loop.start()


# -------------------------------
# COMMANDS
# -------------------------------
@bot.command()
async def level(ctx):
    xp = await get_level(ctx.author.id)
    await ctx.send(f"**{ctx.author.name}**, your level is: **{xp}** 🎉")


# -------------------------------
# START BOT (FINAL LINE ONLY)
# -------------------------------
keep_alive()   # Start flask server
bot.run(TOKEN) # Start Discord bot
