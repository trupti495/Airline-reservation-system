from database import get_connection
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
from matplotlib.ticker import MaxNLocator

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
        print("3. Yearly flight report")
        print("4.exit")

        try:

            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    daily_flight_report()

                case 2:
                    monthly_flight_report()

                case 3:
                    yearly_flight_report()
                case 4:
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
        flight_ids = []
        available_seats = []

        for row in rows:
            flight_ids.append(str(row[0]))
            available_seats.append(row[7])

        plt.figure(figsize=(8,5))
        plt.bar(flight_ids, available_seats)

        plt.title("Daily Flight Report")
        plt.xlabel("Flight ID")
        plt.ylabel("Available Seats")

        for i, value in enumerate(available_seats):
            plt.text(i, value, str(value), ha="center")

        plt.grid(axis="y")
        plt.show()

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
        flight_ids = []
        available_seats = []

        for row in rows:
         flight_ids.append(str(row[0]))
         available_seats.append(row[7])

        plt.figure(figsize=(9,5))
        plt.bar(flight_ids, available_seats)

        plt.title("Monthly Flight Report")
        plt.xlabel("Flight ID")
        plt.ylabel("Available Seats")

        for i, value in enumerate(available_seats):
            plt.text(i, value, str(value), ha="center")

        plt.grid(axis="y")
        plt.show()

    except Exception as e:
        print("Error :", e)

def yearly_flight_report():

    heading("YEARLY FLIGHT REPORT")

    try:

        year = input("Enter Year (YYYY) : ")

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
        WHERE substr(departure_date,1,4)=?
        """,(year,))

        rows = cursor.fetchall()

        if not rows:
            print("No Flight Found.")
            return

        flight_ids = []
        available_seats = []

        for row in rows:
            flight_ids.append(str(row[0]))
            available_seats.append(row[7])

        plt.figure(figsize=(9,5))
        plt.bar(flight_ids, available_seats)

        plt.title("Yearly Flight Report")
        plt.xlabel("Flight ID")
        plt.ylabel("Available Seats")

        for i, value in enumerate(available_seats):
            plt.text(i, value, str(value), ha="center")

        plt.grid(axis="y")
        plt.show()

    except Exception as e:
        print("Error :", e)      

# ==========================================================
# PASSENGER REPORT MENU
# ==========================================================

def passenger_report_menu():
    while True:
        print("1. All Passengers")
        print("2. Passenger by Flight")
        print("3. Passenger Age Distribution")
        print("4. Back")
        try:

            ch = int(input("Enter Choice : "))
            match ch:

                case 1:
                    all_passengers_report()

                case 2:
                    passenger_by_flight_report()

                case 3:
                    passenger_age_distribution()

                case 4:
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
        gender = {}
        for row in rows:
            if row[3] in gender:
                gender[row[3]] += 1
            else:
                gender[row[3]] = 1

        plt.figure(figsize=(6,6))

        plt.pie(
            gender.values(),
            labels=gender.keys(),
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Passenger Gender Distribution")
        plt.show()

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

        gender = {}

        for row in rows:
            if row[3] in gender:
                gender[row[3]] += 1
            else:
                gender[row[3]] = 1

        plt.figure(figsize=(6,5))

        plt.bar(gender.keys(), gender.values())

        plt.title(f"Passengers in Flight {flight_id}")
        plt.xlabel("Gender")
        plt.ylabel("Passengers")

        # Show only integer values on Y-axis
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        for i, value in enumerate(gender.values()):
            plt.text(i, value, str(value), ha="center")

        plt.grid(axis="y", linestyle="--")

        plt.show()

    except Exception as e:
        print("Error :", e)


# ==========================================================
# PASSENGER AGE DISTRIBUTION CHART
# ==========================================================
def passenger_age_distribution():

    heading("PASSENGER AGE DISTRIBUTION")

    try:

        cursor.execute("""
        SELECT age
        FROM passengers
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No Passenger Found.")
            return

        ages = []

        for row in rows:
            ages.append(row[0])

        plt.figure(figsize=(8,5))

        plt.hist(
            ages,
            bins=5,
            edgecolor="black"
        )

        plt.title("Passenger Age Distribution")
        plt.xlabel("Age")
        plt.ylabel("Number of Passengers")

        plt.grid(axis="y", linestyle="--")

        plt.show()

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
        status = []
        count = []

        cursor.execute("""
        SELECT status, COUNT(*)
        FROM bookings
        WHERE booking_date = ?
        GROUP BY status
        """, (booking_date,))

        chart_data = cursor.fetchall()

        for row in chart_data:
            status.append(row[0])
            count.append(row[1])

        plt.figure(figsize=(7,5))
        plt.bar(status, count, edgecolor="black")

        plt.title(f"Daily Bookings ({booking_date})")
        plt.xlabel("Booking Status")
        plt.ylabel("Number of Bookings")

        for i, value in enumerate(count):
            plt.text(i, value, str(value), ha="center")

        plt.grid(axis="y", linestyle="--")
        plt.show()
    except Exception as e:
        print("Error :", e)
