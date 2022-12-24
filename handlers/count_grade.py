from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers.add_exam import users_data


def register_handlers_count_grade(dp: Dispatcher):
    dp.register_message_handler(count_grade, commands="count_grade", state="*")


def grade_calculator(user_id):
    data = users_data[user_id]
    grade = 0
    for i in data.keys():
        grade += data[i][0] * data[i][1]
    return round(grade, 4)


async def count_grade(msg: types.Message, state: FSMContext):
    await state.finish()
    answer = "Ваша оценка: " + str(grade_calculator(msg.from_user.id))
    await msg.answer(answer)
