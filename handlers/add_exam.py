from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


users_data = dict()


def register_handlers_add_exam(dp: Dispatcher):
    dp.register_message_handler(add_exam, commands="add_exam", state="*")
    # dp.register_message_handler(add_preset, commands="add_preset", state="*")
    # dp.register_message_handler(get_disc_name, state=SetPreset.get_discipline_name)
    dp.register_message_handler(catch_exam_name, state=SetExam.set_name)
    dp.register_message_handler(catch_exam_weight, state=SetExam.set_weight)
    dp.register_message_handler(catch_exam_grade, state=SetExam.set_grade)


class SetExam(StatesGroup):
    set_name = State()
    set_weight = State()
    set_grade = State()


# class SetPreset(StatesGroup):
#     get_discipline_name = State()
#     matan = State()
#     teorver = State()
#     akos = State()
#     ipr = State()
#     getting_grades = State()
#
#
# async def add_preset(msg: types.Message, state: FSMContext):
#     await msg.answer("Введите номер выбранного предмета (скопируйте название и отправьте боту):\n" +
#                      "1. Математический анализ\n" +
#                      "2. Теория вероятностей\n" +
#                      "3. Архитектура компьютеров и операционные системы\n" +
#                      "4. Инструменты промышленной разработки\n")
#     await state.set_state(SetPreset.get_discipline_name.state)
#
#
# async def get_disc_name(msg: types.Message, state: FSMContext):
#     match msg.text:
#         case "1":
#             await state.set_state(SetPreset.matan.state)
#         case "2":
#             await state.set_state(SetPreset.teorver.state)
#         case "3":
#             await state.set_state(SetPreset.akos.state)
#         case "4":
#             await state.set_state(SetPreset.ipr.state)
#         case _:
#             await msg.answer("Введите число в диапазоне 1-4")


# async def get_grade_preset(msg: types.Message):
#     if 0 <= int(msg.text) <= 10:
#         return int(msg.text)
#     else:
#         await msg.answer("Введите число от 0 до 10")
#         return -1

#
# async def matan_grade(msg: types.Message, state: FSMContext):
#     await msg.answer("Выбран предмет математический анализ, ")


async def add_exam(msg: types.Message, state: FSMContext):
    await msg.answer("Введите название элемента контроля")
    await state.set_state(SetExam.set_name.state)


async def catch_exam_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
        user_message = data['name']
        users_data[msg.from_user.id][user_message] = list()
        await msg.answer("Введите вес элемента контроля в виде десятичной дроби (например, 0.25)")

    # Finish conversation
    await state.set_state(SetExam.set_weight.state)


async def catch_exam_weight(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if float(msg.text) > 1.0:
                raise ValueError
            users_data[msg.from_user.id][data['name']].append(float(msg.text))
            await msg.answer("Введите оценку за элемент контроля")
            await state.set_state(SetExam.set_grade.state)
        except ValueError:
            await msg.answer("Слишком большой коэффициент, (" + str(float(msg.txt)) + " > 1.0" + ")")
        except:
            await msg.answer("Неправильный ввод, попробуйте снова")



    # Finish conversation



async def catch_exam_grade(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if float(msg.text) > 10.0:
                raise ValueError
            users_data[msg.from_user.id][data['name']].append(float(msg.text))
            await msg.answer("Элемент контроля успешно добавлен!")
        except:
            await msg.answer("Неправильный ввод, попробуйте снова")
    # Finish conversation
    await state.finish()  # закончили работать с сотояниями
