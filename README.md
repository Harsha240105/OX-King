Discord Leveling & Voice Control Bot

A powerful **Discord bot featuring a voice XP leveling system, rank cards, leaderboard, and a private voice channel lock system.

The bot rewards users for being active in voice channels and provides visual rank cards and leaderboards to track progress.

Features
🎙 Voice Channel XP

Users earn XP automatically while staying in a selected voice channel.

🏆 Rank Cards

Generate personalized rank cards showing:

Level

Current XP

Progress to next level

📊 Leaderboard

Display the Top 10 users in the server ranked by XP.

🔒 Private Voice Channel Lock

A special voice channel behaves like this:

Situation	Result
Owner joins VC	Channel unlocks
Members join	Allowed
Owner leaves	All users kicked + channel locks

Members can see the channel but cannot join until the owner joins.

💾 Persistent Database

Uses SQLite to permanently store XP data.

☁ Hosting Friendly

Includes a Flask keep-alive server so the bot stays online on hosting platforms like Render.

Project Structure
## Project Structure

```
discord-leveling-bot/
│
├── requirements.txt
├── README.md
│
└── Discord/
    ├── main.py
    │
    ├── assets/
    │   ├── bg.png
    │   ├── bar_empty.png
    │   └── bar_fill.png
    │
    └── utils/
        ├── db.py
        ├── rank_card.py
        └── leaderboard.py
```
Installation

1️⃣ Clone the repository
git clone https://github.com/yourusername/discord-leveling-bot.git
cd discord-leveling-bot

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add your bot token

Create an environment variable:

Linux / Mac:

export BOT_TOKEN=your_discord_bot_token

Windows:

set BOT_TOKEN=your_discord_bot_token
4️⃣ Add image assets

Place the following files inside:

Discord/assets/

Required files:

File	Purpose
bg.png	Rank card background
bar_empty.png	XP bar background
bar_fill.png	XP progress bar
Running the Bot

Start the bot using:

python Discord/main.py
Commands
Command	Description
!level	Show your rank card
!leaderboard	Show the top 10 users
!lb	Shortcut for leaderboard
Configuration

You can edit important settings inside:

Discord/main.py

Example configuration:

VOICE_CHANNEL_NAME = "Anime"
XP_PER_MINUTE = 0.833

OWNER_ID = your_discord_user_id
PRIVATE_VC_ID = your_private_voice_channel_id
How to Add User ID and Voice Channel ID

To use the Private Voice Channel Lock system, you must add your Discord User ID and Voice Channel ID.

1️⃣ Get Your Discord User ID

Enable Developer Mode in **Discord.

Steps:

Open User Settings ⚙️

Go to Advanced

Enable Developer Mode

Then:

Go to your server

Right-click your username

Click Copy User ID

Example:

1072737265660465182
2️⃣ Get Voice Channel ID

Right-click the voice channel

Click Copy Channel ID

Example:

1477532709638373408
3️⃣ Add IDs in main.py

Open:

Discord/main.py

Find the CONFIG section:

# ===============================
# CONFIG
# ===============================

VOICE_CHANNEL_NAME = "Anime"
XP_PER_MINUTE = 0.833

OWNER_ID = 1072737265660465182
PRIVATE_VC_ID = 1477532709638373408

Replace with your own IDs if needed.

How the Private Voice Channel System Works
Action	Result
You join the private VC	Channel unlocks
Members join	Allowed
You leave the VC	Everyone gets kicked
Channel locks again	Nobody can join

Members can see the voice channel but cannot join until you join it.

Required Bot Permissions

Make sure your bot role has these permissions:

Move Members

Manage Channels

View Channel

Connect

Without these permissions the system will not work.

Database

The bot stores XP inside:

database.db

The database is automatically created on the first run.

Level System

XP required for each level follows this formula:

XP required = 100 × (level²)

Example:

Level	XP Required
Level 1	100 XP
Level 2	400 XP
Level 3	900 XP
Level 4	1600 XP
Requirements

Python 3.11+

discord.py 2.0+

aiosqlite

Flask

Pillow

aiohttp

Install all requirements using:

pip install -r requirements.txt
Hosting

This bot works well on:

Render

Railway

VPS servers

Replit (with uptime monitor)

Future Improvements

Possible upgrades:

Message XP system

Slash commands

Level role rewards

Web dashboard

Server configuration panel

License

This project is open-source and available for personal or educational use.

## License

MIT
