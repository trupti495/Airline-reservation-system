from database import get_connection
import sqlite3

from rich.table import Table
from rich.console import Console
from colorama import Fore, init


# ============================================================
# INITIALIZATION
# ============================================================

init(autoreset=True)
console = Console()


# ============================================================
# COMMON HEADING
# ============================================================

def heading(title):

    print()

    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )

    print()


# ============================================================
# COMMON FLIGHT TABLE
# White Border + Colored Text + Lines Between Rows
# ============================================================

def create_flight_table(title="Flight Details"):

    table = Table(
        title=title,
        border_style="white",
        show_lines=True
    )

    table.add_column(
        "Flight ID",
        justify="center",
        style="cyan"
    )

    table.add_column(
        "Flight No.",
        justify="center",
        style="green"
    )

    table.add_column(
        "Airline",
        style="yellow"
    )

    table.add_column(
        "Source",
        style="magenta"
    )

    table.add_column(
        "Destination",
        style="magenta"
    )

    table.add_column(
        "Date",
        justify="center",
        style="cyan"
    )

    table.add_column(
        "Time",
        justify="center",
        style="cyan"
    )

    table.add_column(
        "Fare",
        justify="center",
        style="green"
    )

    table.add_column(
        "Available",
        justify="center",
        style="cyan"
    )

    return table


# ============================================================
# ADD ROW TO FLIGHT TABLE
# ============================================================

def add_flight_row(table, flight):

    table.add_row(

        str(flight[0]),

        str(flight[1]),

        str(flight[2]),

        str(flight[3]),

        str(flight[4]),

        str(flight[5]),

        str(flight[6]),

        f"₹ {flight[7]:.2f}",

        str(flight[8])

    )


# ============================================================
# VALIDATE DATE FORMAT
# ============================================================

def validate_date(date_text):

    try:

        from datetime import datetime

        datetime.strptime(
            date_text,
            "%Y-%m-%d"
        )

        return True

    except ValueError:

        return False


# ============================================================
# VALIDATE TIME FORMAT
# ============================================================

def validate_time(time_text):

    try:

        from datetime import datetime

        datetime.strptime(
            time_text,
            "%H:%M"
        )

        return True

    except ValueError:

        return False


# ============================================================
# 1. ADD FLIGHT
# ============================================================

