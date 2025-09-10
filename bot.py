import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram import F

# Логирование
logging.basicConfig(level=logging.INFO)

# Берём токен из переменной окружения
API_TOKEN = os.getenv("7881272979:AAEKnpHPz5fT-XhBqJmopaNXOZjjeNDrdro")

# Создаём объекты
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хэндлер на слово "да"
@dp.message(F.text.lower() == "да")
async def reply_da(message: types.Message):
    await message.reply("пизда")

# Точка входа
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


