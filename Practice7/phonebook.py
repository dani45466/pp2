from connect import get_connection
import csv

# 1. Create table
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

# 2. Insert from CSV
def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV импорт выполнен")

# 3. Insert from console
def insert_from_console():
    name = input("Имя: ")
    phone = input("Телефон: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен")

# 4. Search
def search():
    keyword = input("Поиск: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM contacts
        WHERE name ILIKE %s OR phone LIKE %s
    """, (f"%{keyword}%", f"{keyword}%"))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

# 5. Update
def update():
    name = input("Кого изменить: ")
    new_name = input("Новое имя (Enter если нет): ")
    new_phone = input("Новый телефон (Enter если нет): ")

    conn = get_connection()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE contacts SET name = %s WHERE name = %s",
            (new_name, name)
        )

    if new_phone:
        cur.execute(
            "UPDATE contacts SET phone = %s WHERE name = %s",
            (new_phone, name)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Обновлено")

# 6. Delete
def delete():
    value = input("Удалить (имя или телефон): ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM contacts
        WHERE name = %s OR phone = %s
    """, (value, value))

    conn.commit()
    cur.close()
    conn.close()
    print("Удалено")

# Menu
def menu():
    while True:
        print("""
1. Create table
2. Import CSV
3. Add contact
4. Search
5. Update
6. Delete
0. Exit
""")

        choice = input("Выбор: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            search()
        elif choice == "5":
            update()
        elif choice == "6":
            delete()
        elif choice == "0":
            break

if __name__ == "__main__":
    menu()