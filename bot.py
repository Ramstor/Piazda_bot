import logging
from aiogram import Bot, Dispatcher, executor, types
import os

# Берём токен из переменных окружения (удобно для хостинга)
API_TOKEN = os.getenv("BOT_TOKEN", "7881272979:AAEKnpHPz5fT-XhBqJmopaNXOZjjeNDrdro")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message(F.text.regexp(r"(?i)^да$"))
async def reply_da(message: types.Message):
    await message.reply("пязда")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

