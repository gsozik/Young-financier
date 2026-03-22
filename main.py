import asyncio
from aiogram import Bot, Dispatcher

from bot.app import router
from settings import bot_api_key


async def main():
    bot = Bot(token=bot_api_key)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())