def add_flight():

    heading("ADD FLIGHT")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ----------------------------------------------------
        # FLIGHT NUMBER
        # ----------------------------------------------------

        flight_number = input(
            "Enter Flight Number : "
        ).strip().upper()

        if not flight_number:

            print(
                Fore.RED +
                "Flight Number cannot be empty!"
            )

            return

        cursor.execute(
            """
            SELECT flight_id
            FROM flights
            WHERE flight_number = ?
            """,
            (flight_number,)
        )

        if cursor.fetchone():

            print(
                Fore.RED +
                "Flight Number already exists!"
            )

            return

        # ----------------------------------------------------
        # AIRLINE
        # ----------------------------------------------------

        airline_input = input(
            "Enter Airline ID : "
        ).strip()

        if not airline_input.isdigit():

            print(
                Fore.RED +
                "Invalid Airline ID!"
            )

            return

        airline_id = int(airline_input)

        cursor.execute(
            """
            SELECT airline_id
            FROM airlines
            WHERE airline_id = ?
            """,
            (airline_id,)
        )

        if cursor.fetchone() is None:

            print(
                Fore.RED +
                "Airline ID not found!"
            )

            return

        # ----------------------------------------------------
        # SOURCE AIRPORT
        # ----------------------------------------------------

        source_input = input(
            "Enter Source Airport ID : "
        ).strip()

        if not source_input.isdigit():

            print(
                Fore.RED +
                "Invalid Source Airport ID!"
            )

            return

        source_airport_id = int(source_input)

        cursor.execute(
            """
            SELECT airport_id
            FROM airports
            WHERE airport_id = ?
            """,
            (source_airport_id,)
        )

        if cursor.fetchone() is None:

            print(
                Fore.RED +
                "Source Airport ID not found!"
            )

            return

        # ----------------------------------------------------
        # DESTINATION AIRPORT
        # ----------------------------------------------------

        destination_input = input(
            "Enter Destination Airport ID : "
        ).strip()

        if not destination_input.isdigit():

            print(
                Fore.RED +
                "Invalid Destination Airport ID!"
            )

            return

        destination_airport_id = int(
            destination_input
        )

        cursor.execute(
            """
            SELECT airport_id
            FROM airports
            WHERE airport_id = ?
            """,
            (destination_airport_id,)
        )

        if cursor.fetchone() is None:

            print(
                Fore.RED +
                "Destination Airport ID not found!"
            )

            return

        # ----------------------------------------------------
        # SAME AIRPORT CHECK
        # ----------------------------------------------------

        if source_airport_id == destination_airport_id:

            print(
                Fore.RED +
                "Source and Destination Airport "
                "cannot be the same!"
            )

            return

        # ----------------------------------------------------
        # DEPARTURE DATE
        # ----------------------------------------------------

        departure_date = input(
            "Enter Departure Date (YYYY-MM-DD) : "
        ).strip()

        if not validate_date(departure_date):

            print(
                Fore.RED +
                "Invalid date format! "
                "Use YYYY-MM-DD."
            )

            return

        # ----------------------------------------------------
        # DEPARTURE TIME
        # ----------------------------------------------------

        departure_time = input(
            "Enter Departure Time (HH:MM) : "
        ).strip()

        if not validate_time(departure_time):

            print(
                Fore.RED +
                "Invalid time format! "
                "Use HH:MM."
            )

            return

        # ----------------------------------------------------
        # FARE
        # ----------------------------------------------------

        try:

            fare = float(
                input(
                    "Enter Base Fare : "
                ).strip()
            )

        except ValueError:

            print(
                Fore.RED +
                "Please enter a valid fare."
            )

            return

        if fare < 0:

            print(
                Fore.RED +
                "Fare cannot be negative!"
            )

            return

        # ----------------------------------------------------
        # SEAT DETAILS
        # ----------------------------------------------------

        print()

        print(
            Fore.CYAN +
            "Enter Seat Details"
        )

        print()

        try:

            economy_seats = int(
                input(
                    "Enter Economy Seats : "
                ).strip()
            )

            premium_economy_seats = int(
                input(
                    "Enter Premium Economy Seats : "
                ).strip()
            )

            business_seats = int(
                input(
                    "Enter Business Class Seats : "
                ).strip()
            )

        except ValueError:

            print(
                Fore.RED +
                "Seat counts must be numeric!"
            )

            return

        # ----------------------------------------------------
        # VALIDATE SEAT COUNTS
        # ----------------------------------------------------

        if (
            economy_seats < 0
            or premium_economy_seats < 0
            or business_seats < 0
        ):

            print(
                Fore.RED +
                "Seat count cannot be negative!"
            )

            return

        total_seats = (
            economy_seats
            +
            premium_economy_seats
            +
            business_seats
        )

        if total_seats == 0:

            print(
                Fore.RED +
                "At least one seat must be available!"
            )

            return

        # ----------------------------------------------------
        # INSERT FLIGHT
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO flights
            (
                flight_number,
                airline_id,
                source_airport_id,
                destination_airport_id,
                departure_date,
                departure_time,
                fare,
                total_seats,
                economy_seats,
                premium_economy_seats,
                business_seats,
                available_seats,
                available_economy_seats,
                available_premium_economy_seats,
                available_business_seats
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
            """,
            (
                flight_number,
                airline_id,
                source_airport_id,
                destination_airport_id,
                departure_date,
                departure_time,
                fare,
                total_seats,
                economy_seats,
                premium_economy_seats,
                business_seats,
                total_seats,
                economy_seats,
                premium_economy_seats,
                business_seats
            )
        )

        flight_id = cursor.lastrowid

        # ----------------------------------------------------
        # CREATE ECONOMY SEATS
        # ----------------------------------------------------

        for i in range(1, economy_seats + 1):

            seat_no = f"E{i}"

            cursor.execute(
                """
                INSERT INTO seats
                (
                    flight_id,
                    seat_no,
                    seat_class,
                    seat_type,
                    seat_status
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    flight_id,
                    seat_no,
                    "Economy",
                    "Window" if i % 2 == 1 else "Aisle",
                    "Available"
                )
            )

        # ----------------------------------------------------
        # CREATE PREMIUM ECONOMY SEATS
        # ----------------------------------------------------

        for i in range(1, premium_economy_seats + 1):

            seat_no = f"PE{i}"

            cursor.execute(
                """
                INSERT INTO seats
                (
                    flight_id,
                    seat_no,
                    seat_class,
                    seat_type,
                    seat_status
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    flight_id,
                    seat_no,
                    "Premium Economy",
                    "Window" if i % 2 == 1 else "Aisle",
                    "Available"
                )
            )

        # ----------------------------------------------------
        # CREATE BUSINESS SEATS
        # ----------------------------------------------------

        for i in range(1, business_seats + 1):

            seat_no = f"B{i}"

            cursor.execute(
                """
                INSERT INTO seats
                (
                    flight_id,
                    seat_no,
                    seat_class,
                    seat_type,
                    seat_status
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    flight_id,
                    seat_no,
                    "Business",
                    "Window" if i % 2 == 1 else "Aisle",
                    "Available"
                )
            )

        # ----------------------------------------------------
        # COMMIT
        # ----------------------------------------------------

        conn.commit()

        print()

        print(
            Fore.GREEN +
            "Flight added successfully!"
        )

        print(
            Fore.CYAN +
            f"Flight ID : {flight_id}"
        )

        print(
            Fore.CYAN +
            f"Flight Number : {flight_number}"
        )

        print(
            Fore.CYAN +
            f"Total Seats : {total_seats}"
        )

        print(
            Fore.CYAN +
            f"Economy : {economy_seats}"
        )

        print(
            Fore.CYAN +
            f"Premium Economy : {premium_economy_seats}"
        )

        print(
            Fore.CYAN +
            f"Business : {business_seats}"
        )

    except sqlite3.IntegrityError as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Database Error : {e}"
        )

    except Exception as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()


