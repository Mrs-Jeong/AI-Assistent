from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from handlers.nlp import summarization

logger = logging.getLogger(__name__)


# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
list_size_names = ["Кратко", "Подробно"]
size_dict = {"Кратко": "short", "Подробно": "long"}


class Reduction(StatesGroup):
    """Создаем этапы/состояния работы машины состояния"""

    waiting_for_size_name = State()
    waiting_for_text = State()


def create_keyboard(list_btn):
    """Создание клавиатуры"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in list_btn:
        keyboard.add(name)
    return keyboard


async def summarization_start(message: types.Message, state: FSMContext):
    await message.answer(
        "Выберите степень сжатия:", reply_markup=create_keyboard(list_size_names)
    )
    await state.set_state(Reduction.waiting_for_size_name.state)
    logger.info(
        f"Пользователь:{message.from_user.username} активировал команду /summarization"
    )


async def summarization_chosen(message: types.Message, state: FSMContext):
    if message.text not in list_size_names:
        await message.answer(
            "Такой команды у нас нет!\nПожалуйста, выберите команду, используя клавиатуру ниже."
        )
        return

    logger.info(f"Пользователь:{message.from_user.username} выбрал: {message.text}")
    await state.update_data(size=message.text)

    await state.set_state(Reduction.waiting_for_text.state)
    await message.answer("Введи текст для сокращения:")


async def summarization_result(message: types.Message, state: FSMContext):

    user_data = await state.get_data()

    result = await summarization(message.text, size_dict[user_data["size"]])

    await message.answer(
        result,
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


def register_handlers_summarization(dp: Dispatcher):
    dp.register_message_handler(
        summarization_start, commands="summarization", state="*"
    )
    dp.register_message_handler(
        summarization_chosen, state=Reduction.waiting_for_size_name
    )
    dp.register_message_handler(summarization_result, state=Reduction.waiting_for_text)
