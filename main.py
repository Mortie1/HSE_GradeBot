from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncio import run

from aiogram.types import BotCommand

from handlers.add_exam import register_handlers_add_exam
from handlers.common import register_handlers_common
from handlers.count_grade import register_handlers_count_grade
from util.config import TOKEN


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Доступные команды"),
        BotCommand(command="/add_exam", description="Добавить экзамен"),
        BotCommand(command="/clear", description="Удалить все элементы контроля"),
        BotCommand(command="/count_grade", description="Посчитать оценку"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров

    register_handlers_add_exam(dp)
    register_handlers_common(dp)
    register_handlers_count_grade(dp)


    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == '__main__':
    run(main())






# @dp.message_handler(commands=['data'])
# async def print_data(msg: types.Message):
#     await bot.send_message(msg.from_user.id, str(users_data[msg.from_user.id]))

