from database import get_connection
conn = get_connection()
cursor = conn.cursor()
from rich.console import Console
from rich.table import Table

console = Console()

def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()

def add_passenger():

    heading("ADD PASSENGER")

    try:

        passenger_name = input("Enter Passenger Name : ").strip()
        age = int(input("Enter Age : "))
        gender = input("Enter Gender (Male/Female/Other) : ").strip().title()
        phone = input("Enter Contact Number : ").strip()

        username = input("Enter Username : ").strip()
        password = input("Enter Password : ").strip()

        role = "user"

        # ---------------- Validation ----------------

        if passenger_name == "":
            print("Passenger Name Cannot Be Empty!")
            return

        if age <= 0:
            print("Invalid Age!")
            return

        if gender not in ["Male", "Female", "Other"]:
            print("Invalid Gender!")
            return

        if len(phone) != 10 or not phone.isdigit():
            print("Contact Number Must Be 10 Digits!")
            return

        if username == "":
            print("Username Cannot Be Empty!")
            return

        if len(password) < 6:
            print("Password must contain at least 6 characters.")
            return

        # Check duplicate phone
        cursor.execute(
            "SELECT 1 FROM passengers WHERE phone=?",
            (phone,)
        )

        if cursor.fetchone():
            print("Contact Number Already Exists!")
            return

        # Check duplicate username
        cursor.execute(
            "SELECT 1 FROM users WHERE LOWER(username)=LOWER(?)",
            (username,)
        )

        if cursor.fetchone():
            print("Username Already Exists!")
            return

        # Insert into passengers
        cursor.execute("""
            INSERT INTO passengers
            (passenger_name, age, gender, phone)
            VALUES (?, ?, ?, ?)
        """, (
            passenger_name,
            age,
            gender,
            phone
        ))

        passenger_id = cursor.lastrowid

        # Insert into users
        cursor.execute("""
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, (
            username,
            password,
            role
        ))

        conn.commit()

        heading("PASSENGER ADDED SUCCESSFULLY")

        print("Passenger ID :", passenger_id)
        print("Username     :", username)
        print("Role         :", role)

    except ValueError:
        print("Age Must Be Numeric!")

    except Exception as e:
        conn.rollback()
        print("Error :", e)

# ==========================================
# 3.2.1 VIEW ALL PASSENGERS
# ==========================================

def view_all_passengers():
    heading("ALL PASSENGERS")
    cursor.execute("SELECT * FROM passengers")
    passengers = cursor.fetchall()

    if not passengers:
        print("No Passenger Records Found!")
        return

    table = Table(title="Passenger Details")

    table.add_column("Passenger ID", justify="center", style="cyan")
    table.add_column("Passenger Name", style="green")
    table.add_column("Age", justify="center")
    table.add_column("Gender", justify="center")
    table.add_column("Phone", justify="center")

    for passenger in passengers:

        table.add_row(
            str(passenger[0]),
            passenger[1],
            str(passenger[2]),
            passenger[3],
            passenger[4]
        )

    console.print(table)   
# ==========================================
# 3.2.2 VIEW PASSENGER BY ID
# ==========================================

def view_passenger_by_id():

    heading("VIEW PASSENGER BY ID")
    try:

        passenger_id = int(input("Enter Passenger ID : "))

        cursor.execute(
            "SELECT * FROM passengers WHERE passenger_id=?",
            (passenger_id,)
        )

        passenger = cursor.fetchone()

        if passenger:

            table = Table(title="Passenger Details")

            table.add_column("Passenger ID", justify="center", style="cyan")
            table.add_column("Passenger Name", style="green")
            table.add_column("Age", justify="center")
            table.add_column("Gender", justify="center")
            table.add_column("Phone", justify="center")

            table.add_row(
                str(passenger[0]),
                passenger[1],
                str(passenger[2]),
                passenger[3],
                passenger[4]
            )

            console.print(table)

        else:
            print("Passenger ID Not Found!")

    except ValueError:
        print("Passenger ID Must Be Numeric!")

    except Exception as e:
        print("Error :", e)
# ==========================================
# 3.2.3 VIEW PASSENGER BY NAME
# ==========================================

def view_passenger_by_name():

    heading("VIEW PASSENGER BY NAME")

    try:

        passenger_name = input("Enter Passenger Name : ").strip().title()

        cursor.execute(
            "SELECT * FROM passengers WHERE passenger_name=?",
            (passenger_name,)
        )

        passengers = cursor.fetchall()

        if passengers:

            table = Table(title="Passenger Details")

            table.add_column("Passenger ID", justify="center", style="cyan")
            table.add_column("Passenger Name", style="green")
            table.add_column("Age", justify="center")
            table.add_column("Gender", justify="center")
            table.add_column("Phone", justify="center")

            for passenger in passengers:

                table.add_row(
                    str(passenger[0]),
                    passenger[1],
                    str(passenger[2]),
                    passenger[3],
                    passenger[4]
                )

            console.print(table)

        else:
            print("Passenger Name Not Found!")

    except Exception as e:
        print("Error :", e)
# ==========================================
# 3.3.1 UPDATE PASSENGER BY ID
# ==========================================

def update_passenger():

    heading("UPDATE PASSENGER")

    try:

        passenger_id = int(input("Enter Passenger ID : "))

        cursor.execute(
            "SELECT * FROM passengers WHERE passenger_id=?",
            (passenger_id,)
        )

        passenger = cursor.fetchone()

        if passenger is None:
            print("Passenger ID Not Found!")
            return

        passenger_name = input("Enter New Passenger Name : ").strip().title()
        age = int(input("Enter New Age : "))
        gender = input("Enter New Gender (Male/Female/Other) : ").strip().title()
        phone = input("Enter New Contact Number : ").strip()

        # Validation

        if passenger_name == "":
            print("Passenger Name Cannot Be Empty!")
            return

        if age <= 0:
            print("Invalid Age!")
            return

        if gender not in ["Male", "Female", "Other"]:
            print("Invalid Gender!")
            return

        if len(phone) != 10 or not phone.isdigit():
            print("Contact Number Must Be 10 Digits!")
            return

        # Check duplicate phone number

        cursor.execute(
            """
            SELECT * FROM passengers
            WHERE phone=? AND passenger_id!=?
            """,
            (phone, passenger_id)
        )

        if cursor.fetchone():
            print("Contact Number Already Exists!")
            return

        # Update Passenger

        cursor.execute(
            """
            UPDATE passengers
            SET passenger_name=?,
                age=?,
                gender=?,
                phone=?
            WHERE passenger_id=?
            """,
            (passenger_name, age, gender, phone, passenger_id)
        )

        conn.commit()

        print("Passenger Updated Successfully!")

    except ValueError:
        print("Passenger ID and Age Must Be Numeric!")

    except Exception as e:
        print("Error :", e)
# ==========================================
# 3.3.2 UPDATE CONTACT NUMBER
# ==========================================

def update_contact_number():

    heading("UPDATE CONTACT NUMBER")

    try:

        passenger_id = int(input("Enter Passenger ID : "))
        phone = input("Enter New Contact Number : ").strip()

        if len(phone) != 10 or not phone.isdigit():
            print("Contact Number Must Be 10 Digits!")
            return

        cursor.execute(
            "UPDATE passengers SET phone=? WHERE passenger_id=?",
            (phone, passenger_id)
        )

        conn.commit()

        if cursor.rowcount:
            print("Contact Number Updated Successfully!")
        else:
            print("Passenger ID Not Found!")

    except ValueError:
        print("Passenger ID Must Be Numeric!")

    except Exception as e:
        print("Error :", e)                                 
# ==========================================
# 3.4.1 DELETE PASSENGER BY ID
# ==========================================

def delete_passenger_by_id():

    heading("DELETE PASSENGER")

    try:

        passenger_id = int(input("Enter Passenger ID : "))

        cursor.execute(
            "DELETE FROM passengers WHERE passenger_id=?",
            (passenger_id,)
        )

        conn.commit()

        if cursor.rowcount:
            print("Passenger Deleted Successfully!")
        else:
            print("Passenger ID Not Found!")

    except ValueError:
        print("Passenger ID Must Be Numeric!")

    except Exception as e:
        print("Error :", e)

# ==========================================
# 3.4.2 DELETE PASSENGER BY NAME
# ==========================================

def delete_passenger_by_name():

    print("\n========== DELETE PASSENGER BY NAME ==========\n")

    try:

        passenger_name = input("Enter Passenger Name : ").strip().title()

        cursor.execute(
            "DELETE FROM passengers WHERE passenger_name=?",
            (passenger_name,)
        )

        conn.commit()

        if cursor.rowcount:
            print("Passenger Deleted Successfully!")
        else:
            print("Passenger Name Not Found!")

    except Exception as e:
        print("Error :", e)

# ==========================================
# PASSENGER MANAGEMENT MENU
# ==========================================

def passenger_management():

    while True:

        heading("PASSENGER MANAGEMENT")
        print("1. Add Passenger")
        print("2. View Passengers")
        print("3. Update Passenger")
        print("4. Delete Passenger")
        print("5. Back")

        choice = input("\nEnter Your Choice : ")

        if choice == "1":
            add_passenger()

        elif choice == "2":

            while True:

                heading("VIEW PASSENGERS")
                print("1. View All Passengers")
                print("2. View by Passenger ID")
                print("3. View by Name")
                print("4. Back")

                view_choice = input("\nEnter Your Choice : ")

                if view_choice == "1":
                    view_all_passengers()

                elif view_choice == "2":
                    view_passenger_by_id()

                elif view_choice == "3":
                    view_passenger_by_name()

                elif view_choice == "4":
                    break

                else:
                    print("Invalid Choice!")

        elif choice == "3":

            while True:

                heading("UPDATE PASSENGER")
                print("1. Update by Passenger ID")
                print("2. Update Contact Number")
                print("3. Back")

                update_choice = input("\nEnter Your Choice : ")

                if update_choice == "1":
                    update_passenger()

                elif update_choice == "2":
                    update_contact_number()

                elif update_choice == "3":
                    break

                else:
                    print("Invalid Choice!")

        elif choice == "4":

            while True:

                heading("DELETE PASSENGER")
                print("1. Delete by Passenger ID")
                print("2. Delete by Name")
                print("3. Back")

                delete_choice = input("\nEnter Your Choice : ")

                if delete_choice == "1":
                    delete_passenger_by_id()

                elif delete_choice == "2":
                    delete_passenger_by_name()

                elif delete_choice == "3":
                    break

                else:
                    print("Invalid Choice!")

        elif choice == "5":
            break

        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    passenger_management()
        