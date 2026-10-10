import sqlite3

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

cursor.execute("SELECT member_id FROM members")

members = cursor.fetchall()

for member in members:
    member_id = member[0]

    email = f"member{member_id}@gmail.com"
    phone = f"{6000000000 + member_id:010d}"

    cursor.execute("""
        UPDATE members
        SET email = ?, phone = ?
        WHERE member_id = ?
    """, (email, phone, member_id))

connection.commit()
connection.close()

print("All member email and phone numbers updated successfully!")