import logging
from aiogram import Bot, Dispatcher, executor, types
import os

# Берём токен из переменных окружения (удобно для хостинга)
API_TOKEN = os.getenv("7881272979:AAEKnpHPz5fT-XhBqJmopaNXOZjjeNDrdro")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(lambda message: message.text and message.text.strip().lower() == "да")
async def reply_da(message: types.Message):
    await message.reply("пизда")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

