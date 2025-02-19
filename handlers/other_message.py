from aiogram import Dispatcher, types


# @dp.message_handler()
async def echo_handler(message):
    text = message.text  # текст ссобщения
    # await message.answer("Я вас не понимаю")
    await message.reply("Я вас не понимаю")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_handler)
