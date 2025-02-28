# admin_group.py
from token import AWAIT

from aiogram import types, Dispatcher
from bot_config import ADMINS, bot


async def welcome_user(message: types.Message):
    for member in message.new_chat_members:
        await message.answer(f'Добро пожаловать! {member.full_name}\n\n'
                             f'Просим ознакомиться с правилами нашей группы✨\n'
                             f'* Не материться\n'
                             f'* Не спамить\n'
                             f'* Не рекламировать 🏳️‍🌈\n'
                             f'* Не обсуждать политику')

user_warnings = {}


async def user_warning(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id not in ADMINS:
            await message.answer('Недостаточно прав! Обратитесь к админу!')
        elif not message.reply_to_message:
            await message.answer('Команда должна быть ответом на сообщение!')
        else:
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.full_name
            user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

            for admin in ADMINS:
                await bot.send_message(chat_id=admin,
                                       text=f'{user_name} получил предупреждение ({user_warnings[user_id]}/3)')

                if user_warnings[user_id] >= 3:
                    await bot.kick_chat_member(message.chat.id, user_id)
                    await bot.unban_chat_member(message.chat.id, user_id)

                    await bot.send_message(chat_id=message.chat.id,
                                           text=f'{user_name} был удален из группы за превышение кол-ва предупреждений!')


                    await bot.send_message(chat_id=admin,
                                           text=f'{user_name} был удален из группы за превышение кол-ва предупреждений!')




def register_handlers(dp: Dispatcher):
    dp.register_message_handler(welcome_user, content_types=[types.ContentType.NEW_CHAT_MEMBERS])
    dp.register_message_handler(user_warning, commands='warn')