import aiosqlite, asyncio

async def async_fetch_users():
  async with aiosqlite.connect("ALX_prodev.db") as db:
     async with db.execute("SELECT * FROM users") as cursor:
        async for row in cursor:
          return await cursor.fetchall()

async def async_fetch_older_users():
  async with aiosqlite.connect("ALX_prodev.db") as db:
     async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
        async for row in cursor:
          return await cursor.fetchall()


async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

asyncio.run(fetch_concurrently())
