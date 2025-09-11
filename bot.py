import logging
import os
import re
import asyncio
from datetime import datetime, time, timedelta
from aiogram import Bot, Dispatcher, executor, types


logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN", "7881272979:AAEKnpHPz5fT-XhBqJmopaNXOZjjeNDrdro")
TIMEZONE = os.getenv("TIMEZONE") or "Europe/Amsterdam"


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Хэндлер на "да" с любыми знаками и пробелами
@dp.message_handler(lambda m: m.text and re.fullmatch(r"(?i)\s*да+\s*[),!,.?…]*\s*", m.text.strip()))
async def reply_da(message: types.Message):
    await message.reply("пязда")
    
# chat_id будем хранить в памяти
chat_id: int | None = None

def seconds_until(target: time) -> int:
    """Сколько секунд ждать до следующего target времени"""
    now = datetime.now()
    today_target = datetime.combine(now.date(), target)
    if now >= today_target:
        today_target += timedelta(days=1)
    return int((today_target - now).total_seconds())

async def scheduler():
    global chat_id
    while True:
        if chat_id:
            # ждём до 9:00
            await asyncio.sleep(seconds_until(time(10, 0)))
            if datetime.now().weekday() < 5:  # Пн=0 ... Пт=4
                await bot.send_message(chat_id, "Всем хорошего рабочего дня")

            # ждём до 18:00
            await asyncio.sleep(seconds_until(time(18, 0)))
            if datetime.now().weekday() < 5:
                await bot.send_message(chat_id, "Можно домой")
        else:
            # если чат ещё не зарегистрирован — проверяем каждые 10 секунд
            await asyncio.sleep(10)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Используй команду /register, чтобы зарегистрировать чат.\n"
        "Я буду писать сюда только по будням в 09:00 и 18:00."
    )

@dp.message_handler(commands=["register"])
async def cmd_register(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    await message.reply(f"Этот чат зарегистрирован (chat_id = {chat_id}).")

@dp.message_handler(commands=["status"])
async def cmd_status(message: types.Message):
    if chat_id:
        await message.reply(f"Сейчас зарегистрирован chat_id: {chat_id}")
    else:
        await message.reply("Чат ещё не зарегистрирован.")

async def on_startup(dp):
    asyncio.create_task(scheduler())

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

