# Discord Leveling Bot

A Discord bot with XP leveling system, rank cards, and leaderboard functionality.

## Features

- **Voice Channel XP**: Users gain XP for being in voice channels
- **Rank Cards**: Beautiful personalized rank cards showing user progress
- **Leaderboard**: Top 10 players displayed with ranks and XP
- **Database**: SQLite database for persistent XP tracking
- **Keep Alive**: Flask server to keep the bot running on hosting platforms like Render

## Project Structure

```
discord-leveling-bot/
├── requirements.txt
├── README.md
└── Discord/
    ├── main.py
    ├── assets/
    │   ├── bg.png
    │   ├── bar_empty.png
    │   └── bar_fill.png
    └── utils/
        ├── rank_card.py
        ├── leaderboard.py
        └── db.py
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Discord bot token as an environment variable:
   ```bash
   export BOT_TOKEN=your_token_here
   ```

4. Add the image assets to `Discord/assets/`:
   - `bg.png` - Background image for rank cards
   - `bar_empty.png` - Empty XP bar
   - `bar_fill.png` - Filled XP bar

## Running the Bot

```bash
python Discord/main.py
```

## Commands

- `!level` - View your rank card
- `!leaderboard` or `!lb` - View the top 10 leaderboard

## Configuration

Edit the following in `Discord/main.py`:

- `VOICE_CHANNEL_NAME` - The voice channel to track XP from
- `XP_PER_MINUTE` - XP awarded per minute in voice channel
- `display_name` - Custom name to display on rank cards

## Database

The bot uses SQLite (`database.db`) to store user XP. The database is automatically created on first run.

### Level Formula

XP needed for next level = 100 × (level²)

- Level 0: 0 XP
- Level 1: 100 XP
- Level 2: 400 XP
- Level 3: 900 XP
- etc.

## Requirements

- Python 3.11+
- discord.py 2.0+
- aiosqlite
- flask
- Pillow
- aiohttp

## License

MIT
