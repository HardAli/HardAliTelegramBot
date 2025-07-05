import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from bot.database.db import init_db
from bot.handlers import admin, user

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]

admin.ADMIN_IDS.extend(ADMIN_IDS)

dp = Dispatcher()

dp.include_router(user.router)
dp.include_router(admin.router)

async def main():
    await init_db()
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())