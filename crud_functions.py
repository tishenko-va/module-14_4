import sqlite3


def get_connection():
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Products')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        )
        ''')

    for i in range(1, 5):
        cursor.execute(
            "INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   (f"Product{i}", f"Описание{i}", f"{i * 100}")
        )
    connection.commit()
    connection.close()
    return sqlite3.connect('initiate.db')

def get_all_products():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT title, description, price FROM Products")
        all_products = cursor.fetchall()
        return all_products
    finally:
        connection.close()

result = get_all_products()
print(result)
