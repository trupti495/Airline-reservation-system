from database import get_connection
from rich.console import Console

console = Console()

def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()

conn = get_connection()
cursor = conn.cursor()

# =====================================================
# ADD AIRLINE
# =====================================================
def add_airline():
    heading("ADD AIRLINE")

    airline_name = input("Enter Airline Name : ")

    cursor.execute(
        """
        INSERT INTO airlines(airline_name)
        VALUES(?)
        """,
        (airline_name,)
    )

    conn.commit()
    print("Airline Added Successfully!")

# =====================================================
# VIEW AIRLINES
# =====================================================
def view_airlines():

    while True:

        heading("VIEW AIRLINES")
        print("1. View All Airlines")
        print("2. Search by Airline ID")
        print("3. Search by Airline Name")
        print("4. Back")

        choice = input("Enter Choice : ")

        if choice == "1":

            cursor.execute("SELECT * FROM airlines")

            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Record Found!")

        elif choice == "2":

            airline_id = int(input("Enter Airline ID : "))

            cursor.execute(
                "SELECT * FROM airlines WHERE airline_id=?",
                (airline_id,)
            )

            row = cursor.fetchone()

            if row:
                print(row)
            else:
                print("No Record Found!")

        elif choice == "3":

            name = input("Enter Airline Name : ")

            cursor.execute(
                "SELECT * FROM airlines WHERE airline_name LIKE ?",
                ('%' + name + '%',)
            )

            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Record Found!")

        elif choice == "4":
            break

        else:
            print("Invalid Choice!")

# =====================================================
# UPDATE AIRLINE
# =====================================================
def update_airline():

    heading("UPDATE AIRLINE")

    airline_id = int(input("Enter Airline ID : "))
    new_name = input("Enter New Airline Name : ")

    cursor.execute(
        """
        UPDATE airlines
        SET airline_name=?
        WHERE airline_id=?
        """,
        (new_name, airline_id)
    )

    conn.commit()

    if cursor.rowcount:
        print("Airline Updated Successfully!")
    else:
        print("Airline ID Not Found!")

# =====================================================
# DELETE AIRLINE
# =====================================================
def delete_airline():

    heading("DELETE AIRLINE")

    try:
        airline_id = int(input("Enter Airline ID : "))

        # Check if airline exists
        cursor.execute(
            "SELECT * FROM airlines WHERE airline_id=?",
            (airline_id,)
        )
        airline = cursor.fetchone()

        if not airline:
            print("Airline ID Not Found!")
            return

        # Check if airline is used in flights table
        cursor.execute(
            "SELECT * FROM flights WHERE airline_id=?",
            (airline_id,)
        )

        if cursor.fetchone():
            print("Cannot delete! This airline is assigned to one or more flights.")
            return

        # Delete airline
        cursor.execute(
            "DELETE FROM airlines WHERE airline_id=?",
            (airline_id,)
        )

        conn.commit()
        print("Airline Deleted Successfully!")

    except ValueError:
        print("Invalid Airline ID! Please enter a number.")

    except Exception as e:
        print("Error:", e)
# =====================================================
# ADD AIRPORT
# =====================================================
def add_airport():

    heading("Add airport")
    airport_name = input("Enter Airport Name : ")
    city = input("Enter City : ")

    cursor.execute(
        """
        INSERT INTO airports
        (airport_name, city)
        VALUES(?,?)
        """,
        (airport_name, city)
    )

    conn.commit()
    print("Airport Added Successfully!")

# =====================================================
# VIEW AIRPORTS
# =====================================================
def view_airports():

    while True:

        heading("VIEW AIRPORTS ")
        print("1. View All Airports")
        print("2. Search by Airport ID")
        print("3. Search by Airport Name")
        print("4. Back")

        choice = input("Enter Choice : ")

        if choice == "1":

            cursor.execute("SELECT * FROM airports")

            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Record Found!")

        elif choice == "2":

            airport_id = int(input("Enter Airport ID : "))

            cursor.execute(
                "SELECT * FROM airports WHERE airport_id=?",
                (airport_id,)
            )

            row = cursor.fetchone()

            if row:
                print(row)
            else:
                print("No Record Found!")

        elif choice == "3":

            name = input("Enter Airport Name : ")

            cursor.execute(
                "SELECT * FROM airports WHERE airport_name LIKE ?",
                ('%' + name + '%',)
            )

            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print("No Record Found!")

        elif choice == "4":
            break

        else:
            print("Invalid Choice!")

# =====================================================
# UPDATE AIRPORT
# =====================================================
def update_airport():

    heading("UPDATE AIRPORT")

    airport_id = int(input("Enter Airport ID : "))
    city = input("Enter New City : ")

    cursor.execute(
        """
        UPDATE airports
        SET city=?
        WHERE airport_id=?
        """,
        (city, airport_id)
    )

    conn.commit()

    if cursor.rowcount:
        print("Airport Updated Successfully!")
    else:
        print("Airport ID Not Found!")

# =====================================================
# DELETE AIRPORT
# =====================================================
import sqlite3

def delete_airport():

    heading("DELETE AIRPORT")

    try:
        airport_id = int(input("Enter Airport ID : "))

        # Check if airport exists
        cursor.execute(
            "SELECT * FROM airports WHERE airport_id=?",
            (airport_id,)
        )

        if cursor.fetchone() is None:
            print("Airport ID Not Found!")
            return

        # Check whether airport is used in flights
        cursor.execute("""
            SELECT * FROM flights
            WHERE source_airport_id=? OR destination_airport_id=?
        """, (airport_id, airport_id))

        if cursor.fetchone():
            print("Cannot delete! This airport is assigned to one or more flights.")
            return

        # Delete airport
        cursor.execute(
            "DELETE FROM airports WHERE airport_id=?",
            (airport_id,)
        )

        conn.commit()
        print("Airport Deleted Successfully!")

    except ValueError:
        print("Invalid Airport ID! Please enter a number.")

    except sqlite3.IntegrityError:
        print("Cannot delete! Airport is linked with existing records.")

    except Exception as e:
        print("Error:", e)
