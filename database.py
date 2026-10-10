import sqlite3


def connect_db():
    connection = sqlite3.connect("library.db")
    return connection


def create_tables():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            available INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            issue_date TEXT,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        )
    """)

    connection.commit()
    connection.close()