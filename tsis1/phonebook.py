import csv
import json
from connect import get_connection


# ---------------- SETUP ----------------

def execute_sql_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(sql)
        conn.commit()
        print(filename, "executed successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def setup_database():
    execute_sql_file("schema.sql")
    execute_sql_file("procedures.sql")


# ---------------- HELPERS ----------------

def print_rows(rows):
    if not rows:
        print("No data.")
        return

    for row in rows:
        print(row)


def get_group_id(cur, group_name):
    if not group_name:
        group_name = "Other"

    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    return cur.fetchone()[0]


# ---------------- SHOW CONTACTS ----------------

def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                c.id,
                c.name,
                c.surname,
                c.email,
                c.birthday,
                g.name AS group_name,
                p.phone,
                p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            ORDER BY c.id;
        """)

        rows = cur.fetchall()
        print_rows(rows)

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- ADD CONTACT ----------------

def add_contact():
    name = input("Name: ").strip()
    surname = input("Surname: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday YYYY-MM-DD or empty: ").strip()
    group_name = input("Group Family/Work/Friend/Other: ").strip()

    phone = input("Phone: ").strip()
    phone_type = input("Phone type home/work/mobile: ").strip()

    if surname == "":
        surname = None
    if email == "":
        email = None
    if birthday == "":
        birthday = None
    if phone_type == "":
        phone_type = "mobile"

    conn = get_connection()
    cur = conn.cursor()

    try:
        group_id = get_group_id(cur, group_name)

        cur.execute("""
            INSERT INTO contacts(name, surname, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name, surname)
            DO UPDATE SET
                email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id;
        """, (name, surname, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
            ON CONFLICT (contact_id, phone) DO NOTHING;
        """, (contact_id, phone, phone_type))

        conn.commit()
        print("Contact saved.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- ADD PHONE ----------------

def add_phone_to_contact():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type home/work/mobile: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))
        conn.commit()
        print("Phone added.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- MOVE TO GROUP ----------------

def move_contact_to_group():
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("CALL move_to_group(%s, %s);", (name, group_name))
        conn.commit()
        print("Contact moved to group.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- SEARCH ----------------

def search_contacts_console():
    query = input("Search text: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM search_contacts(%s);", (query,))
        rows = cur.fetchall()
        print_rows(rows)

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


def search_by_email():
    email_part = input("Email contains: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, name, surname, email
            FROM contacts
            WHERE email ILIKE %s
            ORDER BY id;
        """, ("%" + email_part + "%",))

        rows = cur.fetchall()
        print_rows(rows)

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- FILTER BY GROUP ----------------

def filter_by_group():
    group_name = input("Group name: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT c.id, c.name, c.surname, c.email, c.birthday, g.name
            FROM contacts c
            JOIN groups g ON c.group_id = g.id
            WHERE g.name ILIKE %s
            ORDER BY c.id;
        """, (group_name,))

        rows = cur.fetchall()
        print_rows(rows)

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- SORT ----------------

def sort_contacts():
    print("Sort by:")
    print("1. name")
    print("2. birthday")
    print("3. date added")

    choice = input("Choose: ").strip()

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday"
    elif choice == "3":
        order_by = "c.created_at"
    else:
        print("Wrong choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(f"""
            SELECT c.id, c.name, c.surname, c.email, c.birthday, c.created_at
            FROM contacts c
            ORDER BY {order_by};
        """)

        rows = cur.fetchall()
        print_rows(rows)

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- PAGINATION NEXT / PREV ----------------

def paginated_navigation():
    limit_value = int(input("Page size: "))
    offset = 0

    conn = get_connection()
    cur = conn.cursor()

    try:
        while True:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s);",
                (limit_value, offset)
            )

            rows = cur.fetchall()

            print("\n--- Page ---")
            print_rows(rows)

            command = input("\nnext / prev / quit: ").strip().lower()

            if command == "next":
                offset += limit_value
            elif command == "prev":
                offset -= limit_value

                if offset < 0:
                    offset = 0
            elif command == "quit":
                break
            else:
                print("Wrong command.")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- EXPORT JSON ----------------

def export_to_json():
    filename = input("JSON filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 
                c.id,
                c.name,
                c.surname,
                c.email,
                c.birthday,
                g.name AS group_name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id;
        """)

        contacts = cur.fetchall()
        result = []

        for contact in contacts:
            contact_id = contact[0]

            cur.execute("""
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s;
            """, (contact_id,))

            phones = cur.fetchall()

            result.append({
                "name": contact[1],
                "surname": contact[2],
                "email": contact[3],
                "birthday": str(contact[4]) if contact[4] else None,
                "group": contact[5],
                "phones": [
                    {"phone": p[0], "type": p[1]}
                    for p in phones
                ]
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=4)

        print("Export finished.")

    except Exception as e:
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- IMPORT JSON ----------------

def import_from_json():
    filename = input("JSON filename: ").strip()

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    try:
        for item in data:
            name = item.get("name")
            surname = item.get("surname")
            email = item.get("email")
            birthday = item.get("birthday")
            group_name = item.get("group")
            phones = item.get("phones", [])

            cur.execute("""
                SELECT id
                FROM contacts
                WHERE name = %s
                  AND COALESCE(surname, '') = COALESCE(%s, '');
            """, (name, surname))

            existing = cur.fetchone()

            if existing:
                answer = input(f"{name} already exists. skip/overwrite: ").strip().lower()

                if answer == "skip":
                    continue

            group_id = get_group_id(cur, group_name)

            cur.execute("""
                INSERT INTO contacts(name, surname, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (name, surname)
                DO UPDATE SET
                    email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id;
            """, (name, surname, email, birthday, group_id))

            contact_id = cur.fetchone()[0]

            for p in phones:
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone) DO NOTHING;
                """, (contact_id, p["phone"], p["type"]))

        conn.commit()
        print("Import finished.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- IMPORT CSV ----------------

def import_from_csv():
    filename = input("CSV filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["name"]
                surname = row["surname"] if row["surname"] else None
                email = row["email"] if row["email"] else None
                birthday = row["birthday"] if row["birthday"] else None
                group_name = row["group"] if row["group"] else "Other"
                phone = row["phone"]
                phone_type = row["phone_type"] if row["phone_type"] else "mobile"

                group_id = get_group_id(cur, group_name)

                cur.execute("""
                    INSERT INTO contacts(name, surname, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (name, surname)
                    DO UPDATE SET
                        email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                    RETURNING id;
                """, (name, surname, email, birthday, group_id))

                contact_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone) DO NOTHING;
                """, (contact_id, phone, phone_type))

        conn.commit()
        print("CSV import finished.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()


# ---------------- MENU ----------------

def menu():
    while True:
        print("\n--- PhoneBook TSIS 1 ---")
        print("1. Setup database")
        print("2. Show all contacts")
        print("3. Add or update contact")
        print("4. Add phone to contact")
        print("5. Move contact to group")
        print("6. Search contacts")
        print("7. Search by email")
        print("8. Filter by group")
        print("9. Sort contacts")
        print("10. Paginated navigation")
        print("11. Export to JSON")
        print("12. Import from JSON")
        print("13. Import from CSV")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            setup_database()
        elif choice == "2":
            show_all_contacts()
        elif choice == "3":
            add_contact()
        elif choice == "4":
            add_phone_to_contact()
        elif choice == "5":
            move_contact_to_group()
        elif choice == "6":
            search_contacts_console()
        elif choice == "7":
            search_by_email()
        elif choice == "8":
            filter_by_group()
        elif choice == "9":
            sort_contacts()
        elif choice == "10":
            paginated_navigation()
        elif choice == "11":
            export_to_json()
        elif choice == "12":
            import_from_json()
        elif choice == "13":
            import_from_csv()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()