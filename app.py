from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re
from datetime import date

app = Flask(__name__)

DB_NAME = "library.db"


# ---------------- DATABASE CONNECTION ----------------

def get_db_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# ---------------- DASHBOARD ----------------

@app.route("/")
def dashboard():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE available = 1")
    available_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books WHERE available = 0")
    issued_books_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM members")
    total_members = cursor.fetchone()[0]

    cursor.execute("""
        SELECT book_id, title, author, category, available
        FROM books
        ORDER BY book_id DESC
        LIMIT 10
    """)
    recent_books = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books_count,
        total_members=total_members,
        recent_books=recent_books
    )


# ---------------- ADD BOOK ----------------

@app.route("/add-book", methods=["GET", "POST"])
def add_book_page():

    error = None

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        category = request.form.get("category", "").strip()

        if not title:
            error = "Book title is required!"

        elif not author:
            error = "Author name is required!"

        else:
            connection = get_db_connection()

            try:
                connection.execute("""
                    INSERT INTO books (title, author, category, available)
                    VALUES (?, ?, ?, 1)
                """, (title, author, category))

                connection.commit()
                connection.close()

                return redirect(url_for("books"))

            except sqlite3.Error:
                connection.rollback()
                connection.close()
                error = "Unable to add book. Please try again."

        return render_template(
            "add_book.html",
            error=error,
            title=title,
            author=author,
            category=category
        )

    return render_template(
        "add_book.html",
        error=None,
        title="",
        author="",
        category=""
    )


# ---------------- ADD MEMBER ----------------

@app.route("/add-member", methods=["GET", "POST"])
def add_member_page():

    error = None

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        if not name:
            error = "Member name is required!"

        elif not email:
            error = "Email address is required!"

        elif not re.fullmatch(r"[^@\s]+@gmail\.com", email, re.IGNORECASE):
            error = "Please enter a valid Gmail address!"

        elif not phone:
            error = "Phone number is required!"

        elif not phone.isdigit() or len(phone) != 10:
            error = "Phone number must contain exactly 10 digits!"

        else:
            connection = get_db_connection()

            try:
                connection.execute("""
                    INSERT INTO members (name, email, phone)
                    VALUES (?, ?, ?)
                """, (name, email, phone))

                connection.commit()
                connection.close()

                return redirect(url_for("members"))

            except sqlite3.Error:
                connection.rollback()
                connection.close()
                error = "Unable to add member. Please try again."

        return render_template(
            "add_member.html",
            error=error,
            name=name,
            email=email,
            phone=phone
        )

    return render_template(
        "add_member.html",
        error=None,
        name="",
        email="",
        phone=""
    )


# ---------------- SEARCH BOOKS ----------------

@app.route("/search-books")
def search_books():

    search_query = request.args.get("q", "").strip()

    connection = get_db_connection()

    search_results = connection.execute("""
        SELECT book_id, title, author, category, available
        FROM books
        WHERE title LIKE ?
           OR author LIKE ?
           OR category LIKE ?
           OR CAST(book_id AS TEXT) LIKE ?
        ORDER BY title
        LIMIT 100
    """, (
        f"%{search_query}%",
        f"%{search_query}%",
        f"%{search_query}%",
        f"%{search_query}%"
    )).fetchall()

    connection.close()

    return render_template(
        "books.html",
        books=search_results,
        search_query=search_query
    )


# ---------------- BOOKS PAGE ----------------

@app.route("/books")
def books():

    connection = get_db_connection()

    books_list = connection.execute("""
        SELECT book_id, title, author, category, available
        FROM books
        ORDER BY book_id DESC
        LIMIT 100
    """).fetchall()

    connection.close()

    return render_template(
        "books.html",
        books=books_list,
        search_query=""
    )


# ---------------- SEARCH MEMBERS ----------------

@app.route("/search-members")
def search_members():

    search_query = request.args.get("q", "").strip()

    connection = get_db_connection()

    search_results = connection.execute("""
        SELECT member_id, name, email, phone
        FROM members
        WHERE name LIKE ?
           OR email LIKE ?
           OR phone LIKE ?
           OR CAST(member_id AS TEXT) LIKE ?
        ORDER BY member_id DESC
        LIMIT 100
    """, (
        f"%{search_query}%",
        f"%{search_query}%",
        f"%{search_query}%",
        f"%{search_query}%"
    )).fetchall()

    connection.close()

    return render_template(
        "members.html",
        members=search_results,
        search_query=search_query
    )


# ---------------- MEMBERS PAGE ----------------

@app.route("/members")
def members():

    connection = get_db_connection()

    members_list = connection.execute("""
        SELECT member_id, name, email, phone
        FROM members
        ORDER BY member_id DESC
        LIMIT 100
    """).fetchall()

    connection.close()

    return render_template(
        "members.html",
        members=members_list,
        search_query=""
    )


