import asyncio
import logging

# pip install aiogram==2.25.2
# Выполнить в консоле, если не установлена библиотека
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from handlers.summarization import register_handlers_summarization
from handlers.common import register_handlers_common

TOKEN = "6615597539:AAEpeoic5atmssVltLxNwymFnPf-hDsdTHM"
logger = logging.basicConfig(
        level=logging.INFO,
        filename="bot_log.log",
        format="%(asctime)s %(levelname)s %(lineno)s %(funcName)s %(message)s",
    )



# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Начать"),
        types.BotCommand(command="/summarization", description="Сократить текст"),
        types.BotCommand(command="/cancel", description="Отменить текущее действие"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
   
    bot = Bot(token=TOKEN)

    # Для работы на сервере
    # proxy_url = 'http://proxy.server:3128'
    # bot = Bot(token=TOKEN, proxy=proxy_url)

    dp = Dispatcher(
        bot, storage=MemoryStorage()
    )  # принимает и обрабатывает все обновления

    # Регистрация всех команд бота
    register_handlers_summarization(dp) # сокращатель текста
    register_handlers_common(dp) # стартовые команды

    await set_commands(bot)
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