# ============================================================
# 2. VIEW ALL FLIGHTS
# ============================================================

def view_all_flights():

    heading("ALL FLIGHTS")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                f.flight_id,
                f.flight_number,
                a.airline_name,
                sa.airport_name,
                da.airport_name,
                f.departure_date,
                f.departure_time,
                f.fare,
                f.available_seats

            FROM flights f

            JOIN airlines a
                ON f.airline_id = a.airline_id

            JOIN airports sa
                ON f.source_airport_id = sa.airport_id

            JOIN airports da
                ON f.destination_airport_id = da.airport_id

            ORDER BY f.flight_id
            """
        )

        flights = cursor.fetchall()

        if not flights:

            print(
                "No Flight Records Found!"
            )

            return

        table = create_flight_table(
            "Flight Details"
        )

        for flight in flights:

            add_flight_row(
                table,
                flight
            )

        console.print(table)

    except Exception as e:

        print(
            "Error :",
            e
        )

    finally:

        conn.close()


# ============================================================
# 3. VIEW AVAILABLE FLIGHTS
# ============================================================

def view_available_flights():

    heading("AVAILABLE FLIGHTS")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                f.flight_id,
                f.flight_number,
                a.airline_name,
                sa.airport_name,
                da.airport_name,
                f.departure_date,
                f.departure_time,
                f.fare,
                f.available_seats

            FROM flights f

            JOIN airlines a
                ON f.airline_id = a.airline_id

            JOIN airports sa
                ON f.source_airport_id = sa.airport_id

            JOIN airports da
                ON f.destination_airport_id = da.airport_id

            WHERE f.available_seats > 0

            ORDER BY
                f.departure_date,
                f.departure_time
            """
        )

        flights = cursor.fetchall()

        if not flights:

            print(
                "No Available Flights Found!"
            )

            return

        table = create_flight_table(
            "Available Flight Details"
        )

        for flight in flights:

            add_flight_row(
                table,
                flight
            )

        console.print(table)

    except Exception as e:

        print(
            "Error :",
            e
        )

    finally:

        conn.close()


# ============================================================
# 4. SEARCH BY FLIGHT ID
# ============================================================

