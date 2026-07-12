from database import get_connection
from rich.console import Console
from rich.table import Table
from colorama import Fore, Style, init

console = Console() #object
def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()

init(autoreset=True)

conn = get_connection()
cursor = conn.cursor()

# ==========================================================
# REPORTS MENU
# ==========================================================
def reports_menu():
    while True:
        heading("REPORTS MENU")
        print("1. Flight Report")
        print("2. Passenger Report")
        print("3. Booking Report")
        print("4. Revenue Report")
        print("5. Back")
        try:
            ch = int(input("\nEnter Choice : "))

            match ch:

                case 1:
                    flight_report_menu()

                case 2:
                    passenger_report_menu()

                case 3:
                    booking_report_menu()

                case 4:
                     revenue_report_menu()

                case 5:
                    
                    break

                case _:
                    print("Invalid Choice.")

        except Exception as e:
            print("Error :", e)


# ==========================================================
# FLIGHT REPORT MENU
# ==========================================================

def flight_report_menu():

    while True:

        heading("FLIGHT REPORT")
        print("1. Daily Flight Report")
        print("2. Monthly Flight Report")
        print("3. Back")

        try:

            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    daily_flight_report()

                case 2:
                    monthly_flight_report()

                case 3:
                    break

                case _:
                    print("Invalid Choice.")

        except Exception as e:
            print("Error :", e)


# ==========================================================
# 7.1.1 DAILY FLIGHT REPORT
# ==========================================================

def daily_flight_report():
    heading("DAILY FLIGHT REPORT")
    try:
        date = input("Enter Date (YYYY-MM-DD) : ")
        cursor.execute("""
        SELECT
        flight_id,
        airline_id,
        source_airport_id,
        destination_airport_id,
        departure_date,
        departure_time,
        fare,
        available_seats
        FROM flights
        WHERE departure_date = ?
        """, (date,))
        rows = cursor.fetchall()
        if not rows:
            print("No Flight Found.")
            return
        print()
        table = Table(title="Daily Flight Report")

        table.add_column("Flight ID")
        table.add_column("Airline ID")
        table.add_column("Source")
        table.add_column("Destination")
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Fare")
        table.add_column("Seats")

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5]),
                str(row[6]),
                str(row[7])
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)


# ==========================================================
# 7.1.2 MONTHLY FLIGHT REPORT
# ==========================================================

def monthly_flight_report():
    heading("MONTHLY FLIGHT REPORT")
    try:

        month = input("Enter Month (YYYY-MM) : ")

        cursor.execute("""
        SELECT
        flight_id,
        airline_id,
        source_airport_id,
        destination_airport_id,
        departure_date,
        departure_time,
        fare,
        available_seats
        FROM flights
        WHERE substr(departure_date,1,7)=?
        """, (month,))

        rows = cursor.fetchall()

        if not rows:
            print("No Flight Found.")
            return

        table = Table(title="Monthly Flight Report")

        table.add_column("Flight ID")
        table.add_column("Airline ID")
        table.add_column("Source")
        table.add_column("Destination")
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Fare")
        table.add_column("Seats")

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5]),
                str(row[6]),
                str(row[7])
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)

# ==========================================================
# PASSENGER REPORT MENU
# ==========================================================

def passenger_report_menu():
    while True:
        heading("PASSENGER REPORT")
        print("1. All Passengers")
        print("2. Passenger by Flight")
        print("3. Back")

        try:

            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    all_passengers_report()

                case 2:
                    passenger_by_flight_report()

                case 3:
                    break

                case _:
                    print("Invalid Choice.")

        except Exception as e:
            print("Error :", e)


# ==========================================================
# 7.2.1 ALL PASSENGERS REPORT
# ==========================================================

