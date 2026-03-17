import os
import discord
from discord.ext import commands, tasks
import asyncio

# ===============================
# LOAD BOT TOKEN
# ===============================
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN:
    print("✅ BOT_TOKEN loaded")
else:
    print("❌ BOT_TOKEN missing")
    exit()

# ===============================
# LOCAL FILES
# ===============================
from utils.db import Database
from utils.rank_card import generate_rank_card
from utils.leaderboard import generate_leaderboard

# ===============================
# FLASK KEEP ALIVE (Render)
# ===============================
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def home():
    return "OXK Ranking Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()

# ===============================
# DISCORD BOT SETUP
# ===============================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

db = Database("database.db")

# ===============================
# CONFIG
# ===============================
VOICE_CHANNEL_NAME = "Anime"   # XP channel
XP_PER_MINUTE = 0.833

OWNER_ID = 1072737265660465182
PRIVATE_VC_ID = 1477532709638373408

# ===============================
# BOT READY EVENT
# ===============================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    await db.setup()

    # lock private VC when bot starts
    channel = bot.get_channel(PRIVATE_VC_ID)

    if channel:
        everyone = channel.guild.default_role
        await channel.set_permissions(everyone, connect=False)
        print("🔒 Private VC locked")

    if not voice_xp_loop.is_running():
        voice_xp_loop.start()

# ===============================
# VOICE XP LOOP
# ===============================
@tasks.loop(minutes=1)
async def voice_xp_loop():

    await bot.wait_until_ready()

    if not bot.guilds:
        return

    guild = bot.guilds[0]

    channel = discord.utils.get(guild.voice_channels, name=VOICE_CHANNEL_NAME)

    if not channel:
        print("❌ Anime voice channel not found")
        return

    for member in channel.members:

        if member.bot:
            continue

        await db.add_xp(member.id, XP_PER_MINUTE)

        print(f"🎉 XP given → {member.name}")

# ===============================
# PRIVATE VOICE LOCK SYSTEM
# ===============================
@bot.event
async def on_voice_state_update(member, before, after):

    channel = bot.get_channel(PRIVATE_VC_ID)

    if channel is None:
        return

    everyone = channel.guild.default_role

    # OWNER JOINS → unlock VC
    if member.id == OWNER_ID and after.channel == channel:

        await channel.set_permissions(everyone, connect=True)

        print("🔓 Private VC unlocked")

    # OWNER LEAVES → kick members & lock VC
    if member.id == OWNER_ID and before.channel == channel and after.channel != channel:

        for m in channel.members:
            await m.move_to(None)

        await channel.set_permissions(everyone, connect=False)

        print("🔒 Private VC locked")

# ===============================
# COMMAND: !level
# ===============================
@bot.command()
async def level(ctx):

    try:
        xp, level, next_xp = await db.get_user_progress(ctx.author.id)

        file = await generate_rank_card(
            user=ctx.author,
            xp=xp,
            level=level,
            next_xp=next_xp,
            display_name="OXK"
        )

        await ctx.send(file=file)

    except Exception as e:
        print("❌ level error:", e)
        await ctx.send("Error generating rank card")

# ===============================
# COMMAND: !leaderboard
# ===============================
@bot.command(aliases=["lb"])
async def leaderboard(ctx):

    try:
        file = await generate_leaderboard(ctx.guild, db)

        await ctx.send(file=file)

    except Exception as e:
        print("❌ leaderboard error:", e)
        await ctx.send("Error generating leaderboard")

# ===============================
# START BOT
# ===============================
keep_alive()

bot.run(TOKEN)
