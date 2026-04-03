from connect import get_connection


def execute_sql_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        sql = f.read()

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        print(f"{filename} executed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error in {filename}: {e}")
    finally:
        cur.close()
        conn.close()


def setup_database():
    execute_sql_file("functions.sql")
    execute_sql_file("procedures.sql")


def search_by_pattern():
    pattern = input("Enter pattern: ")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts_by_pattern(%s);", (pattern,))
        rows = cur.fetchall()

        if rows:
            print("\nFound contacts:")
            for row in rows:
                print(row)
        else:
            print("No matches found.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def upsert_one_contact():
    name = input("Name: ")
    surname = input("Surname (optional): ")
    phone = input("Phone: ")

    if surname.strip() == "":
        surname = None

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL upsert_contact(%s, %s, %s);", (name, surname, phone))
        conn.commit()
        print("Contact inserted/updated successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def upsert_many_contacts():
    print("Enter contacts one by one.")
    print("Format: name,surname,phone")
    print("Type 'stop' to finish.")

    names = []
    surnames = []
    phones = []

    while True:
        line = input("> ").strip()
        if line.lower() == "stop":
            break

        parts = line.split(",")
        if len(parts) != 3:
            print("Wrong format. Use: name,surname,phone")
            continue

        name, surname, phone = [p.strip() for p in parts]
        names.append(name)
        surnames.append(surname if surname else None)
        phones.append(phone)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "CALL upsert_many_contacts(%s, %s, %s);",
            (names, surnames, phones)
        )
        conn.commit()
        print("Bulk insert/update finished.")

        # Пытаемся показать invalid_contacts
        try:
            cur.execute("SELECT * FROM invalid_contacts;")
            invalid_rows = cur.fetchall()

            if invalid_rows:
                print("\nInvalid rows:")
                for row in invalid_rows:
                    print(row)
            else:
                print("No invalid rows.")
        except Exception:
            print("No invalid rows table available.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def show_paginated():
    limit_value = int(input("Limit: "))
    offset_value = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s);",
            (limit_value, offset_value)
        )
        rows = cur.fetchall()

        if rows:
            print("\nContacts page:")
            for row in rows:
                print(row)
        else:
            print("No data.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def delete_contact():
    value = input("Enter username or phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact(%s);", (value,))
        conn.commit()
        print("Delete operation completed.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, surname, phone FROM contacts ORDER BY id;")
        rows = cur.fetchall()

        if rows:
            print("\nAll contacts:")
            for row in rows:
                print(row)
        else:
            print("PhoneBook is empty.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def menu():
    while True:
        print("\n--- PhoneBook Practice 8 ---")
        print("1. Setup database objects")
        print("2. Show all contacts")
        print("3. Search contacts by pattern")
        print("4. Upsert one contact")
        print("5. Upsert many contacts")
        print("6. Show contacts with pagination")
        print("7. Delete contact by username or phone")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            setup_database()
        elif choice == "2":
            show_all_contacts()
        elif choice == "3":
            search_by_pattern()
        elif choice == "4":
            upsert_one_contact()
        elif choice == "5":
            upsert_many_contacts()
        elif choice == "6":
            show_paginated()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()