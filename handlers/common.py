from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.add_exam import users_data


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    dp.register_message_handler(cmd_clear, commands="clear", state="*")


async def cmd_start(msg: types.Message, state: FSMContext):
    await state.finish()
    if not (msg.from_user.id in users_data):
        users_data[msg.from_user.id] = dict()
    await msg.answer(
        "Напишите /help чтобы просмотреть доступные команды",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_help(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer("/help - список команд\n" +
                     "/cancel - отменить текущее действие\n" +
                     "/add_exam - добавить элемент контроля\n" +
                     "/count_grade - посчитать оценку\n" + 
                     "/clear - удалить все элементы контроля")


async def cmd_clear(msg: types.Message, state: FSMContext):
    await state.finish()
    users_data[msg.from_user.id].clear()
    await msg.answer("Оценка очищена")


async def cmd_cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
