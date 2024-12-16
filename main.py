import asyncio
import configparser
import logging
from aiogram import Bot, Dispatcher
from bot_module.handlers import start_handler

config = configparser.ConfigParser()
config.read("CONFIG.ini")
tg_token = config["Passwords"]["TG_token"]
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=tg_token)
# Диспетчер
dp = Dispatcher()
dp.include_routers(start_handler.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
