import sqlite3


class Database:
    def __init__(self, path):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS complaints(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    text TEXT
                )        
            """)
            conn.commit()

    def add_complaint(self, data: dict):
        print(data)
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO complaints (name, age, text) VALUES (?, ?, ?)
            """,
                (data["name"], data["age"], data["text"]),
            )
            conn.commit()