def all_passengers_report():
    heading("ALL PASSENGERS REPORT")
    try:

        cursor.execute("""
        SELECT
        passenger_id,
        passenger_name,
        age,
        gender,
        phone
        FROM passengers
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No Passenger Found.")
            return

        table = Table(title="All Passengers")

        table.add_column("Passenger ID")
        table.add_column("Passenger Name")
        table.add_column("Age")
        table.add_column("Gender")
        table.add_column("Phone")

        for row in rows:

            table.add_row(
                str(row[0]),
                row[1],
                str(row[2]),
                row[3],
                row[4]
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)


# ==========================================================
# 7.2.2 PASSENGER BY FLIGHT REPORT
# ==========================================================

def passenger_by_flight_report():
    heading("PASSENGER BY FLIGHT REPORT")
    try:

        flight_id = int(input("Enter Flight ID : "))

        cursor.execute("""
        SELECT

        passengers.passenger_id,
        passengers.passenger_name,
        passengers.age,
        passengers.gender,
        passengers.phone,
        bookings.seat_no,
        bookings.status

        FROM passengers

        INNER JOIN bookings

        ON passengers.passenger_id = bookings.passenger_id

        WHERE bookings.flight_id = ?

        """, (flight_id,))

        rows = cursor.fetchall()

        if not rows:
            print("No Passenger Found For This Flight.")
            return

        table = Table(title=f"Passengers of Flight {flight_id}")

        table.add_column("Passenger ID")
        table.add_column("Passenger Name")
        table.add_column("Age")
        table.add_column("Gender")
        table.add_column("Phone")
        table.add_column("Seat No")
        table.add_column("Status")

        for row in rows:

            table.add_row(
                str(row[0]),
                row[1],
                str(row[2]),
                row[3],
                row[4],
                row[5],
                row[6]
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)

# ==========================================================
# BOOKING REPORT MENU
# ==========================================================

def booking_report_menu():

    while True:
        heading("BOOKING REPORT")
        print("1. Daily Bookings")
        print("2. Monthly Bookings")
        print("3. Cancelled Bookings")
        print("4. Back")

        try:

            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    daily_booking_report()

                case 2:
                    monthly_booking_report()

                case 3:
                    cancelled_booking_report()

                case 4:
                    break

                case _:
                    print("Invalid Choice.")

        except Exception as e:
            print("Error :", e)


# ==========================================================
# 7.3.1 DAILY BOOKING REPORT
# ==========================================================
def daily_booking_report():
    heading("DAILY BOOKING REPORT")
    try:
        booking_date = input("Enter Date (YYYY-MM-DD) : ")
        cursor.execute("""
        SELECT
        booking_id,
        passenger_id,
        flight_id,
        booking_date,
        seat_no,
        status
        FROM bookings
        WHERE booking_date = ?
        """, (booking_date,))
        rows = cursor.fetchall()
        if not rows:
            print("No Booking Found.")
            return
        table = Table(title="Daily Booking Report")
        table.add_column("Booking ID")
        table.add_column("Passenger ID")
        table.add_column("Flight ID")
        table.add_column("Booking Date")
        table.add_column("Seat No")
        table.add_column("Status")

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                row[3],
                row[4],
                row[5]
            )

        console.print(table)
    except Exception as e:
        print("Error :", e)
# ==========================================================
# 7.3.2 MONTHLY BOOKING REPORT
# ==========================================================

def monthly_booking_report():
    heading("MONTHLY BOOKING REPORT")
    try:
        month = input("Enter Month (YYYY-MM) : ")
        cursor.execute("""
        SELECT
        booking_id,
        passenger_id,
        flight_id,
        booking_date,
        seat_no,
        status
        FROM bookings
        WHERE substr(booking_date,1,7)=?
        """, (month,))
        rows = cursor.fetchall()
        if not rows:
            print("No Booking Found.")
            return
        table = Table(title="Monthly Booking Report")

        table.add_column("Booking ID")
        table.add_column("Passenger ID")
        table.add_column("Flight ID")
        table.add_column("Booking Date")
        table.add_column("Seat No")
        table.add_column("Status")

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                row[3],
                row[4],
                row[5]
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)


# ==========================================================
# 7.3.3 CANCELLED BOOKING REPORT
# ==========================================================

def cancelled_booking_report():
    heading("CANCELLED BOOKING REPORT")
    try:

        cursor.execute("""
        SELECT
        booking_id,
        passenger_id,
        flight_id,
        booking_date,
        seat_no,
        status
        FROM bookings
        WHERE status='Cancelled'
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No Cancelled Bookings Found.")
            return

        table = Table(title="Cancelled Booking Report")

        table.add_column("Booking ID")
        table.add_column("Passenger ID")
        table.add_column("Flight ID")
        table.add_column("Booking Date")
        table.add_column("Seat No")
        table.add_column("Status")

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                row[3],
                row[4],
                row[5]
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)   
# ==========================================================
# REVENUE REPORT MENU
# ==========================================================