# ==========================================================
# 7.3.2 MONTHLY BOOKING REPORT
# ==========================================================

def monthly_booking_report():

    heading("MONTHLY BOOKING REPORT")

    try:

        month = input("Enter Month (YYYY-MM) : ")

        dates = []
        total_bookings = []

        cursor.execute("""
        SELECT
            booking_date,
            COUNT(*)
        FROM bookings
        WHERE substr(booking_date,1,7)=?
        GROUP BY booking_date
        ORDER BY booking_date
        """, (month,))

        chart_data = cursor.fetchall()

        if not chart_data:
            print("No Booking Found.")
            return

        for row in chart_data:
            dates.append(row[0])
            total_bookings.append(row[1])

        plt.figure(figsize=(10,5))

        plt.bar(dates, total_bookings)

        plt.title(f"Monthly Booking Report ({month})")
        plt.xlabel("Booking Date")
        plt.ylabel("Number of Bookings")

        for i, value in enumerate(total_bookings):
            plt.text(i, value, str(value), ha="center")

        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--")
        plt.tight_layout()

        plt.show()

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

        # ---------------- CANCELLED BOOKING CHART ----------------



        dates = []
        cancelled = []

        cursor.execute("""
        SELECT
            booking_date,
            COUNT(*)
        FROM bookings
        WHERE status = 'Cancelled'
        GROUP BY booking_date
        ORDER BY booking_date
        """)

        chart_data = cursor.fetchall()

        if chart_data:

            for row in chart_data:
                dates.append(row[0])
                cancelled.append(row[1])

            plt.figure(figsize=(8,5))

            plt.bar(dates, cancelled, edgecolor="black")

            plt.title("Cancelled Bookings Report")
            plt.xlabel("Booking Date")
            plt.ylabel("Number of Cancelled Bookings")

            for i, value in enumerate(cancelled):
                plt.text(i, value, str(value), ha="center")

            plt.grid(axis="y", linestyle="--")

            plt.xticks(rotation=45)

            plt.tight_layout()
            plt.show()
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


        if row and row[2] is not None:
            plt.figure(figsize=(6,5))

            labels = ["Revenue"]
            values = [row[2]]

            plt.bar(labels, values)
            plt.title(f"Daily Revenue ({payment_date})")
            plt.xlabel("Revenue")
            plt.ylabel("Amount (₹)")

            for i, value in enumerate(values):
                plt.text(i, value, f"₹{value}", ha="center")

            plt.show()
        
        
    except Exception as e:
        print("Error :", e)


# ==========================================================
# 7.4.2 MONTHLY REVENUE REPORT
# ==========================================================

def monthly_revenue_report():

    heading("MONTHLY REVENUE REPORT")

    try:

        month = input("Enter Month (YYYY-MM) : ")

        dates = []
        revenue = []

        cursor.execute("""
        SELECT
            payment_date,
            SUM(amount)
        FROM payments
        WHERE substr(payment_date,1,7)=?
        AND payment_status='Success'
        GROUP BY payment_date
        ORDER BY payment_date
        """, (month,))

        chart_data = cursor.fetchall()

        if not chart_data:
            print("No Revenue Found.")
            return

        for row in chart_data:
            dates.append(row[0])
            revenue.append(row[1])

        plt.figure(figsize=(10,5))

        plt.bar(dates, revenue)

        plt.title(f"Monthly Revenue Report ({month})")
        plt.xlabel("Payment Date")
        plt.ylabel("Revenue (₹)")

        for i, value in enumerate(revenue):
            plt.text(i, value, f"₹{value}", ha="center")

        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--")
        plt.tight_layout()

        plt.show()

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
                # ---------------- YEARLY REVENUE CHART ----------------

        years = []
        revenue = []

        cursor.execute("""
        SELECT
            substr(payment_date,1,4),
            SUM(amount)
        FROM payments
        WHERE payment_status = 'Success'
        GROUP BY substr(payment_date,1,4)
        ORDER BY substr(payment_date,1,4)
        """)

        chart_data = cursor.fetchall()

        if chart_data:

            for row in chart_data:
                years.append(row[0])
                revenue.append(row[1])

            plt.figure(figsize=(7,5))

            plt.bar(years, revenue, edgecolor="black")

            plt.title("Yearly Revenue Report")
            plt.xlabel("Year")
            plt.ylabel("Revenue (₹)")

            for i, value in enumerate(revenue):
                plt.text(i, value, f"₹{value}", ha="center")

            plt.grid(axis="y", linestyle="--")
            plt.show()

    except Exception as e:
        print("Error :", e)             

if __name__ == "__main__":
    reports_menu()