def search_by_flight_id():

    heading("SEARCH FLIGHT BY ID")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        flight_id = int(
            input(
                "Enter Flight ID : "
            )
        )

        cursor.execute(
            """
            SELECT
                f.flight_id,
                f.flight_number,
                a.airline_name,
                sa.airport_name,
                da.airport_name,
                f.departure_date,
                f.departure_time,
                f.fare,
                f.economy_seats,
                f.premium_economy_seats,
                f.business_seats,
                f.available_economy_seats,
                f.available_premium_economy_seats,
                f.available_business_seats

            FROM flights f

            JOIN airlines a
                ON f.airline_id = a.airline_id

            JOIN airports sa
                ON f.source_airport_id = sa.airport_id

            JOIN airports da
                ON f.destination_airport_id = da.airport_id

            WHERE f.flight_id = ?
            """,
            (flight_id,)
        )

        flight = cursor.fetchone()

        if not flight:

            print(
                Fore.RED +
                "Flight not found."
            )

            return

        display_flight_details(
            flight
        )

    except ValueError:

        print(
            Fore.RED +
            "Please enter a valid Flight ID."
        )

    except Exception as e:

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()


# ============================================================
# 5. SEARCH BY FLIGHT NUMBER
# ============================================================

def search_by_flight_number():

    heading("SEARCH FLIGHT BY NUMBER")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        flight_number = input(
            "Enter Flight Number : "
        ).strip().upper()

        if not flight_number:

            print(
                Fore.RED +
                "Flight Number cannot be empty."
            )

            return

        cursor.execute(
            """
            SELECT
                f.flight_id,
                f.flight_number,
                a.airline_name,
                sa.airport_name,
                da.airport_name,
                f.departure_date,
                f.departure_time,
                f.fare,
                f.economy_seats,
                f.premium_economy_seats,
                f.business_seats,
                f.available_economy_seats,
                f.available_premium_economy_seats,
                f.available_business_seats

            FROM flights f

            JOIN airlines a
                ON f.airline_id = a.airline_id

            JOIN airports sa
                ON f.source_airport_id = sa.airport_id

            JOIN airports da
                ON f.destination_airport_id = da.airport_id

            WHERE f.flight_number = ?
            """,
            (flight_number,)
        )

        flight = cursor.fetchone()

        if not flight:

            print(
                Fore.RED +
                "Flight not found."
            )

            return

        display_flight_details(
            flight
        )

    except Exception as e:

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()


# ============================================================
# DISPLAY FLIGHT DETAILS
# ============================================================

def display_flight_details(flight):

    table = Table(
        title="Flight Details",
        border_style="white",
        show_lines=True
    )

    table.add_column(
        "Field",
        style="cyan"
    )

    table.add_column(
        "Details",
        style="green"
    )

    table.add_row(
        "Flight ID",
        str(flight[0])
    )

    table.add_row(
        "Flight Number",
        str(flight[1])
    )

    table.add_row(
        "Airline",
        str(flight[2])
    )

    table.add_row(
        "Source Airport",
        str(flight[3])
    )

    table.add_row(
        "Destination Airport",
        str(flight[4])
    )

    table.add_row(
        "Departure Date",
        str(flight[5])
    )

    table.add_row(
        "Departure Time",
        str(flight[6])
    )

    table.add_row(
        "Base Fare",
        f"₹ {flight[7]:.2f}"
    )

    table.add_row(
        "Economy Seats",
        f"{flight[11]} / {flight[8]}"
    )

    table.add_row(
        "Premium Economy Seats",
        f"{flight[12]} / {flight[9]}"
    )

    table.add_row(
        "Business Seats",
        f"{flight[13]} / {flight[10]}"
    )

    console.print(table)

    print()

    print(
        Fore.CYAN +
        "Format: Available Seats / Total Seats"
    )


# ============================================================
# 6. SEARCH BY SOURCE & DESTINATION
# ============================================================

