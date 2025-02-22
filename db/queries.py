# queries.py

CREATE_TABLE_store = """
    CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    price TEXT,
    size TEXT,
    product_id TEXT,
    photo TEXT
    )
"""

CREATE_TABLE_store_details = """
    CREATE TABLE IF NOT EXISTS store_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    product_id TEXT
    )
"""


INSERT_store_query = """
    INSERT INTO store (name_product, price, size, product_id, photo)
    VALUES (?, ?, ?, ?, ?)
"""

INSERT_store_details_query = """
    INSERT INTO store_details (category, product_id)
    VALUES (?, ?)
"""