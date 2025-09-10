import logging
import os
import re
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo
from pathlib import Path

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("BOT_TOKEN", "7881272979:AAEKnpHPz5fT-XhBqJmopaNXOZjjeNDrdro")
TIMEZONE = os.getenv("TIMEZONE") or "Europe/Amsterdam"
# Файл для хранения chat_id (простая "персистентность")
CHAT_ID_FILE = Path("chat_id.txt")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler(timezone=ZoneInfo(TIMEZONE))

# Хэндлер на "да" с любыми знаками и пробелами
@dp.message_handler(lambda m: m.text and re.fullmatch(r"(?i)\s*да+\s*[),!,.?…]*\s*", m.text.strip()))
async def reply_da(message: types.Message):
    await message.reply("пязда")
    
    def save_chat_id(chat_id: int):
    CHAT_ID_FILE.write_text(str(chat_id))

def load_chat_id() -> int | None:
    if CHAT_ID_FILE.exists():
        try:
            return int(CHAT_ID_FILE.read_text().strip())
        except Exception:
            return None
    return None

async def send_good_morning():
    chat_id = load_chat_id()
    if not chat_id:
        print("No chat_id saved — пропускаем отправку 'Всем хорошего рабочего дня'")
        return
    try:
        await bot.send_message(chat_id, "Всем хорошего рабочего дня")
        print("Sent morning message to", chat_id)
    except Exception as e:
        print("Ошибка при отправке morning:", e)

async def send_home_time():
    chat_id = load_chat_id()
    if not chat_id:
        print("No chat_id saved — пропускаем отправку 'Можно домой'")
        return
    try:
        await bot.send_message(chat_id, "Можно домой")
        print("Sent evening message to", chat_id)
    except Exception as e:
        print("Ошибка при отправке evening:", e)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    text = (
        "Привет! Я бот, который отправляет сообщения в 9:00 и 18:00.\n\n"
        "Команды:\n"
        "/register — зарегистрировать этот чат для рассылки (бот будет отправлять в этот чат)\n"
        "/unregister — удалить регистрацию\n"
        "/status — показать текущий зарегистрированный chat_id\n"
    )
    await message.reply(text)

@dp.message_handler(commands=["register"])
async def cmd_register(message: types.Message):
    chat_id = message.chat.id
    save_chat_id(chat_id)
    await message.reply(f"Готово — этот чат зарегистрирован (chat_id = {chat_id}). Буду писать сюда в 09:00 и 18:00.")

@dp.message_handler(commands=["unregister"])
async def cmd_unregister(message: types.Message):
    if CHAT_ID_FILE.exists():
        CHAT_ID_FILE.unlink()
        await message.reply("Регистрация удалена.")
    else:
        await message.reply("Чат не был зарегистрирован.")

@dp.message_handler(commands=["status"])
async def cmd_status(message: types.Message):
    chat_id = load_chat_id()
    if chat_id:
        await message.reply(f"Зарегистрированный chat_id: {chat_id}")
    else:
        await message.reply("Пока нет зарегистрированного чата.")

async def on_startup(dp):
    # добавить задания cron: 09:00 и 18:00 в указанной TIMEZONE
    # CronTrigger(hour=9, minute=0) и hour=18
    scheduler.add_job(lambda: asyncio.create_task(send_good_morning()),
                      trigger=CronTrigger(hour=9, minute=0, timezone=ZoneInfo(TIMEZONE)))
    scheduler.add_job(lambda: asyncio.create_task(send_home_time()),
                      trigger=CronTrigger(hour=18, minute=0, timezone=ZoneInfo(TIMEZONE)))
    scheduler.start()
    print("Scheduler started with timezone:", TIMEZONE)
    # можно логировать текущий зарегистрированный chat_id
    print("Registered chat_id:", load_chat_id())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

