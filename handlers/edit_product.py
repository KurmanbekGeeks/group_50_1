# edit_product.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from db import main_db


class EditProduct(StatesGroup):
    for_field = State()
    for_new_photo = State()
    for_new_field = State()



async def start_send_products(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button_all = InlineKeyboardButton('Вывести все товары',
                                      callback_data='all_edit')
    button_one = InlineKeyboardButton('Вывести по одному',
                                      callback_data='one_edit')

    keyboard.add(button_all, button_one)

    await message.answer('Выберите каким образом хотите просмотреть товары:',
                         reply_markup=keyboard)


async def send_all_products(call: types.CallbackQuery):
    products = main_db.fetch_all_products()

    if products:
        for product in products:

            caption = (f'Название товара - {product["name_product"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Размер - {product["size"]}\n'
                       f'Артикул - {product["product_id"]}\n'
                       f'Цена - {product["price"]}\n')

            keyboard = InlineKeyboardMarkup()
            button_edit = InlineKeyboardButton('Редактировать',
                                            callback_data=f'edit_{product["product_id"]}')
            keyboard.add(button_edit)

            await call.message.answer_photo(product["photo"], caption=caption,
                                       reply_markup=keyboard)

    else:
        await call.message.answer('Товар нет!')


async def edit_product(call: types.CallbackQuery, state: FSMContext):
    product_id = call.data.split('_')[1]
    print(product_id)

    await state.update_data(product_id=product_id)

    keyboard = InlineKeyboardMarkup(row_width=2)

    name_button = InlineKeyboardButton(text="Название", callback_data="field_name_product")
    category_button = InlineKeyboardButton(text="Категория", callback_data="field_category")
    price_button = InlineKeyboardButton(text="Цена", callback_data="field_price")
    size_button = InlineKeyboardButton(text="Размер", callback_data="field_size")
    photo_button = InlineKeyboardButton(text="Фото", callback_data="field_photo")
    keyboard.add(name_button, category_button, price_button, size_button, photo_button)

    await call.message.answer('Выберите поле для редактирования:',
                              reply_markup=keyboard)

    await EditProduct.for_field.set()


async def select_field_product(call: types.CallbackQuery, state: FSMContext):

    field_map = {
        'field_name_product': 'name_product',
        'field_category': 'category',
        'field_price': 'price',
        'field_size': 'size',
        'field_photo': 'photo'
    }

    field = field_map.get(call.data)

    if not field:
        await call.message.answer('Недопустимое поле')
        return

    await state.update_data(field=field)

    if field == 'photo':
        await EditProduct.for_new_photo.set()
        await call.message.answer('Отправьте новое фото:')
    else:
        await EditProduct.for_new_field.set()
        await call.message.answer('Отправьте новое значение:')



async def set_new_value(message: types.Message, state: FSMContext):
    user_data = await state.get_data()

    product_id = user_data['product_id']
    field = user_data['field']

    new_value = message.text

    main_db.update_product_field(product_id, field, new_value)

    await message.answer(f'Поле {field} успешно обновлено!\n'
                         f'Обновите список')

    await state.finish()


async def set_new_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    product_id = user_data['product_id']

    photo_id = message.photo[-1].file_id


    main_db.update_product_field(product_id, 'photo', photo_id)

    await message.answer('Фото успешно обновлено!\n'
                         'Обновите список!')
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands='send_edit')
    dp.register_callback_query_handler(send_all_products, Text(equals='all_edit'))
    dp.register_callback_query_handler(edit_product, Text(startswith='edit_'))
    dp.register_callback_query_handler(select_field_product, Text(startswith='field_'),
                                       state=EditProduct.for_field)
    dp.register_message_handler(set_new_value, state=EditProduct.for_new_field)
    dp.register_message_handler(set_new_photo, state=EditProduct.for_new_photo,
                                content_types=['photo'])