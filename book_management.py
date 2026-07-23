from database import get_connection
from rich.console import Console
from rich.table import Table
from datetime import datetime


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = get_connection()
cursor = conn.cursor()

# Enable Foreign Key Support
cursor.execute("PRAGMA foreign_keys = ON")


# ============================================================
# RICH CONSOLE
# ============================================================

console = Console()


# ============================================================
# COMMON HEADING
# Only headings are colored
# ============================================================

def heading(title):

    print()

    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )

    print()


# ============================================================
# 1. SEARCH PASSENGER
# ============================================================

def search_passenger():

    heading("SEARCH PASSENGER")

    passenger_id = input(
        "Enter Passenger ID : "
    ).strip()

    if not passenger_id.isdigit():

        print("Invalid Passenger ID.")
        return None

    try:

        cursor.execute(
            """
            SELECT
                passenger_id,
                passenger_name,
                age,
                gender,
                phone
            FROM passengers
            WHERE passenger_id = ?
            """,
            (int(passenger_id),)
        )

        passenger = cursor.fetchone()

        if not passenger:

            print("Passenger Not Found.")
            return None

        table = Table(
            show_header=True,
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column(
            "Passenger ID",
            style="bright_yellow"
        )

        table.add_column(
            "Passenger Name",
            style="bright_cyan"
        )

        table.add_column("Age")
        table.add_column("Gender")

        table.add_column(
            "Phone",
            style="bright_green"
        )

        table.add_row(
            str(passenger[0]),
            str(passenger[1]),
            str(passenger[2]),
            str(passenger[3]),
            str(passenger[4])
        )

        console.print(table)

        return passenger[0]

    except Exception as e:

        print(
            f"Error while searching passenger: {e}"
        )

        return None


# ============================================================
# 2. SEARCH FLIGHT
# Source is mandatory
# Destination and Date are optional
# ============================================================

def search_flight():

    heading("SEARCH FLIGHT")

    source = input(
        "Enter Source Airport or City : "
    ).strip()

    if not source:

        print(
            "Source Airport or City Cannot Be Empty."
        )

        return None

    destination = input(
        "Enter Destination Airport or City (optional) : "
    ).strip()

    departure_date = input(
        "Enter Departure Date (YYYY-MM-DD) (optional) : "
    ).strip()

    try:

        cursor.execute(
            """
            SELECT
                f.flight_id,
                f.flight_number,

                source.airport_name,
                source.city,

                destination.airport_name,
                destination.city,

                f.departure_date,
                f.departure_time,

                f.fare,
                f.available_seats

            FROM flights f

            JOIN airports source
                ON f.source_airport_id =
                   source.airport_id

            JOIN airports destination
                ON f.destination_airport_id =
                   destination.airport_id

            WHERE
            (
                LOWER(source.airport_name) LIKE LOWER(?)
                OR
                LOWER(source.city) LIKE LOWER(?)
            )

            AND
            (
                ? = ''
                OR
                LOWER(destination.airport_name) LIKE LOWER(?)
                OR
                LOWER(destination.city) LIKE LOWER(?)
            )

            AND
            (
                ? = ''
                OR
                f.departure_date = ?
            )

            AND f.available_seats > 0

            ORDER BY
                f.departure_date,
                f.departure_time
            """,
            (
                f"%{source}%",
                f"%{source}%",

                destination,
                f"%{destination}%",
                f"%{destination}%",

                departure_date,
                departure_date
            )
        )

        flights = cursor.fetchall()

        if not flights:

            print(
                "No Available Flight Found."
            )

            return None

        table = Table(
            show_header=True,
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column(
            "Flight ID",
            style="bright_yellow"
        )

        table.add_column(
            "Flight No.",
            style="bright_green"
        )

        table.add_column(
            "Source",
            style="bright_cyan"
        )

        table.add_column(
            "Destination",
            style="bright_cyan"
        )

        table.add_column("Date")
        table.add_column("Time")

        table.add_column(
            "Fare",
            style="bright_yellow"
        )

        table.add_column(
            "Seats",
            style="bright_green"
        )

        for flight in flights:

            table.add_row(
                str(flight[0]),
                str(flight[1]),
                f"{flight[2]} ({flight[3]})",
                f"{flight[4]} ({flight[5]})",
                str(flight[6]),
                str(flight[7]),
                str(flight[8]),
                str(flight[9])
            )

        console.print(table)

        flight_id = input(
            "\nEnter Flight ID to Select : "
        ).strip()

        if not flight_id.isdigit():

            print(
                "Invalid Flight ID."
            )

            return None

        flight_id = int(flight_id)

        valid_flight_ids = [
            flight[0]
            for flight in flights
        ]

        if flight_id not in valid_flight_ids:

            print(
                "Please Select a Flight ID "
                "From the Displayed Results."
            )

            return None

        return flight_id

    except Exception as e:

        print(
            f"Error while searching flight: {e}"
        )

        return None


# ============================================================
# 3. SELECT SEAT CLASS
# ============================================================

def select_seat_class(flight_id):

    heading("SELECT SEAT CLASS")

    try:

        cursor.execute(
            """
            SELECT DISTINCT
                seat_class
            FROM seats
            WHERE flight_id = ?
            AND seat_status = 'Available'
            ORDER BY seat_class
            """,
            (flight_id,)
        )

        classes = cursor.fetchall()

        if not classes:

            print(
                "No Available Seats Found."
            )

            return None

        for index, seat_class in enumerate(
            classes,
            start=1
        ):

            print(
                f"{index}  {seat_class[0]}"
            )

        print()

        choice = input(
            "Select Seat Class : "
        ).strip()

        if not choice.isdigit():

            print(
                "Invalid Choice."
            )

            return None

        choice = int(choice)

        if choice < 1 or choice > len(classes):

            print(
                "Invalid Seat Class Selection."
            )

            return None

        return classes[
            choice - 1
        ][0]

    except Exception as e:

        print(
            f"Error while selecting seat class: {e}"
        )

        return None


# ============================================================
# 4. SELECT SEAT TYPE
# ============================================================

def select_seat_type(
    flight_id,
    seat_class
):

    heading("SELECT SEAT TYPE")

    try:

        cursor.execute(
            """
            SELECT DISTINCT
                seat_type
            FROM seats
            WHERE flight_id = ?
            AND seat_class = ?
            AND seat_status = 'Available'
            ORDER BY seat_type
            """,
            (
                flight_id,
                seat_class
            )
        )

        seat_types = cursor.fetchall()

        if not seat_types:

            print(
                "No Available Seat Type Found."
            )

            return None

        for index, seat_type in enumerate(
            seat_types,
            start=1
        ):

            print(
                f"{index}  {seat_type[0]}"
            )

        print()

        choice = input(
            "Select Seat Type : "
        ).strip()

        if not choice.isdigit():

            print(
                "Invalid Choice."
            )

            return None

        choice = int(choice)

        if choice < 1 or choice > len(seat_types):

            print(
                "Invalid Seat Type Selection."
            )

            return None

        return seat_types[
            choice - 1
        ][0]

    except Exception as e:

        print(
            f"Error while selecting seat type: {e}"
        )

        return None


# ============================================================
# 5. SELECT AVAILABLE SEAT
# ============================================================

def select_seat(
    flight_id,
    seat_class,
    seat_type
):

    heading("AVAILABLE SEATS")

    try:

        cursor.execute(
            """
            SELECT
                seat_id,
                seat_no,
                seat_class,
                seat_type,
                seat_status
            FROM seats
            WHERE flight_id = ?
            AND seat_class = ?
            AND seat_type = ?
            AND seat_status = 'Available'
            ORDER BY seat_id
            """,
            (
                flight_id,
                seat_class,
                seat_type
            )
        )

        seats = cursor.fetchall()

        if not seats:

            print(
                "No Available Seats Found."
            )

            return None

        table = Table(
            show_header=True,
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column(
            "Seat ID",
            style="bright_yellow"
        )

        table.add_column(
            "Seat No.",
            style="bright_magenta"
        )

        table.add_column(
            "Seat Class",
            style="bright_cyan"
        )

        table.add_column(
            "Seat Type",
            style="bright_cyan"
        )

        table.add_column(
            "Status",
            style="bright_green"
        )

        for seat in seats:

            table.add_row(
                str(seat[0]),
                str(seat[1]),
                str(seat[2]),
                str(seat[3]),
                str(seat[4])
            )

        console.print(table)

        seat_id = input(
            "\nEnter Seat ID to Select : "
        ).strip()

        if not seat_id.isdigit():

            print(
                "Invalid Seat ID."
            )

            return None

        seat_id = int(seat_id)

        for seat in seats:

            if seat[0] == seat_id:

                return seat

        print(
            "Please Select a Seat ID "
            "From the Displayed Available Seats."
        )

        return None

    except Exception as e:

        print(
            f"Error while selecting seat: {e}"
        )

        return None


# ============================================================
# 6. BOOK TICKET
# ============================================================

def book_ticket():

    heading("BOOK TICKET")

    try:

        # ----------------------------------------------------
        # STEP 1 : SELECT PASSENGER
        # ----------------------------------------------------

        print("Step 1 : Select Passenger")

        passenger_id = search_passenger()

        if passenger_id is None:

            return

        # ----------------------------------------------------
        # STEP 2 : SELECT FLIGHT
        # ----------------------------------------------------

        print("\nStep 2 : Select Flight")

        flight_id = search_flight()

        if flight_id is None:

            return

        # ----------------------------------------------------
        # GET FLIGHT DETAILS
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                f.flight_id,
                f.flight_number,

                source.airport_name,
                source.city,

                destination.airport_name,
                destination.city,

                f.departure_date,
                f.departure_time,

                f.fare,
                f.available_seats

            FROM flights f

            JOIN airports source
                ON f.source_airport_id =
                   source.airport_id

            JOIN airports destination
                ON f.destination_airport_id =
                   destination.airport_id

            WHERE f.flight_id = ?
            """,
            (flight_id,)
        )

        flight = cursor.fetchone()

        if not flight:

            print(
                "Flight Not Found."
            )

            return

        if flight[9] <= 0:

            print(
                "No Seats Available on This Flight."
            )

            return

        # ----------------------------------------------------
        # STEP 3 : SELECT SEAT CLASS
        # ----------------------------------------------------

        print("\nStep 3 : Select Seat Class")

        seat_class = select_seat_class(
            flight_id
        )

        if seat_class is None:

            return

        # ----------------------------------------------------
        # STEP 4 : SELECT SEAT TYPE
        # ----------------------------------------------------

        print("\nStep 4 : Select Seat Type")

        seat_type = select_seat_type(
            flight_id,
            seat_class
        )

        if seat_type is None:

            return

        # ----------------------------------------------------
        # STEP 5 : SELECT SEAT
        # ----------------------------------------------------

        print("\nStep 5 : Select Seat")

        selected_seat = select_seat(
            flight_id,
            seat_class,
            seat_type
        )

        if selected_seat is None:

            return

        seat_id = selected_seat[0]
        seat_no = selected_seat[1]

        # ----------------------------------------------------
        # BOOKING SUMMARY
        # ----------------------------------------------------

        heading("BOOKING SUMMARY")

        table = Table(
            show_header=True,
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column(
            "Field",
            style="bright_cyan"
        )

        table.add_column(
            "Details",
            style="white"
        )

        table.add_row(
            "Passenger ID",
            str(passenger_id)
        )

        table.add_row(
            "Flight Number",
            str(flight[1])
        )

        table.add_row(
            "Source",
            f"{flight[2]} ({flight[3]})"
        )

        table.add_row(
            "Destination",
            f"{flight[4]} ({flight[5]})"
        )

        table.add_row(
            "Departure Date",
            str(flight[6])
        )

        table.add_row(
            "Departure Time",
            str(flight[7])
        )

        table.add_row(
            "Seat Number",
            str(seat_no)
        )

        table.add_row(
            "Seat Class",
            str(seat_class)
        )

        table.add_row(
            "Seat Type",
            str(seat_type)
        )

        table.add_row(
            "Fare",
            str(flight[8])
        )

        console.print(table)

        # ----------------------------------------------------
        # CONFIRM BOOKING
        # ----------------------------------------------------

        confirm = input(
            "\nConfirm Booking (Y/N) : "
        ).strip().upper()

        if confirm != "Y":

            print(
                "Booking Cancelled by User."
            )

            return

        # ----------------------------------------------------
        # CURRENT DATE
        # Only booking_date is used
        # ----------------------------------------------------

        booking_date = datetime.now().strftime(
            "%Y-%m-%d"
        )

        # ----------------------------------------------------
        # START TRANSACTION
        # ----------------------------------------------------

        conn.execute("BEGIN")

        # ----------------------------------------------------
        # CHECK SELECTED SEAT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT seat_id
            FROM seats
            WHERE seat_id = ?
            AND flight_id = ?
            AND seat_status = 'Available'
            """,
            (
                seat_id,
                flight_id
            )
        )

        if not cursor.fetchone():

            conn.rollback()

            print(
                "Booking Failed. "
                "Selected Seat is No Longer Available."
            )

            return

        # ----------------------------------------------------
        # INSERT BOOKING
        # booking_time REMOVED
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO bookings
            (
                passenger_id,
                flight_id,
                seat_id,
                booking_date,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                passenger_id,
                flight_id,
                seat_id,
                booking_date,
                "Confirmed"
            )
        )

        booking_id = cursor.lastrowid

        # ----------------------------------------------------
        # UPDATE SEAT STATUS
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE seats

            SET seat_status = 'Booked'

            WHERE seat_id = ?

            AND flight_id = ?

            AND seat_status = 'Available'
            """,
            (
                seat_id,
                flight_id
            )
        )

        if cursor.rowcount == 0:

            conn.rollback()

            print(
                "Booking Failed. "
                "Seat Could Not Be Reserved."
            )

            return

        # ----------------------------------------------------
        # DECREASE AVAILABLE SEATS
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE flights

            SET available_seats =
                available_seats - 1

            WHERE flight_id = ?

            AND available_seats > 0
            """,
            (flight_id,)
        )

        if cursor.rowcount == 0:

            conn.rollback()

            print(
                "Booking Failed. "
                "No Available Seats."
            )

            return

        # ----------------------------------------------------
        # SAVE CHANGES
        # ----------------------------------------------------

        conn.commit()

        # ----------------------------------------------------
        # BOOKING CONFIRMED
        # ----------------------------------------------------

        heading("BOOKING CONFIRMED")

        table = Table(
            show_header=True,
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column(
            "Field",
            style="bright_cyan"
        )

        table.add_column(
            "Details"
        )

        table.add_row(
            "Booking ID",
            str(booking_id)
        )

        table.add_row(
            "Passenger ID",
            str(passenger_id)
        )

        table.add_row(
            "Flight Number",
            str(flight[1])
        )

        table.add_row(
            "Source",
            f"{flight[2]} ({flight[3]})"
        )

        table.add_row(
            "Destination",
            f"{flight[4]} ({flight[5]})"
        )

        table.add_row(
            "Seat Number",
            str(seat_no)
        )

        table.add_row(
            "Seat Class",
            str(seat_class)
        )

        table.add_row(
            "Seat Type",
            str(seat_type)
        )

        table.add_row(
            "Booking Date",
            booking_date
        )

        table.add_row(
            "Booking Status",
            "Confirmed"
        )

        console.print(table)

        print(
            "\nTicket Booked Successfully.\n to confirmed your booking please confirm payment"
            
        )

    except Exception as e:

        conn.rollback()

        print(
            f"Error while booking ticket: {e}"
        )


# ============================================================
# 7. VIEW BOOKING
# ============================================================

def view_booking():

    heading("VIEW BOOKING")

    booking_id = input(
        "Enter Booking ID : "
    ).strip()

    if not booking_id.isdigit():

        print(
            "Invalid Booking ID."
        )

        return

    try:

        cursor.execute(
            """
            SELECT
                b.booking_id,
                p.passenger_name,
                p.phone,
                f.flight_number,

                source.airport_name,
                source.city,

                destination.airport_name,
                destination.city,

                f.departure_date,
                f.departure_time,

                s.seat_no,
                s.seat_class,
                s.seat_type,

                f.fare,

                b.booking_date,
                b.status

            FROM bookings b

            JOIN passengers p
                ON b.passenger_id =
                   p.passenger_id

            JOIN flights f
                ON b.flight_id =
                   f.flight_id

            JOIN seats s
                ON b.seat_id =
                   s.seat_id

            JOIN airports source
                ON f.source_airport_id =
                   source.airport_id

            JOIN airports destination
                ON f.destination_airport_id =
                   destination.airport_id

            WHERE b.booking_id = ?
            """,
            (int(booking_id),)
        )

        booking = cursor.fetchone()

        if not booking:

            print(
                "Booking Not Found."
            )

            return

        table = Table(
            show_header=True,
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column(
            "Field",
            style="bright_cyan"
        )

        table.add_column(
            "Details"
        )

        table.add_row(
            "Booking ID",
            str(booking[0])
        )

        table.add_row(
            "Passenger",
            str(booking[1])
        )

        table.add_row(
            "Phone",
            str(booking[2])
        )

        table.add_row(
            "Flight",
            str(booking[3])
        )

        table.add_row(
            "Source",
            f"{booking[4]} ({booking[5]})"
        )

        table.add_row(
            "Destination",
            f"{booking[6]} ({booking[7]})"
        )

        table.add_row(
            "Departure Date",
            str(booking[8])
        )

        table.add_row(
            "Departure Time",
            str(booking[9])
        )

        table.add_row(
            "Seat Number",
            str(booking[10])
        )

        table.add_row(
            "Seat Class",
            str(booking[11])
        )

        table.add_row(
            "Seat Type",
            str(booking[12])
        )

        table.add_row(
            "Fare",
            str(booking[13])
        )

        table.add_row(
            "Booking Date",
            str(booking[14])
        )

        table.add_row(
            "Booking Status",
            str(booking[15])
        )

        console.print(table)

    except Exception as e:

        print(
            f"Error while viewing booking: {e}"
        )


# ============================================================
# 8. CANCEL BOOKING
# ============================================================

def cancel_booking():

    heading("CANCEL BOOKING")

    booking_id = input(
        "Enter Booking ID : "
    ).strip()

    if not booking_id.isdigit():

        print(
            "Invalid Booking ID."
        )

        return

    booking_id = int(booking_id)

    try:

        cursor.execute(
            """
            SELECT
                b.booking_id,
                p.passenger_name,
                f.flight_number,

                source.city,
                destination.city,

                f.departure_date,
                f.departure_time,

                b.flight_id,

                s.seat_id,
                s.seat_no,
                s.seat_class,
                s.seat_type,

                f.fare,
                b.status

            FROM bookings b

            JOIN passengers p
                ON b.passenger_id =
                   p.passenger_id

            JOIN flights f
                ON b.flight_id =
                   f.flight_id

            JOIN seats s
                ON b.seat_id =
                   s.seat_id

            JOIN airports source
                ON f.source_airport_id =
                   source.airport_id

            JOIN airports destination
                ON f.destination_airport_id =
                   destination.airport_id

            WHERE b.booking_id = ?
            """,
            (booking_id,)
        )

        booking = cursor.fetchone()

        if not booking:

            print(
                "Booking Not Found."
            )

            return

        table = Table(
            show_header=True,
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column(
            "Field",
            style="bright_cyan"
        )

        table.add_column(
            "Details"
        )

        table.add_row(
            "Booking ID",
            str(booking[0])
        )

        table.add_row(
            "Passenger",
            str(booking[1])
        )

        table.add_row(
            "Flight",
            str(booking[2])
        )

        table.add_row(
            "Source",
            str(booking[3])
        )

        table.add_row(
            "Destination",
            str(booking[4])
        )

        table.add_row(
            "Departure Date",
            str(booking[5])
        )

        table.add_row(
            "Departure Time",
            str(booking[6])
        )

        table.add_row(
            "Seat Number",
            str(booking[9])
        )

        table.add_row(
            "Seat Class",
            str(booking[10])
        )

        table.add_row(
            "Seat Type",
            str(booking[11])
        )

        table.add_row(
            "Fare",
            str(booking[12])
        )

        table.add_row(
            "Booking Status",
            str(booking[13])
        )

        console.print(table)

        if booking[13].lower() == "cancelled":

            print(
                "This Booking is Already Cancelled."
            )

            return

        confirm = input(
            "\nAre You Sure You Want To "
            "Cancel This Booking? (Y/N) : "
        ).strip().upper()

        if confirm != "Y":

            print(
                "Cancellation Process Stopped."
            )

            return

        conn.execute("BEGIN")

        # ----------------------------------------------------
        # UPDATE BOOKING STATUS
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE bookings

            SET
                status = ?,
                cancellation_reason = ?

            WHERE booking_id = ?
            """,
            (
                "Cancelled",
                "Passenger requested cancellation",
                booking_id
            )
        )

        # ----------------------------------------------------
        # RETURN SEAT
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE seats

            SET seat_status = 'Available'

            WHERE seat_id = ?

            AND flight_id = ?

            AND seat_status = 'Booked'
            """,
            (
                booking[8],
                booking[7]
            )
        )

        if cursor.rowcount == 0:

            conn.rollback()

            print(
                "Cancellation Failed. "
                "Seat Could Not Be Released."
            )

            return

        # ----------------------------------------------------
        # INCREASE AVAILABLE SEATS
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE flights

            SET available_seats =
                available_seats + 1

            WHERE flight_id = ?
            """,
            (booking[7],)
        )

        # ----------------------------------------------------
        # SAVE CHANGES
        # ----------------------------------------------------

        conn.commit()

        print(
            "\nBooking Cancelled Successfully."
        )

    except Exception as e:

        conn.rollback()

        print(
            f"Error while cancelling booking: {e}"
        )


# ============================================================
# 9. BOOKING HISTORY
# ============================================================

def booking_history():

    heading("BOOKING HISTORY")

    try:

        cursor.execute(
            """
            SELECT
                b.booking_id,
                p.passenger_name,
                f.flight_number,

                source.city,
                destination.city,

                s.seat_no,
                s.seat_class,
                s.seat_type,

                b.booking_date,
                b.status

            FROM bookings b

            JOIN passengers p
                ON b.passenger_id =
                   p.passenger_id

            JOIN flights f
                ON b.flight_id =
                   f.flight_id

            JOIN seats s
                ON b.seat_id =
                   s.seat_id

            JOIN airports source
                ON f.source_airport_id =
                   source.airport_id

            JOIN airports destination
                ON f.destination_airport_id =
                   destination.airport_id

            ORDER BY
                b.booking_id DESC
            """
        )

        bookings = cursor.fetchall()

        if not bookings:

            print(
                "No Booking History Found."
            )

            return

        table = Table(
            show_header=True,
            show_lines=True,
            padding=(0, 2),
            expand=False
        )

        table.add_column(
            "Booking ID",
            style="bright_yellow"
        )

        table.add_column(
            "Passenger",
            style="bright_cyan"
        )

        table.add_column(
            "Flight",
            style="bright_green"
        )

        table.add_column("Source")
        table.add_column("Destination")

        table.add_column(
            "Seat",
            style="bright_magenta"
        )

        table.add_column("Class")
        table.add_column("Type")
        table.add_column("Booking Date")

        table.add_column(
            "Status",
            style="bright_green"
        )

        for booking in bookings:

            table.add_row(
                str(booking[0]),
                str(booking[1]),
                str(booking[2]),
                str(booking[3]),
                str(booking[4]),
                str(booking[5]),
                str(booking[6]),
                str(booking[7]),
                str(booking[8]),
                str(booking[9])
            )

        console.print(table)

    except Exception as e:

        print(
            f"Error while fetching booking history: {e}"
        )


# ============================================================
# 10. BOOKING MANAGEMENT MENU
# Menu is plain text
# Only heading is colored
# ============================================================

def booking_management():

    while True:

        heading("BOOKING MANAGEMENT")

        print("1  Book Ticket")
        print("2  View Booking")
        print("3  Cancel Booking")
        print("4  Booking History")
        print("5  Back")

        print()

        choice = input(
            "Enter Your Choice : "
        ).strip()

        if choice == "1":

            book_ticket()

        elif choice == "2":

            view_booking()

        elif choice == "3":

            cancel_booking()

        elif choice == "4":

            booking_history()

        elif choice == "5":

            break

        else:

            print(
                "Invalid Choice. Please Try Again."
            )


# ============================================================
# RUN MODULE DIRECTLY
# ============================================================

if __name__ == "__main__":

    try:

        booking_management()

    finally:

        conn.close()