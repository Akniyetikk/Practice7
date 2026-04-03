import csv
from connect import get_connection

def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader) 
            for row in reader:
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone_number) "
                    "VALUES (%s, %s) ON CONFLICT DO NOTHING", (row[0], row[1])
                )
        conn.commit()
        print("Data imported.")
    except FileNotFoundError:
        print("File not found.")
    finally:
        cur.close()
        conn.close()

def insert_from_console():
    name = input("Name: ")
    phone = input("Phone: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact saved.")

def update_contact():
    target_name = input("Enter current name: ")
    new_name = input("Enter new name (leave blank to keep same): ")
    new_phone = input("Enter new phone (leave blank to keep same): ")
    
    conn = get_connection()
    cur = conn.cursor()
    
    if new_name and new_phone:
        cur.execute("UPDATE phonebook SET first_name = %s, phone_number = %s WHERE first_name = %s", (new_name, new_phone, target_name))
    elif new_name:
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, target_name))
    elif new_phone:
        cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (new_phone, target_name))
        
    conn.commit()
    cur.close()
    conn.close()
    print("Updated.")

def query_contacts():
    search = input("Search by name/prefix: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE first_name LIKE %s OR phone_number LIKE %s", (search + '%', search + '%'))
    for row in cur.fetchall():
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
    cur.close()
    conn.close()

def delete_contact():
    target = input("Name or Phone to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s", (target, target))
    conn.commit()
    cur.close()
    conn.close()
    print("Deleted.")

if __name__ == "__main__":
    while True:
        print("\n1.CSV 2.Add 3.Update 4.Search 5.Delete 0.Exit")
        choice = input("Choice: ")
        if choice == '1': insert_from_csv('contacts.csv')
        elif choice == '2': insert_from_console()
        elif choice == '3': update_contact()
        elif choice == '4': query_contacts()
        elif choice == '5': delete_contact()
        elif choice == '0': break