def search_by_source_destination():

    heading("SEARCH BY SOURCE & DESTINATION")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        source_airport = input(
            "Enter Source Airport Name : "
        ).strip()

        destination_airport = input(
            "Enter Destination Airport Name (Optional) : "
        ).strip()

        # Source is required
        if source_airport == "":
            print(
                Fore.RED +
                "Source Airport Name cannot be empty."
            )
            return

        # ----------------------------------------------------
        # SEARCH QUERY
        # Destination is optional
        # ----------------------------------------------------

        if destination_airport == "":

            cursor.execute(
                """
                SELECT
                    f.flight_id,
                    f.flight_number,
                    a.airline_name,
                    sa.airport_name,
                    da.airport_name,
                    f.departure_date,
                    f.departure_time,
                    f.fare,
                    f.available_seats

                FROM flights f

                JOIN airlines a
                    ON f.airline_id = a.airline_id

                JOIN airports sa
                    ON f.source_airport_id = sa.airport_id

                JOIN airports da
                    ON f.destination_airport_id = da.airport_id

                WHERE LOWER(sa.airport_name) LIKE ?

                ORDER BY
                    f.departure_date,
                    f.departure_time
                """,
                (
                    "%" + source_airport.lower() + "%",
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    f.flight_id,
                    f.flight_number,
                    a.airline_name,
                    sa.airport_name,
                    da.airport_name,
                    f.departure_date,
                    f.departure_time,
                    f.fare,
                    f.available_seats

                FROM flights f

                JOIN airlines a
                    ON f.airline_id = a.airline_id

                JOIN airports sa
                    ON f.source_airport_id = sa.airport_id

                JOIN airports da
                    ON f.destination_airport_id = da.airport_id

                WHERE LOWER(sa.airport_name) LIKE ?
                AND LOWER(da.airport_name) LIKE ?

                ORDER BY
                    f.departure_date,
                    f.departure_time
                """,
                (
                    "%" + source_airport.lower() + "%",
                    "%" + destination_airport.lower() + "%"
                )
            )

        flights = cursor.fetchall()

        # ----------------------------------------------------
        # NO RECORDS
        # ----------------------------------------------------

        if not flights:

            print(
                Fore.RED +
                "No flights found."
            )

            return

        # ----------------------------------------------------
        # CREATE TABLE
        # ----------------------------------------------------

        table = create_flight_table(
            "Search Results"
        )

        # ----------------------------------------------------
        # ADD FLIGHT ROWS
        # ----------------------------------------------------

        for flight in flights:

            add_flight_row(
                table,
                flight
            )

        # ----------------------------------------------------
        # DISPLAY TABLE
        # ----------------------------------------------------

        console.print(table)

    except Exception as e:

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()

# ============================================================
# 7. UPDATE AVAILABLE SEATS
# ============================================================

def update_available_seats():

    heading("UPDATE AVAILABLE SEATS")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        flight_number = input(
            "Enter Flight Number : "
        ).strip().upper()

        cursor.execute(
            """
            SELECT
                flight_id,
                economy_seats,
                premium_economy_seats,
                business_seats

            FROM flights

            WHERE flight_number = ?
            """,
            (flight_number,)
        )

        flight = cursor.fetchone()

        if flight is None:

            print(
                Fore.RED +
                "Flight not found."
            )

            return

        print()

        print("1. Economy")
        print("2. Premium Economy")
        print("3. Business")

        choice = input(
            "Select Seat Class : "
        ).strip()

        try:

            seats = int(
                input(
                    "Enter New Available Seats : "
                )
            )

        except ValueError:

            print(
                Fore.RED +
                "Please enter a valid number."
            )

            return

        if seats < 0:

            print(
                Fore.RED +
                "Seats cannot be negative."
            )

            return

        if choice == "1":

            column = "available_economy_seats"
            total_seats = flight[1]

        elif choice == "2":

            column = "available_premium_economy_seats"
            total_seats = flight[2]

        elif choice == "3":

            column = "available_business_seats"
            total_seats = flight[3]

        else:

            print(
                Fore.RED +
                "Invalid Seat Class."
            )

            return

        if seats > total_seats:

            print(
                Fore.RED +
                f"Available seats cannot be greater "
                f"than total seats ({total_seats})."
            )

            return

        cursor.execute(
            f"""
            UPDATE flights

            SET {column} = ?

            WHERE flight_number = ?
            """,
            (
                seats,
                flight_number
            )
        )

        cursor.execute(
            """
            SELECT
                available_economy_seats,
                available_premium_economy_seats,
                available_business_seats

            FROM flights

            WHERE flight_number = ?
            """,
            (flight_number,)
        )

        available = cursor.fetchone()

        total_available = (
            available[0]
            +
            available[1]
            +
            available[2]
        )

        cursor.execute(
            """
            UPDATE flights

            SET available_seats = ?

            WHERE flight_number = ?
            """,
            (
                total_available,
                flight_number
            )
        )

        conn.commit()

        print(
            Fore.GREEN +
            "Available seats updated successfully!"
        )

    except Exception as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()


# ============================================================
# 8. UPDATE SCHEDULE
# ============================================================

def update_schedule():

    heading("UPDATE FLIGHT SCHEDULE")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        flight_number = input(
            "Enter Flight Number : "
        ).strip().upper()

        departure_date = input(
            "Enter New Departure Date (YYYY-MM-DD) : "
        ).strip()

        if not validate_date(departure_date):

            print(
                Fore.RED +
                "Invalid date format!"
            )

            return

        departure_time = input(
            "Enter New Departure Time (HH:MM) : "
        ).strip()

        if not validate_time(departure_time):

            print(
                Fore.RED +
                "Invalid time format!"
            )

            return

        cursor.execute(
            """
            UPDATE flights

            SET
                departure_date = ?,
                departure_time = ?

            WHERE flight_number = ?
            """,
            (
                departure_date,
                departure_time,
                flight_number
            )
        )

        if cursor.rowcount == 0:

            print(
                Fore.RED +
                "Flight not found."
            )

            return

        conn.commit()

        print(
            Fore.GREEN +
            "Schedule updated successfully!"
        )

    except Exception as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()


# ============================================================
# 9. UPDATE FARE
# ============================================================

def update_fare():

    heading("UPDATE FLIGHT FARE")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        flight_number = input(
            "Enter Flight Number : "
        ).strip().upper()

        fare = float(
            input(
                "Enter New Fare : "
            )
        )

        if fare < 0:

            print(
                Fore.RED +
                "Fare cannot be negative."
            )

            return

        cursor.execute(
            """
            UPDATE flights

            SET fare = ?

            WHERE flight_number = ?
            """,
            (
                fare,
                flight_number
            )
        )

        if cursor.rowcount == 0:

            print(
                Fore.RED +
                "Flight not found."
            )

            return

        conn.commit()

        print(
            Fore.GREEN +
            "Fare updated successfully!"
        )

    except ValueError:

        print(
            Fore.RED +
            "Please enter a valid fare."
        )

    except Exception as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()


# ============================================================
# 10. DELETE FLIGHT BY ID
# ============================================================

def delete_flight():

    heading("DELETE FLIGHT BY ID")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        flight_id = int(
            input(
                "Enter Flight ID to delete : "
            )
        )

        cursor.execute(
            """
            SELECT flight_number
            FROM flights
            WHERE flight_id = ?
            """,
            (flight_id,)
        )

        flight = cursor.fetchone()

        if flight is None:

            print(
                Fore.RED +
                "Flight not found."
            )

            return

        cursor.execute(
            """
            SELECT booking_id
            FROM bookings
            WHERE flight_id = ?
            """,
            (flight_id,)
        )

        if cursor.fetchone():

            print(
                Fore.RED +
                "Cannot delete flight. "
                "Bookings exist for this flight."
            )

            return

        confirm = input(
            "Are you sure you want to delete "
            "this flight? (Y/N) : "
        ).strip().upper()

        if confirm != "Y":

            print(
                Fore.YELLOW +
                "Deletion cancelled."
            )

            return

        cursor.execute(
            """
            DELETE FROM seats
            WHERE flight_id = ?
            """,
            (flight_id,)
        )

        cursor.execute(
            """
            DELETE FROM flights
            WHERE flight_id = ?
            """,
            (flight_id,)
        )

        conn.commit()

        print(
            Fore.GREEN +
            "Flight deleted successfully!"
        )

    except ValueError:

        print(
            Fore.RED +
            "Please enter a valid Flight ID."
        )

    except sqlite3.IntegrityError as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Cannot delete flight : {e}"
        )

    except Exception as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()


# ============================================================
# 11. DELETE BY FLIGHT NUMBER
# ============================================================

def delete_by_flight_number():

    heading("DELETE FLIGHT BY NUMBER")

    conn = get_connection()
    cursor = conn.cursor()

    try:

        flight_number = input(
            "Enter Flight Number to delete : "
        ).strip().upper()

        cursor.execute(
            """
            SELECT flight_id
            FROM flights
            WHERE flight_number = ?
            """,
            (flight_number,)
        )

        flight = cursor.fetchone()

        if flight is None:

            print(
                Fore.RED +
                "Flight not found."
            )

            return

        flight_id = flight[0]

        cursor.execute(
            """
            SELECT booking_id
            FROM bookings
            WHERE flight_id = ?
            """,
            (flight_id,)
        )

        if cursor.fetchone():

            print(
                Fore.RED +
                "Cannot delete flight. "
                "Bookings exist for this flight."
            )

            return

        confirm = input(
            "Are you sure you want to delete "
            "this flight? (Y/N) : "
        ).strip().upper()

        if confirm != "Y":

            print(
                Fore.YELLOW +
                "Deletion cancelled."
            )

            return

        cursor.execute(
            """
            DELETE FROM seats
            WHERE flight_id = ?
            """,
            (flight_id,)
        )

        cursor.execute(
            """
            DELETE FROM flights
            WHERE flight_id = ?
            """,
            (flight_id,)
        )

        conn.commit()

        print(
            Fore.GREEN +
            "Flight deleted successfully!"
        )

    except sqlite3.IntegrityError as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Cannot delete flight : {e}"
        )

    except Exception as e:

        conn.rollback()

        print(
            Fore.RED +
            f"Error : {e}"
        )

    finally:

        conn.close()


# ============================================================
# VIEW FLIGHTS MENU
# ============================================================

def view_flight_menu():

    while True:

        heading("VIEW FLIGHTS")

        print("1. View All Flights")
        print("2. View Available Flights")
        print("3. Back")

        choice = input(
            "Enter Your Choice : "
        ).strip()

        if choice == "1":

            view_all_flights()

        elif choice == "2":

            view_available_flights()

        elif choice == "3":

            break

        else:

            print(
                Fore.RED +
                "Invalid Choice!"
            )


# ============================================================
# SEARCH FLIGHT MENU
# ============================================================

def search_flight_menu():

    while True:

        heading("SEARCH FLIGHT")

        print("1. Search by Flight ID")
        print("2. Search by Flight Number")
        print("3. Search by Source & Destination")
        print("4. Back")

        choice = input(
            "Enter Your Choice : "
        ).strip()

        if choice == "1":

            search_by_flight_id()

        elif choice == "2":

            search_by_flight_number()

        elif choice == "3":

            search_by_source_destination()

        elif choice == "4":

            break

        else:

            print(
                Fore.RED +
                "Invalid Choice!"
            )


# ============================================================
# UPDATE FLIGHT MENU
# ============================================================

def update_flight_menu():

    while True:

        heading("UPDATE FLIGHT")

        print("1. Update Available Seats")
        print("2. Update Schedule")
        print("3. Update Fare")
        print("4. Back")

        choice = input(
            "Enter Your Choice : "
        ).strip()

        if choice == "1":

            update_available_seats()

        elif choice == "2":

            update_schedule()

        elif choice == "3":

            update_fare()

        elif choice == "4":

            break

        else:

            print(
                Fore.RED +
                "Invalid Choice!"
            )


# ============================================================
# DELETE FLIGHT MENU
# ============================================================

def delete_flight_menu():

    while True:

        heading("DELETE FLIGHT")

        print("1. Delete by Flight ID")
        print("2. Delete by Flight Number")
        print("3. Back")

        choice = input(
            "Enter Your Choice : "
        ).strip()

        if choice == "1":

            delete_flight()

        elif choice == "2":

            delete_by_flight_number()

        elif choice == "3":

            break

        else:

            print(
                Fore.RED +
                "Invalid Choice!"
            )


# ============================================================
# MAIN FLIGHT MANAGEMENT MENU
# ============================================================

def flight_management():

    while True:

        heading("FLIGHT MANAGEMENT")

        print("1. Add Flight")
        print("2. View Flights")
        print("3. Search Flight")
        print("4. Update Flight")
        print("5. Delete Flight")
        print("6. Back")

        choice = input(
            "Enter Your Choice : "
        ).strip()

        if choice == "1":

            add_flight()

        elif choice == "2":

            view_flight_menu()

        elif choice == "3":

            search_flight_menu()

        elif choice == "4":

            update_flight_menu()

        elif choice == "5":

            delete_flight_menu()

        elif choice == "6":

            break

        else:

            print(
                Fore.RED +
                "Invalid Choice!"
            )


# ============================================================
# RUN MODULE DIRECTLY
# ============================================================

if __name__ == "__main__":

    flight_management()