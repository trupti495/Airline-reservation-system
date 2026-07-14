from database import get_connection
from rich.console import Console
from rich.table import Table
import sqlite3

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
            cursor.execute("SELECT airline_id, airline_name FROM airlines")
            rows = cursor.fetchall()

            if rows:
                table = Table(title="All Airlines", show_lines=True)
                table.add_column("Airline ID", style="cyan", justify="center")
                table.add_column("Airline Name", style="green")
                for row in rows:
                    table.add_row(str(row[0]), row[1])
                console.print(table)
            else:
                print("No Record Found!")

        elif choice == "2":
            airline_id = int(input("Enter Airline ID : "))
            cursor.execute(
                "SELECT airline_id, airline_name FROM airlines WHERE airline_id=?",
                (airline_id,)
            )
            row = cursor.fetchone()

            if row:
                table = Table(title="Airline Details", show_lines=True)
                table.add_column("Airline ID", style="cyan", justify="center")
                table.add_column("Airline Name", style="green")
                table.add_row(str(row[0]), row[1])
                console.print(table)
            else:
                print("No Record Found!")

        elif choice == "3":
            name = input("Enter Airline Name : ")
            cursor.execute(
                "SELECT airline_id, airline_name FROM airlines WHERE airline_name LIKE?",
                ('%' + name + '%',)
            )
            rows = cursor.fetchall()

            if rows:
                table = Table(title=f"Search Results for '{name}'", show_lines=True)
                table.add_column("Airline ID", style="cyan", justify="center")
                table.add_column("Airline Name", style="green")
                for row in rows:
                    table.add_row(str(row[0]), row[1])
                console.print(table)
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
        cursor.execute("SELECT airline_name FROM airlines WHERE airline_id=?", (airline_id,))
        airline = cursor.fetchone()
        if not airline:
            print("Airline ID Not Found!")
            return

        # Check if airline is used in flights table
        cursor.execute("SELECT * FROM flights WHERE airline_id=?", (airline_id,))
        if cursor.fetchone():
            print("Cannot delete! This airline is assigned to one or more flights.")
            return

        # Confirmation
        confirm = input(f"Are you sure you want to delete '{airline[0]}'? [y/N]: ").lower()
        if confirm!= 'y':
            print("Deletion cancelled.")
            return

        # Delete airline
        cursor.execute("DELETE FROM airlines WHERE airline_id=?", (airline_id,))
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
    heading("ADD AIRPORT")
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
        heading("VIEW AIRPORTS")
        print("1. View All Airports")
        print("2. Search by Airport ID")
        print("3. Search by Airport Name")
        print("4. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            cursor.execute("SELECT airport_id, airport_name, city FROM airports")
            rows = cursor.fetchall()

            if rows:
                table = Table(title="All Airports", show_lines=True)
                table.add_column("Airport ID", style="cyan", justify="center")
                table.add_column("Airport Name", style="green")
                table.add_column("City", style="yellow")
                for row in rows:
                    table.add_row(str(row[0]), row[1], row[2])
                console.print(table)
            else:
                print("No Record Found!")

        elif choice == "2":
            airport_id = int(input("Enter Airport ID : "))
            cursor.execute(
                "SELECT airport_id, airport_name, city FROM airports WHERE airport_id=?",
                (airport_id,)
            )
            row = cursor.fetchone()

            if row:
                table = Table(title="Airport Details", show_lines=True)
                table.add_column("Airport ID", style="cyan", justify="center")
                table.add_column("Airport Name", style="green")
                table.add_column("City", style="yellow")
                table.add_row(str(row[0]), row[1], row[2])
                console.print(table)
            else:
                print("No Record Found!")

        elif choice == "3":
            name = input("Enter Airport Name : ")
            cursor.execute(
                "SELECT airport_id, airport_name, city FROM airports WHERE airport_name LIKE?",
                ('%' + name + '%',)
            )
            rows = cursor.fetchall()

            if rows:
                table = Table(title=f"Search Results for '{name}'", show_lines=True)
                table.add_column("Airport ID", style="cyan", justify="center")
                table.add_column("Airport Name", style="green")
                table.add_column("City", style="yellow")
                for row in rows:
                    table.add_row(str(row[0]), row[1], row[2])
                console.print(table)
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
def delete_airport():
    heading("DELETE AIRPORT")
    try:
        airport_id = int(input("Enter Airport ID : "))

        # Check if airport exists
        cursor.execute("SELECT airport_name, city FROM airports WHERE airport_id=?", (airport_id,))
        airport = cursor.fetchone()
        if airport is None:
            print("Airport ID Not Found!")
            return

        # Check whether airport is used in flights
        cursor.execute("SELECT * FROM flights WHERE source_airport_id=? OR destination_airport_id=?", (airport_id, airport_id))
        if cursor.fetchone():
            print("Cannot delete! This airport is assigned to one or more flights.")
            return
        else:
        # Confirmation
         confirm = input(f"Are you sure you want to delete '{airport[0]}' in {airport[1]}? [y/N]: ").lower()
         if confirm!= 'y':
            print("Deletion cancelled.")
            return

         else: # Delete airport
          cursor.execute("DELETE FROM airports WHERE airport_id=?", (airport_id,))
          conn.commit()
          print("Airport Deleted Successfully!")

    except ValueError:
        print("Invalid Airport ID! Please enter a number.")
    except sqlite3.IntegrityError:
        print("Cannot delete! Airport is linked with existing records.")
    except Exception as e:
        print("Error:", e)