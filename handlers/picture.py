from aiogram import Dispatcher, types


# @dp.message_handler(commands=['pic'])
async def send_photo(message: types.Message):
    with open("images/cat.jpg", "rb") as photo:
        await message.answer_photo(photo, caption="Серьезное лицо")
        # await message.reply_photo(photo, caption="Серьезное лицо")
        # await message.bot.send_photo(message.chat.id, photo)


def register_handlers(dp):
    dp.register_message_handler(send_photo, commands=["pic"])
