from database import get_connection
import sqlite3
from rich.console import Console
from colorama import Fore, init
from tabulate import tabulate

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
            (airline_id, source_airport_id, destination_airport_id,
            departure_date, departure_time, fare, available_seats)
            VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        airline_id,
        source_airport_id,
        destination_airport_id,
        departure_date,
        departure_time,
        fare,
        available_seats
    ))

        conn.commit()
    
        print(Fore.GREEN + "Flight added successfully!")
    except sqlite3.IntegrityError:
        print(Fore.RED + "Foreign Key Constraint Error!")

    finally:
        conn.close()    

def view_all_flights():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()

    if not flights:
        print("\nNo flights found.")
        conn.close()
        return

        print("\n==================== ALL FLIGHTS ====================")
    print(f"Total Flights : {len(flights)}")
    print("-" * 95)

    print(f"{'Flight ID':<10}{'Airline':<10}{'Source':<10}{'Destination':<15}{'Date':<12}{'Time':<10}{'Fare':<10}{'Seats'}")
    print("-" * 95)

    for flight in flights:
        print(
            f"{flight[0]:<10}"
            f"{flight[1]:<10}"
            f"{flight[2]:<10}"
            f"{flight[3]:<15}"
            f"{flight[4]:<12}"
            f"{flight[5]:<10}"
            f"{flight[6]:<10}"
            f"{flight[7]}"
        )

    print("-" * 95)
    conn.close()                       

def view_available_flights():
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM flights WHERE available_seats > 0")
    flights = cursor.fetchall()
    
    if not flights:
        print("\nNo Available Flights.")
        conn.close()
        return

    print("\n================== AVAILABLE FLIGHTS ==================")
    print(f"Total Available Flights : {len(flights)}")
    print("-" * 95)

    print(f"{'Flight ID':<10}{'Airline':<10}{'Source':<10}{'Destination':<15}{'Date':<12}{'Time':<10}{'Fare':<10}{'Seats'}")
    print("-" * 95)

    for flight in flights:
        print(
            f"{flight[0]:<10}"
            f"{flight[1]:<10}"
            f"{flight[2]:<10}"
            f"{flight[3]:<15}"
            f"{flight[4]:<12}"
            f"{flight[5]:<10}"
            f"{flight[6]:<10}"
            f"{flight[7]}"
        )
    print("-" * 95)
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

    print("\n==================== FLIGHT DETAILS ====================")
    print("-" * 95)

    print(f"{'Flight ID':<10}{'Airline':<10}{'Source':<10}{'Destination':<15}{'Date':<12}{'Time':<10}{'Fare':<10}{'Seats'}")
    print("-" * 95)

    print(
        f"{flight[0]:<10}"
        f"{flight[1]:<10}"
        f"{flight[2]:<10}"
        f"{flight[3]:<15}"
        f"{flight[4]:<12}"
        f"{flight[5]:<10}"
        f"{flight[6]:<10}"
        f"{flight[7]}"
    )

    print("-" * 95)
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

    print("\n==================== SEARCH RESULTS ====================")
    print(f"Total Flights : {len(flights)}")
    print("-" * 95)

    print(f"{'Flight ID':<10}{'Airline':<10}{'Source':<10}{'Destination':<15}{'Date':<12}{'Time':<10}{'Fare':<10}{'Seats'}")
    print("-" * 95)

    for flight in flights:
        print(
            f"{flight[0]:<10}"
            f"{flight[1]:<10}"
            f"{flight[2]:<10}"
            f"{flight[3]:<15}"
            f"{flight[4]:<12}"
            f"{flight[5]:<10}"
            f"{flight[6]:<10}"
            f"{flight[7]}"
        )

    print("-" * 95)
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

        cursor.execute("DELETE FROM flights WHERE flight_id = ?", (flight_id,))
        conn.commit()

        print(Fore.GREEN + "Flight deleted successfully!")

    except Exception as e:
        print(Fore.RED + "Error:", e)

    finally:
        conn.close()
 

   