# ---------------- ISSUE BOOK ----------------

@app.route("/issue-book", methods=["GET", "POST"])
def issue_book():

    error = None
    book_id = ""
    member_id = ""

    connection = get_db_connection()

    if request.method == "POST":

        book_id = request.form.get("book_id", "").strip()
        member_id = request.form.get("member_id", "").strip()

        if not book_id.isdigit() or not member_id.isdigit():

            error = "Please enter valid Book ID and Member ID."

        else:

            cursor = connection.cursor()

            cursor.execute("""
                SELECT book_id, title, available
                FROM books
                WHERE book_id = ?
            """, (book_id,))

            book = cursor.fetchone()

            cursor.execute("""
                SELECT member_id, name
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()

            if book is None:
                error = "Book not found!"

            elif member is None:
                error = "Member not found!"

            elif book["available"] != 1:
                error = "This book is already issued!"

            else:

                try:
                    issue_date = date.today().isoformat()

                    cursor.execute("""
                        INSERT INTO issued_books
                        (book_id, member_id, issue_date, return_date)
                        VALUES (?, ?, ?, NULL)
                    """, (book_id, member_id, issue_date))

                    cursor.execute("""
                        UPDATE books
                        SET available = 0
                        WHERE book_id = ? AND available = 1
                    """, (book_id,))

                    if cursor.rowcount != 1:
                        connection.rollback()
                        error = "This book is no longer available!"

                    else:
                        connection.commit()
                        connection.close()
                        return redirect(url_for("issued"))

                except sqlite3.Error:
                    connection.rollback()
                    error = "Unable to issue book. Please try again."

        if error:
            connection.close()

            return render_template(
                "issue_book.html",
                books=get_available_books(),
                members=get_all_members(),
                error=error,
                book_id=book_id,
                member_id=member_id
            )

    connection.close()

    return render_template(
        "issue_book.html",
        books=get_available_books(),
        members=get_all_members(),
        error=error,
        book_id=book_id,
        member_id=member_id
    )


# ---------------- HELPER FUNCTIONS ----------------

def get_available_books():

    connection = get_db_connection()

    books_list = connection.execute("""
        SELECT book_id, title, author
        FROM books
        WHERE available = 1
        ORDER BY title
    """).fetchall()

    connection.close()

    return books_list


def get_all_members():

    connection = get_db_connection()

    members_list = connection.execute("""
        SELECT member_id, name
        FROM members
        ORDER BY name
    """).fetchall()

    connection.close()

    return members_list


# ---------------- RETURN BOOK ----------------

@app.route("/return-book/<int:issue_id>", methods=["POST"])
def return_book(issue_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT book_id, return_date
        FROM issued_books
        WHERE issue_id = ?
    """, (issue_id,))

    record = cursor.fetchone()

    if record is None:
        connection.close()
        return "Issue record not found.", 404

    if record["return_date"] is not None:
        connection.close()
        return redirect(url_for("issued"))

    try:
        return_date = date.today().isoformat()

        cursor.execute("""
            UPDATE issued_books
            SET return_date = ?
            WHERE issue_id = ?
              AND return_date IS NULL
        """, (return_date, issue_id))

        if cursor.rowcount != 1:
            connection.rollback()
            connection.close()
            return "Unable to return this book.", 400

        cursor.execute("""
            UPDATE books
            SET available = 1
            WHERE book_id = ?
        """, (record["book_id"],))

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        connection.close()
        return "Unable to return book. Please try again.", 500

    connection.close()

    return redirect(url_for("issued"))


# ---------------- ISSUED BOOKS PAGE & SEARCH ----------------

@app.route("/issued")
def issued():

    search_query = request.args.get("q", "").strip()

    connection = get_db_connection()

    issued_books_list = connection.execute("""
        SELECT
            issued_books.issue_id,
            issued_books.book_id,
            books.title,
            issued_books.member_id,
            members.name,
            issued_books.issue_date,
            issued_books.return_date
        FROM issued_books

        LEFT JOIN books
            ON issued_books.book_id = books.book_id

        LEFT JOIN members
            ON issued_books.member_id = members.member_id

        WHERE books.title LIKE ?
           OR members.name LIKE ?
           OR CAST(issued_books.issue_id AS TEXT) LIKE ?
           OR CAST(issued_books.book_id AS TEXT) LIKE ?
           OR CAST(issued_books.member_id AS TEXT) LIKE ?

        ORDER BY issued_books.issue_id DESC
    """, (
        f"%{search_query}%",
        f"%{search_query}%",
        f"%{search_query}%",
        f"%{search_query}%",
        f"%{search_query}%"
    )).fetchall()

    connection.close()

    return render_template(
        "issued.html",
        issued_books=issued_books_list,
        search_query=search_query
    )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)