import aiosqlite

async def setup_db():
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                xp REAL DEFAULT 0
            )
        """)
        await db.commit()

async def add_xp(user_id, amount):
    async with aiosqlite.connect("database.db") as db:
        await db.execute("""
            INSERT INTO users (user_id, xp) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET xp = xp + ?
        """, (user_id, amount, amount))
        await db.commit()

async def get_xp(user_id):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT xp FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_top(limit=10):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT user_id, xp FROM users ORDER BY xp DESC LIMIT ?", (limit,)) as cursor:
            return await cursor.fetchall()
