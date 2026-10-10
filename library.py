from database import connect_db
from datetime import date


def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    category = input("Enter category: ").strip()

    if not title or not author:
        print("Title and author cannot be empty.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO books (title, author, category)
        VALUES (?, ?, ?)
    """, (title, author, category))

    connection.commit()
    connection.close()

    print("Book added successfully!")


def view_books():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT book_id, title, author, category, available
        FROM books
    """)

    books = cursor.fetchall()
    connection.close()

    if not books:
        print("No books found.")
        return

    print("\n--- Book List ---")

    for book in books:
        status = "Available" if book[4] == 1 else "Issued"

        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Category: {book[3]} | "
            f"Status: {status}"
        )


def search_book():
    keyword = input("Enter book title or author to search: ").strip()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT book_id, title, author, category, available
        FROM books
        WHERE title LIKE ? OR author LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    books = cursor.fetchall()
    connection.close()

    if not books:
        print("No matching books found.")
        return

    print("\n--- Search Results ---")

    for book in books:
        status = "Available" if book[4] == 1 else "Issued"

        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Category: {book[3]} | "
            f"Status: {status}"
        )


def add_member():
    name = input("Enter member name: ").strip()
    email = input("Enter email: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name:
        print("Member name cannot be empty.")
        return

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO members (name, email, phone)
        VALUES (?, ?, ?)
    """, (name, email, phone))

    connection.commit()
    connection.close()

    print("Member added successfully!")


def view_members():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT member_id, name, email, phone
        FROM members
    """)

    members = cursor.fetchall()
    connection.close()

    if not members:
        print("No members found.")
        return

    print("\n--- Member List ---")

    for member in members:
        print(
            f"ID: {member[0]} | "
            f"Name: {member[1]} | "
            f"Email: {member[2]} | "
            f"Phone: {member[3]}"
        )


def issue_book():
    book_id = input("Enter book ID: ").strip()
    member_id = input("Enter member ID: ").strip()

    if not book_id.isdigit() or not member_id.isdigit():
        print("Book ID and Member ID must be numbers.")
        return

    book_id = int(book_id)
    member_id = int(member_id)

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT available FROM books WHERE book_id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        print("Book not found.")
        connection.close()
        return

    if book[0] == 0:
        print("Book is already issued.")
        connection.close()
        return

    cursor.execute(
        "SELECT member_id FROM members WHERE member_id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if member is None:
        print("Member not found.")
        connection.close()
        return

    issue_date = date.today().isoformat()

    cursor.execute("""
        INSERT INTO issued_books (book_id, member_id, issue_date)
        VALUES (?, ?, ?)
    """, (book_id, member_id, issue_date))

    cursor.execute("""
        UPDATE books
        SET available = 0
        WHERE book_id = ?
    """, (book_id,))

    connection.commit()
    connection.close()

    print("Book issued successfully!")


def return_book():
    book_id = input("Enter book ID to return: ").strip()

    if not book_id.isdigit():
        print("Book ID must be a number.")
        return

    book_id = int(book_id)

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT issue_id
        FROM issued_books
        WHERE book_id = ? AND return_date IS NULL
    """, (book_id,))

    issue = cursor.fetchone()

    if issue is None:
        print("This book is not currently issued.")
        connection.close()
        return

    return_date = date.today().isoformat()

    cursor.execute("""
        UPDATE issued_books
        SET return_date = ?
        WHERE issue_id = ?
    """, (return_date, issue[0]))

    cursor.execute("""
        UPDATE books
        SET available = 1
        WHERE book_id = ?
    """, (book_id,))

    connection.commit()
    connection.close()

    print("Book returned successfully!")


def delete_book():
    book_id = input("Enter book ID to delete: ").strip()

    if not book_id.isdigit():
        print("Book ID must be a number.")
        return

    book_id = int(book_id)

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT book_id FROM books WHERE book_id = ?",
        (book_id,)
    )

    book = cursor.fetchone()

    if book is None:
        print("Book not found.")
        connection.close()
        return

    cursor.execute(
        "DELETE FROM books WHERE book_id = ?",
        (book_id,)
    )

    connection.commit()
    connection.close()

    print("Book deleted successfully!")