def revenue_report_menu():
    
    while True:

        heading("REVENUE REPORT")
        print("1. Daily Revenue")
        print("2. Monthly Revenue")
        print("3. Yearly Revenue")
        print("4. Back")

        try:

            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    daily_revenue_report()

                case 2:
                    monthly_revenue_report()

                case 3:
                    yearly_revenue_report()

                case 4:
                    break

                case _:
                    print("Invalid Choice.")

        except Exception as e:
            print("Error :", e)


# ==========================================================
# 7.4.1 DAILY REVENUE REPORT
# ==========================================================

def daily_revenue_report():
    heading("DAILY REVENUE REPORT")
    try:

        payment_date = input("Enter Date (YYYY-MM-DD) : ")

        cursor.execute("""
        SELECT
        payment_date,
        COUNT(payment_id),
        SUM(amount)

        FROM payments

        WHERE payment_date = ?
        AND payment_status='Success'
        """, (payment_date,))

        row = cursor.fetchone()

        table = Table(title="Daily Revenue Report")

        table.add_column("Date")
        table.add_column("Total Payments")
        table.add_column("Revenue")

        if row and row[2] is not None:

            table.add_row(
                row[0],
                str(row[1]),
                "₹ " + str(row[2])
            )

        else:

            table.add_row(
                payment_date,
                "0",
                "₹ 0"
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)


# ==========================================================
# 7.4.2 MONTHLY REVENUE REPORT
# ==========================================================

def monthly_revenue_report():
    heading("MONTHLY REVENUE REPORT")
    try:

        month = input("Enter Month (YYYY-MM) : ")

        cursor.execute("""
        SELECT

        substr(payment_date,1,7),
        COUNT(payment_id),
        SUM(amount)

        FROM payments

        WHERE substr(payment_date,1,7)=?
        AND payment_status='Success'
        """, (month,))

        row = cursor.fetchone()

        table = Table(title="Monthly Revenue Report")

        table.add_column("Month")
        table.add_column("Total Payments")
        table.add_column("Revenue")

        if row and row[2] is not None:

            table.add_row(
                row[0],
                str(row[1]),
                "₹ " + str(row[2])
            )

        else:

            table.add_row(
                month,
                "0",
                "₹ 0"
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)


# ==========================================================
# 7.4.3 YEARLY REVENUE REPORT
# ==========================================================

def yearly_revenue_report():
    heading("YEARLY REVENUE REPORT")
    try:

        year = input("Enter Year (YYYY) : ")

        cursor.execute("""
        SELECT

        substr(payment_date,1,4),
        COUNT(payment_id),
        SUM(amount)

        FROM payments

        WHERE substr(payment_date,1,4)=?
        AND payment_status='Success'
        """, (year,))

        row = cursor.fetchone()

        table = Table(title="Yearly Revenue Report")

        table.add_column("Year")
        table.add_column("Total Payments")
        table.add_column("Revenue")

        if row and row[2] is not None:

            table.add_row(
                row[0],
                str(row[1]),
                "₹ " + str(row[2])
            )

        else:

            table.add_row(
                year,
                "0",
                "₹ 0"
            )

        console.print(table)

    except Exception as e:
        print("Error :", e)             

if __name__ == "__main__":
    reports_menu()