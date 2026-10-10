from database import create_tables
from library import (
    add_book,
    view_books,
    search_book,
    add_member,
    view_members,
    issue_book,
    return_book,
    delete_book
)


def main():
    create_tables()

    while True:
        print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Add Member")
        print("5. View Members")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. Delete Book")
        print("9. Exit")
        print("==============================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            search_book()

        elif choice == "4":
            add_member()

        elif choice == "5":
            view_members()

        elif choice == "6":
            issue_book()

        elif choice == "7":
            return_book()

        elif choice == "8":
            delete_book()

        elif choice == "9":
            print("Thank you for using Library Management System!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()