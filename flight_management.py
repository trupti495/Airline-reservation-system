from database import get_connection
import sqlite3
from rich.table import Table
from rich.console import Console
from colorama import Fore, init,Style
from tabulate import tabulate


console = Console()

def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()
init(autoreset=True)
console = Console()

def add_flight():
    conn = get_connection()
    cursor = conn.cursor()
    console.rule("[bold green]Add Flight[/bold green]")
    
    airline_id = int(input("Enter Airline ID: "))
    source_airport_id = int(input("Enter Source Airport ID: "))
    destination_airport_id = int(input("Enter Destination Airport ID: "))
    # Check Airline ID
    cursor.execute("SELECT * FROM airlines WHERE airline_id = ?", (airline_id,))
    if cursor.fetchone() is None:
        print(Fore.RED + "Airline ID not found!")
        conn.close()
        return

# Check Source Airport
    cursor.execute("SELECT * FROM airports WHERE airport_id = ?", (source_airport_id,))
    if cursor.fetchone() is None:
        print(Fore.RED + "Source Airport not found!")
        conn.close()
        return

# Check Destination Airport
    cursor.execute("SELECT * FROM airports WHERE airport_id = ?", (destination_airport_id,))
    if cursor.fetchone() is None:
        print(Fore.RED + "Destination Airport not found!")
        conn.close()
        return
    departure_date = input("Enter Departure Date (YYYY-MM-DD): ")
    departure_time = input("Enter Departure Time (HH:MM): ")
    fare = float(input("Enter Fare: "))
    available_seats = int(input("Enter Available Seats: "))
    print(airline_id, source_airport_id, destination_airport_id)

    try: 
        cursor.execute("""
INSERT INTO flights
(
    airline_id,
    source_airport_id,
    destination_airport_id,
    departure_date,
    departure_time,
    fare,
    total_seats,
    available_seats
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
(
    airline_id,
    source_airport_id,
    destination_airport_id,
    departure_date,
    departure_time,
    fare,
    available_seats,
    available_seats
))

        conn.commit()
    
        print(Fore.GREEN + "Flight added successfully!")
    except sqlite3.IntegrityError:
        print(Fore.RED + "Foreign Key Constraint Error!")

    finally:
        conn.close()    

def view_all_flights():

    heading("VIEW ALL FLIGHTS")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()

    if not flights:
        print("No flights found.")
        conn.close()
        return

    table = Table(
        title="[bold bright_cyan]✈ ALL FLIGHTS ✈[/bold bright_cyan]",
        show_lines=True,
        header_style="bold bright_white"
    )

    table.add_column("Flight ID", style="bright_yellow", justify="center")
    table.add_column("Airline ID", style="bright_green", justify="center")
    table.add_column("Source", style="cyan", justify="center")
    table.add_column("Destination", style="magenta", justify="center")
    table.add_column("Date", style="bright_blue", justify="center")
    table.add_column("Time", style="bright_red", justify="center")
    table.add_column("Fare (₹)", style="green", justify="right")
    table.add_column("Seats", style="yellow", justify="center")

    for flight in flights:
        table.add_row(
            str(flight[0]),
            str(flight[1]),
            str(flight[2]),
            str(flight[3]),
            str(flight[4]),
            str(flight[5]),
            f"₹ {flight[6]}",
            str(flight[7])
        )

    console.print(table)

    conn.close()

def view_available_flights():

    heading("AVAILABLE FLIGHTS")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM flights
        WHERE available_seats > 0
    """)

    flights = cursor.fetchall()

    if not flights:
        print("No Available Flights.")
        conn.close()
        return

    table = Table(
        title="[bold bright_green]🛫 AVAILABLE FLIGHTS 🛫[/bold bright_green]",
        show_lines=True,
        header_style="bold bright_white"
    )

    table.add_column("Flight ID", style="bright_yellow", justify="center")
    table.add_column("Airline ID", style="bright_green", justify="center")
    table.add_column("Source", style="cyan", justify="center")
    table.add_column("Destination", style="magenta", justify="center")
    table.add_column("Date", style="bright_blue", justify="center")
    table.add_column("Time", style="bright_red", justify="center")
    table.add_column("Fare (₹)", style="green", justify="right")
    table.add_column("Seats", style="bold bright_green", justify="center")

    for flight in flights:
        table.add_row(
            str(flight[0]),
            str(flight[1]),
            str(flight[2]),
            str(flight[3]),
            str(flight[4]),
            str(flight[5]),
            f"₹ {flight[6]}",
            str(flight[7])
        )

    console.print(table)

    conn.close()
def search_by_flight_id():
    conn = get_connection()
    cursor = conn.cursor()

    flight_id = int(input("Enter Flight ID: "))

    cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
    flight = cursor.fetchone()

    if not flight:
        print(Fore.RED + "Flight not found.")
        conn.close()
        return

    table = Table(title="Flight Details")

    table.add_column("Flight ID")
    table.add_column("Airline ID")
    table.add_column("Source")
    table.add_column("Destination")
    table.add_column("Date")
    table.add_column("Time")
    table.add_column("Fare")
    table.add_column("Seats")

    table.add_row(
        str(flight[0]),
        str(flight[1]),
        str(flight[2]),
        str(flight[3]),
        str(flight[4]),
        str(flight[5]),
        str(flight[6]),
        str(flight[7])
    )

    console.print(table)

    conn.close()

