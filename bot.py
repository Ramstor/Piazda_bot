import logging
import os
import re

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN", "7881272979:AAEKnpHPz5fT-XhBqJmopaNXOZjjeNDrdro")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Хэндлер на "да" с любыми знаками и пробелами
@dp.message_handler(lambda m: m.text and re.fullmatch(r"(?i)\s*да+\s*[!,.?…]*\s*", m.text.strip()))
async def reply_da(message: types.Message):
    await message.reply("пизда")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

