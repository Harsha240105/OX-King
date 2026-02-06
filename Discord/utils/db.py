import aiosqlite
import math

class Database:
    def __init__(self, path):
        self.path = path

    # ===============================
    # Setup database table
    # ===============================
    async def setup(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS levels (
                    user_id INTEGER PRIMARY KEY,
                    xp REAL DEFAULT 0
                )
            """)
            await db.commit()

    # ===============================
    # Add XP to a user
    # ===============================
    async def add_xp(self, user_id, amount):
        async with aiosqlite.connect(self.path) as db:
            await db.execute("""
                INSERT INTO levels (user_id, xp)
                VALUES (?, ?)
                ON CONFLICT(user_id)
                DO UPDATE SET xp = xp + ?
            """, (user_id, amount, amount))
            await db.commit()

    # ===============================
    # Get XP for a user
    # ===============================
    async def get_xp(self, user_id):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT xp FROM levels WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    # ===============================
    # Level formula (Option C):
    # XP needed = 100 × (level²)
    # ===============================
    def xp_to_level(self, xp):
        level = int(math.sqrt(xp / 100))
        next_level_xp = 100 * ((level + 1) ** 2)
        return level, next_level_xp

    # ===============================
    # Full progress data (xp, level, next xp)
    # ===============================
    async def get_user_progress(self, user_id):
        xp = await self.get_xp(user_id)
        level, next_xp = self.xp_to_level(xp)
        return xp, level, next_xp

    # ===============================
    # Get top 10 leaderboard
    # ===============================
    async def get_leaderboard(self, limit=10):
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("""
                SELECT user_id, xp
                FROM levels
                ORDER BY xp DESC
                LIMIT ?
            """, (limit,)) as cursor:
                rows = await cursor.fetchall()
                return rows
