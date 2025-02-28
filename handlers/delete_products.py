# delete_products.py
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import main_db
from aiogram.types import InputMediaPhoto



async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_all = types.InlineKeyboardButton('Вывести все товары',
                                            callback_data='delete_all')
    button_one = types.InlineKeyboardButton('Вывести по одному',
                                            callback_data='delete_one')
    keyboard.add(button_all, button_one)

    await message.answer('Выберите как просмотреть товары:',
                         reply_markup=keyboard)


async def send_all_products(call: types.CallbackQuery):
    products = main_db.fetch_all_products()

    if products:
        for product in products:

            caption = (f'Название товара - {product["name_product"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Размер - {product["size"]}\n'
                       f'Цена - {product["price"]}\n')


            keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(
                "Удалить", callback_data=f'delete_{product["product_id"]}'))


            await call.message.answer_photo(photo=product["photo"],
                                            caption=caption,
                                            reply_markup=keyboard)

    else:
        await call.message.answer('База пуста! Товаров нет.')


async def delete_all_products(call: types.CallbackQuery):
    product_id = call.data.split('_')[1]

    main_db.delete_product(product_id)

    new_caption = 'Товар удален! Обновите список!'

    if call.message.photo:

        photo_404 = open('images/images.png', 'rb')

        await call.message.edit_media(
            InputMediaPhoto(media=photo_404, caption=new_caption)
        )
    else:
        await call.message.edit_text(new_caption)




def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands='send_delete')
    dp.register_callback_query_handler(send_all_products,
                                       Text(equals="delete_all"))

    dp.register_callback_query_handler(delete_all_products,
                                       Text(startswith="delete_"))