# main_db.py
import sqlite3
from db import queries

db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()


async def create_tables():
    if db:
        print('База данных подключена!')

    cursor.execute(queries.CREATE_TABLE_store)
    cursor.execute(queries.CREATE_TABLE_store_details)


async def sql_insert_store(name_product, price, size, product_id, photo):
    cursor.execute(queries.INSERT_store_query,
                   (name_product, price, size, product_id, photo))
    db.commit()


async def sql_insert_store_details(category, product_id):
    cursor.execute(queries.INSERT_store_details_query,
                   (category, product_id))
    db.commit()

