from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_config import database


# FSM - finite state machine
class Complaint(StatesGroup):
    name = State()
    age = State()
    text = State()


async def start_dialog(callback: CallbackQuery):
    await Complaint.name.set()
    await callback.message.answer("Как вас зовут")


async def stop_dialog(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Спасибо за потраченное время")


async def process_name(message: Message, state: FSMContext):
    name = message.text
    async with state.proxy() as data:
        data["name"] = name
    await Complaint.next()
    await message.answer("Сколько Вам лет")


async def process_age(message: Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Введите число")
        return
    age = int(age)
    if age < 10 or age > 90:
        await message.answer("Неподходящий возраст")
        return
    async with state.proxy() as data:
        data["age"] = message.text
    await Complaint.next()
    await message.answer("Какая у вас жалоба?")


async def process_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
    data = await state.get_data()
    # print(data) # {'name': 'ccc', 'age': 21, 'text': 'fdsfdsfds'}
    database.add_complaint(data)
    await message.answer("Спасибо за отзыв.")
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(start_dialog, lambda c: c.data == "complaint")
    dp.register_message_handler(
        stop_dialog, Text(equals=("стоп", "stop"), ignore_case=True), state="*"
    )
    dp.register_message_handler(process_name, state=Complaint.name)
    dp.register_message_handler(process_age, state=Complaint.age)
    dp.register_message_handler(process_text, state=Complaint.text)