def search_by_source_destination():
    conn = get_connection()
    cursor = conn.cursor()


    source_airport_id = int(input("Enter Source Airport ID: "))
    destination_airport_id = int(input("Enter Destination Airport ID: "))

    cursor.execute("""
        SELECT * FROM flights
        WHERE source_airport_id = ? AND destination_airport_id = ?
    """, (source_airport_id, destination_airport_id))

    flights = cursor.fetchall()

    if not flights:
        print(Fore.RED + "No flights found.")
        conn.close()
        return

    table = Table(title="Search Results")

    table.add_column("Flight ID")
    table.add_column("Airline ID")
    table.add_column("Source")
    table.add_column("Destination")
    table.add_column("Date")
    table.add_column("Time")
    table.add_column("Fare")
    table.add_column("Seats")

    for flight in flights:
        table.add_row(
            str(flight[0]),
            str(flight[1]),
            str(flight[2]),
            str(flight[3]),
            str(flight[4]),
            str(flight[5]),
            str(flight[6]),
            str(flight[7])
        )

    console.print(table)

    conn.close()
def update_available_seats():
    conn = get_connection()
    cursor = conn.cursor()

    flight_id = int(input("Enter Flight ID: "))
    seats = int(input("Enter New Available Seats: "))

    cursor.execute("""
        UPDATE flights
        SET available_seats = ?
        WHERE flight_id = ?
    """, (seats, flight_id))

    conn.commit()

    if cursor.rowcount > 0:
        print(Fore.GREEN + "Available seats updated successfully!")
    else:
        print(Fore.RED + "Flight not found.")

    conn.close()


def update_schedule():
    conn = get_connection()
    cursor = conn.cursor()

    flight_id = int(input("Enter Flight ID: "))
    departure_date = input("Enter New Departure Date (YYYY-MM-DD): ")
    departure_time = input("Enter New Departure Time (HH:MM): ")

    cursor.execute("""
        UPDATE flights
        SET departure_date = ?, departure_time = ?
        WHERE flight_id = ?
    """, (departure_date, departure_time, flight_id))

    conn.commit()

    if cursor.rowcount > 0:
        print(Fore.GREEN + "Schedule updated successfully!")
    else:
        print(Fore.RED + "Flight not found.")

    conn.close()         

def update_fare():
    conn = get_connection()
    cursor = conn.cursor()

    flight_id = int(input("Enter Flight ID: "))
    fare = float(input("Enter New Fare: "))

    cursor.execute("""
        UPDATE flights
        SET fare = ?
        WHERE flight_id = ?
    """, (fare, flight_id))

    conn.commit()

    if cursor.rowcount > 0:
        print(Fore.GREEN + "Fare updated successfully!")
    else:
        print(Fore.RED + "Flight not found.")
    conn.close()       

def delete_flight():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        flight_id = int(input("Enter Flight ID to delete: "))

        # Check if flight exists
        cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
        if cursor.fetchone() is None:
            print(Fore.RED + "Flight not found.")
            return

        # Check if bookings exist
        cursor.execute("SELECT * FROM bookings WHERE flight_id = ?", (flight_id,))
        if cursor.fetchone():
            print(Fore.RED + "Cannot delete flight. Bookings exist for this flight.")
            return

        # Confirmation
        confirm = input("Are you sure you want to delete this flight? (Y/N): ").strip().upper()

        if confirm == "Y":
            cursor.execute("DELETE FROM flights WHERE flight_id = ?", (flight_id,))
            conn.commit()
            print(Fore.GREEN + "Flight deleted successfully!")
        else:
            print(Fore.YELLOW + "Deletion cancelled.")

    except Exception as e:
        print(Fore.RED + f"Error: {e}")

    finally:
        conn.close()

def view_flight_menu():
    while True:
        print("\n===== VIEW FLIGHTS =====")
        print("1. View All Flights")
        print("2. View Available Flights")
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_all_flights()
        elif choice == "2":
            view_available_flights()
        elif choice == "3":
            break
        else:
            print("Invalid Choice")

def search_flight_menu():
    while True:
        print("\n===== SEARCH FLIGHT =====")
        print("1. Search by Flight ID")
        print("2. Search by Source & Destination")
        print("3. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            search_by_flight_id()
        elif choice == "2":
            search_by_source_destination()
        elif choice == "3":
            break
        else:
            print("Invalid Choice")
def update_flight_menu():
    while True:
        print("\n===== UPDATE FLIGHT =====")
        print("1. Update Available Seats")
        print("2. Update Schedule")
        print("3. Update Fare")
        print("4. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            update_available_seats()
        elif choice == "2":
            update_schedule()
        elif choice == "3":
            update_fare()
        elif choice == "4":
            break
        else:
            print("Invalid Choice")
def delete_flight_menu():
    while True:
        print("\n===== DELETE FLIGHT =====")
        print("1. Delete Flight")
        print("2. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            delete_flight()
        elif choice == "2":
            break
        else:
            print("Invalid Choice")                                    
   