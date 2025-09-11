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
    
# список чатов
chat_ids: set[int] = set()


def seconds_until(target: time) -> int:
    """Сколько секунд ждать до следующего target времени"""
    now = datetime.now()
    today_target = datetime.combine(now.date(), target)
    if now >= today_target:
        today_target += timedelta(days=1)
    return int((today_target - now).total_seconds())


async def scheduler():
    global chat_ids
    while True:
        now = datetime.now()
        weekday = now.weekday()

        if weekday < 5 and chat_ids:  # только Пн–Пт
            # если ещё не 9:00 → ждём до 9:00 и шлём сообщение
            if now.time() < time(9, 0):
                await asyncio.sleep(seconds_until(time(9, 0)))
                for cid in chat_ids:
                    await bot.send_message(cid, "Всем хорошего рабочего дня")

            # если уже после 9:00, но до 18:00 → ждём до 18:00
            elif now.time() < time(18, 0):
                await asyncio.sleep(seconds_until(time(18, 0)))
                for cid in chat_ids:
                    await bot.send_message(cid, "Можно домой")

        # ждём до следующего дня 00:00
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0, 0))
        await asyncio.sleep((tomorrow - now).total_seconds())


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.reply(
        "Привет! Используй команду /register, чтобы зарегистрировать этот чат.\n"
        "Я буду писать сюда по будням в 09:00 и 18:00.\n"
        "Команда /status покажет список зарегистрированных чатов."
    )


@dp.message_handler(commands=["register"])
async def cmd_register(message: types.Message):
    global chat_ids
    chat_ids.add(message.chat.id)
    await message.reply(f"Чат зарегистрирован (chat_id = {message.chat.id}).")


@dp.message_handler(commands=["status"])
async def cmd_status(message: types.Message):
    if chat_ids:
        text = "Сейчас зарегистрированы чаты:\n" + "\n".join(map(str, chat_ids))
    else:
        text = "Пока нет зарегистрированных чатов."
    await message.reply(text)


async def on_startup(dp):
    asyncio.create_task(scheduler())

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)


