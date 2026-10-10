import sqlite3
import random


DB_NAME = "library.db"


book_titles = [
    "Python Basics",
    "Advanced Python",
    "Data Structures",
    "Algorithms",
    "Database Management",
    "SQL Fundamentals",
    "Web Development",
    "Java Programming",
    "C Programming",
    "C++ Programming",
    "Machine Learning",
    "Artificial Intelligence",
    "Computer Networks",
    "Operating Systems",
    "Software Engineering",
    "Cloud Computing",
    "Cyber Security",
    "Data Science",
    "Statistics",
    "Computer Architecture"
]

authors = [
    "John Smith",
    "Robert Brown",
    "David Wilson",
    "James Miller",
    "Michael Davis",
    "William Taylor",
    "Richard Anderson",
    "Joseph Thomas",
    "Daniel Jackson",
    "Thomas White"
]

categories = [
    "Programming",
    "Database",
    "Computer Science",
    "Networking",
    "Artificial Intelligence",
    "Data Science",
    "Security",
    "Web Development",
    "Cloud",
    "Software Engineering"
]

first_names = [
    "Arun",
    "Kavin",
    "Rahul",
    "Vijay",
    "Ajay",
    "Priya",
    "Divya",
    "Dharshini",
    "Anitha",
    "Keerthana",
    "Harini",
    "Nithya",
    "Sanjay",
    "Surya",
    "Akash"
]

last_names = [
    "Kumar",
    "Raj",
    "Sharma",
    "Singh",
    "Patel",
    "Reddy",
    "Das",
    "Iyer",
    "Nair",
    "Thomas"
]


def generate_books(connection, count=1000):
    cursor = connection.cursor()

    for i in range(count):
        title = f"{random.choice(book_titles)} {i + 1}"
        author = random.choice(authors)
        category = random.choice(categories)

        cursor.execute("""
            INSERT INTO books (title, author, category, available)
            VALUES (?, ?, ?, 1)
        """, (title, author, category))

    print(f"{count} books added successfully!")


def generate_members(connection, count=1000):
    cursor = connection.cursor()

    for i in range(count):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"member{i + 1}@gmail.com"
        phone = f"{random.randint(6000000000, 9999999999)}"

        cursor.execute("""
            INSERT INTO members (name, email, phone)
            VALUES (?, ?, ?)
        """, (name, email, phone))

    print(f"{count} members added successfully!")


def main():
    connection = sqlite3.connect(DB_NAME)

    generate_books(connection, 1000)
    generate_members(connection, 1000)

    connection.commit()
    connection.close()

    print("\nSample data generation completed!")
    print("1000 books and 1000 members are now available.")


if __name__ == "__main__":
    main()