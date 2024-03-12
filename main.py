import logging
import sys
from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN
from handlers.admin_handler import router

async def main():

    bot = Bot(token=TOKEN)

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())