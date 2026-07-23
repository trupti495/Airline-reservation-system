from database import get_connection
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt
from colorama import init
from matplotlib.ticker import MaxNLocator


# ============================================================
# INITIALIZATION
# ============================================================

init(autoreset=True)

console = Console()


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = get_connection()
cursor = conn.cursor()


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
# INTEGER Y-AXIS
# ============================================================

def set_integer_y_axis():

    ax = plt.gca()

    ax.yaxis.set_major_locator(
        MaxNLocator(integer=True)
    )


# ============================================================
# REPORTS MENU
# ============================================================

def reports_menu():

    while True:

        heading("REPORTS MENU")

        print("1. Flight Report")
        print("2. Passenger Report")
        print("3. Booking Report")
        print("4. Revenue Report")
        print("5. Back")

        try:

            ch = int(
                input("\nEnter Choice : ")
            )

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

        except ValueError:

            print("Please Enter a Valid Number.")

        except Exception as e:

            print("Error :", e)


# ============================================================
# FLIGHT REPORT MENU
# ============================================================

def flight_report_menu():

    while True:

        heading("FLIGHT REPORT")

        print("1. Daily Flight Report")
        print("2. Monthly Flight Report")
        print("3. Yearly Flight Report")
        print("4. Back")

        try:

            ch = int(
                input("Enter Choice : ")
            )

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

        except ValueError:

            print("Please Enter a Valid Number.")

        except Exception as e:

            print("Error :", e)


# ============================================================
# DAILY FLIGHT REPORT
# ============================================================

def daily_flight_report():

    heading("DAILY FLIGHT REPORT")

    try:

        date = input(
            "Enter Date (YYYY-MM-DD) : "
        ).strip()

        cursor.execute(
            """
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
            ORDER BY departure_time
            """,
            (date,)
        )

        rows = cursor.fetchall()

        if not rows:

            print("No Flight Found.")

            return

        table = Table(
            title=f"Daily Flight Report ({date})",
            show_header=True,
            show_lines=True
        )

        table.add_column("Flight ID")
        table.add_column("Airline ID")
        table.add_column("Source ID")
        table.add_column("Destination ID")
        table.add_column("Departure Date")
        table.add_column("Time")
        table.add_column("Fare")
        table.add_column("Available Seats")

        flight_ids = []
        available_seats = []

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

            flight_ids.append(str(row[0]))
            available_seats.append(int(row[7]))

        console.print(table)

        plt.figure(figsize=(8, 5))

        plt.bar(
            flight_ids,
            available_seats,
            edgecolor="black"
        )

        plt.title(
            f"Daily Flight Report ({date})"
        )

        plt.xlabel("Flight ID")
        plt.ylabel("Available Seats")

        for i, value in enumerate(available_seats):

            plt.text(
                i,
                value,
                str(value),
                ha="center"
            )

        set_integer_y_axis()

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# MONTHLY FLIGHT REPORT
# ============================================================

def monthly_flight_report():

    heading("MONTHLY FLIGHT REPORT")

    try:

        month = input(
            "Enter Month (YYYY-MM) : "
        ).strip()

        cursor.execute(
            """
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
            WHERE substr(departure_date, 1, 7) = ?
            ORDER BY departure_date, departure_time
            """,
            (month,)
        )

        rows = cursor.fetchall()

        if not rows:

            print("No Flight Found.")

            return

        table = Table(
            title=f"Monthly Flight Report ({month})",
            show_header=True,
            show_lines=True
        )

        table.add_column("Flight ID")
        table.add_column("Airline ID")
        table.add_column("Source ID")
        table.add_column("Destination ID")
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Fare")
        table.add_column("Available Seats")

        flight_ids = []
        available_seats = []

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

            flight_ids.append(str(row[0]))
            available_seats.append(int(row[7]))

        console.print(table)

        plt.figure(figsize=(9, 5))

        plt.bar(
            flight_ids,
            available_seats,
            edgecolor="black"
        )

        plt.title(
            f"Monthly Flight Report ({month})"
        )

        plt.xlabel("Flight ID")
        plt.ylabel("Available Seats")

        for i, value in enumerate(available_seats):

            plt.text(
                i,
                value,
                str(value),
                ha="center"
            )

        set_integer_y_axis()

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# YEARLY FLIGHT REPORT
# ============================================================

def yearly_flight_report():

    heading("YEARLY FLIGHT REPORT")

    try:

        year = input(
            "Enter Year (YYYY) : "
        ).strip()

        cursor.execute(
            """
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
            WHERE substr(departure_date, 1, 4) = ?
            ORDER BY departure_date, departure_time
            """,
            (year,)
        )

        rows = cursor.fetchall()

        if not rows:

            print("No Flight Found.")

            return

        table = Table(
            title=f"Yearly Flight Report ({year})",
            show_header=True,
            show_lines=True
        )

        table.add_column("Flight ID")
        table.add_column("Airline ID")
        table.add_column("Source ID")
        table.add_column("Destination ID")
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Fare")
        table.add_column("Available Seats")

        flight_ids = []
        available_seats = []

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

            flight_ids.append(str(row[0]))
            available_seats.append(int(row[7]))

        console.print(table)

        plt.figure(figsize=(9, 5))

        plt.bar(
            flight_ids,
            available_seats,
            edgecolor="black"
        )

        plt.title(
            f"Yearly Flight Report ({year})"
        )

        plt.xlabel("Flight ID")
        plt.ylabel("Available Seats")

        for i, value in enumerate(available_seats):

            plt.text(
                i,
                value,
                str(value),
                ha="center"
            )

        set_integer_y_axis()

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# PASSENGER REPORT MENU
# ============================================================

def passenger_report_menu():

    while True:

        heading("PASSENGER REPORT")

        print("1. All Passengers")
        print("2. Passenger by Flight")
        print("3. Passenger Age Distribution")
        print("4. Back")

        try:

            ch = int(
                input("Enter Choice : ")
            )

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

        except ValueError:

            print("Please Enter a Valid Number.")

        except Exception as e:

            print("Error :", e)


# ============================================================
# ALL PASSENGERS REPORT
# ============================================================

def all_passengers_report():

    heading("ALL PASSENGERS REPORT")

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
            ORDER BY passenger_id
            """
        )

        rows = cursor.fetchall()

        if not rows:

            print("No Passenger Found.")

            return

        table = Table(
            title="All Passengers",
            show_header=True,
            show_lines=True
        )

        table.add_column("Passenger ID")
        table.add_column("Name")
        table.add_column("Age")
        table.add_column("Gender")
        table.add_column("Phone")

        gender_count = {}

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4])
            )

            gender = str(row[3])

            gender_count[gender] = (
                gender_count.get(gender, 0) + 1
            )

        console.print(table)

        plt.figure(figsize=(6, 6))

        plt.pie(
            gender_count.values(),
            labels=gender_count.keys(),
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title(
            "Passenger Gender Distribution"
        )

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# PASSENGER BY FLIGHT REPORT
# ============================================================

def passenger_by_flight_report():

    heading("PASSENGER BY FLIGHT REPORT")

    try:

        flight_id = int(
            input("Enter Flight ID : ")
        )

        cursor.execute(
            """
            SELECT
                p.passenger_id,
                p.passenger_name,
                p.age,
                p.gender,
                p.phone,
                s.seat_no,
                b.status
            FROM passengers p
            INNER JOIN bookings b
                ON p.passenger_id = b.passenger_id
            LEFT JOIN seats s
                ON b.seat_id = s.seat_id
            WHERE b.flight_id = ?
            ORDER BY p.passenger_id
            """,
            (flight_id,)
        )

        rows = cursor.fetchall()

        if not rows:

            print(
                "No Passenger Found For This Flight."
            )

            return

        table = Table(
            title=f"Passengers in Flight {flight_id}",
            show_header=True,
            show_lines=True
        )

        table.add_column("Passenger ID")
        table.add_column("Passenger Name")
        table.add_column("Age")
        table.add_column("Gender")
        table.add_column("Phone")
        table.add_column("Seat No.")
        table.add_column("Status")

        gender_count = {}

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5]),
                str(row[6])
            )

            gender = str(row[3])

            gender_count[gender] = (
                gender_count.get(gender, 0) + 1
            )

        console.print(table)

        plt.figure(figsize=(6, 5))

        plt.bar(
            gender_count.keys(),
            gender_count.values(),
            edgecolor="black"
        )

        plt.title(
            f"Passengers in Flight {flight_id}"
        )

        plt.xlabel("Gender")
        plt.ylabel("Passengers")

        set_integer_y_axis()

        for i, value in enumerate(gender_count.values()):

            plt.text(
                i,
                value,
                str(value),
                ha="center"
            )

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except ValueError:

        print(
            "Please Enter a Valid Flight ID."
        )

    except Exception as e:

        print("Error :", e)


# ============================================================
# PASSENGER AGE DISTRIBUTION
# ============================================================

def passenger_age_distribution():

    heading("PASSENGER AGE DISTRIBUTION")

    try:

        cursor.execute(
            """
            SELECT age
            FROM passengers
            WHERE age IS NOT NULL
            """
        )

        rows = cursor.fetchall()

        if not rows:

            print("No Passenger Found.")

            return

        ages = [
            int(row[0])
            for row in rows
        ]

        plt.figure(figsize=(8, 5))

        plt.hist(
            ages,
            bins=5,
            edgecolor="black"
        )

        plt.title(
            "Passenger Age Distribution"
        )

        plt.xlabel("Age")
        plt.ylabel("Number of Passengers")

        set_integer_y_axis()

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# BOOKING REPORT MENU
# ============================================================

def booking_report_menu():

    while True:

        heading("BOOKING REPORT")

        print("1. Daily Bookings")
        print("2. Monthly Bookings")
        print("3. Cancelled Bookings")
        print("4. Back")

        try:

            ch = int(
                input("Enter Choice : ")
            )

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

        except ValueError:

            print("Please Enter a Valid Number.")

        except Exception as e:

            print("Error :", e)


# ============================================================
# DAILY BOOKING REPORT
# ============================================================

def daily_booking_report():

    heading("DAILY BOOKING REPORT")

    try:

        booking_date = input(
            "Enter Date (YYYY-MM-DD) : "
        ).strip()

        cursor.execute(
            """
            SELECT
                b.booking_id,
                b.passenger_id,
                b.flight_id,
                b.booking_date,
                s.seat_no,
                b.status
            FROM bookings b
            LEFT JOIN seats s
                ON b.seat_id = s.seat_id
            WHERE substr(b.booking_date, 1, 10) = ?
            ORDER BY b.booking_id
            """,
            (booking_date,)
        )

        rows = cursor.fetchall()

        if not rows:

            print("No Booking Found.")

            return

        table = Table(
            title=f"Daily Booking Report ({booking_date})",
            show_header=True,
            show_lines=True
        )

        table.add_column("Booking ID")
        table.add_column("Passenger ID")
        table.add_column("Flight ID")
        table.add_column("Booking Date")
        table.add_column("Seat No.")
        table.add_column("Status")

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5])
            )

        console.print(table)

        cursor.execute(
            """
            SELECT
                status,
                COUNT(*)
            FROM bookings
            WHERE substr(booking_date, 1, 10) = ?
            GROUP BY status
            ORDER BY status
            """,
            (booking_date,)
        )

        chart_data = cursor.fetchall()

        statuses = []
        counts = []

        for row in chart_data:

            statuses.append(str(row[0]))
            counts.append(int(row[1]))

        if not statuses:

            return

        plt.figure(figsize=(7, 5))

        plt.bar(
            statuses,
            counts,
            edgecolor="black"
        )

        plt.title(
            f"Daily Bookings ({booking_date})"
        )

        plt.xlabel("Booking Status")
        plt.ylabel("Number of Bookings")

        for i, value in enumerate(counts):

            plt.text(
                i,
                value,
                str(value),
                ha="center"
            )

        set_integer_y_axis()

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# MONTHLY BOOKING REPORT
# ============================================================

def monthly_booking_report():

    heading("MONTHLY BOOKING REPORT")

    try:

        month = input(
            "Enter Month (YYYY-MM) : "
        ).strip()

        cursor.execute(
            """
            SELECT
                substr(booking_date, 1, 10),
                COUNT(*)
            FROM bookings
            WHERE substr(booking_date, 1, 7) = ?
            GROUP BY substr(booking_date, 1, 10)
            ORDER BY substr(booking_date, 1, 10)
            """,
            (month,)
        )

        chart_data = cursor.fetchall()

        if not chart_data:

            print("No Booking Found.")

            return

        dates = []
        total_bookings = []

        for row in chart_data:

            dates.append(row[0])
            total_bookings.append(int(row[1]))

        table = Table(
            title=f"Monthly Booking Report ({month})",
            show_header=True,
            show_lines=True
        )

        table.add_column("Booking Date")
        table.add_column("Total Bookings")

        for i in range(len(dates)):

            table.add_row(
                str(dates[i]),
                str(total_bookings[i])
            )

        console.print(table)

        plt.figure(figsize=(10, 5))

        plt.bar(
            dates,
            total_bookings,
            edgecolor="black"
        )

        plt.title(
            f"Monthly Booking Report ({month})"
        )

        plt.xlabel("Booking Date")
        plt.ylabel("Number of Bookings")

        for i, value in enumerate(total_bookings):

            plt.text(
                i,
                value,
                str(value),
                ha="center"
            )

        set_integer_y_axis()

        plt.xticks(
            rotation=45
        )

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# CANCELLED BOOKING REPORT
# ============================================================

def cancelled_booking_report():

    heading("CANCELLED BOOKING REPORT")

    try:

        cursor.execute(
            """
            SELECT
                b.booking_id,
                b.passenger_id,
                b.flight_id,
                b.booking_date,
                s.seat_no,
                b.status
            FROM bookings b
            LEFT JOIN seats s
                ON b.seat_id = s.seat_id
            WHERE LOWER(TRIM(b.status)) = 'cancelled'
            ORDER BY b.booking_date
            """
        )

        rows = cursor.fetchall()

        if not rows:

            print(
                "No Cancelled Bookings Found."
            )

            return

        table = Table(
            title="Cancelled Booking Report",
            show_header=True,
            show_lines=True
        )

        table.add_column("Booking ID")
        table.add_column("Passenger ID")
        table.add_column("Flight ID")
        table.add_column("Booking Date")
        table.add_column("Seat No.")
        table.add_column("Status")

        for row in rows:

            table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5])
            )

        console.print(table)

        cursor.execute(
            """
            SELECT
                substr(booking_date, 1, 10),
                COUNT(*)
            FROM bookings
            WHERE LOWER(TRIM(status)) = 'cancelled'
            GROUP BY substr(booking_date, 1, 10)
            ORDER BY substr(booking_date, 1, 10)
            """
        )

        chart_data = cursor.fetchall()

        dates = []
        cancelled = []

        for row in chart_data:

            dates.append(row[0])
            cancelled.append(int(row[1]))

        if dates:

            plt.figure(figsize=(8, 5))

            plt.bar(
                dates,
                cancelled,
                edgecolor="black"
            )

            plt.title(
                "Cancelled Bookings Report"
            )

            plt.xlabel("Booking Date")

            plt.ylabel(
                "Number of Cancelled Bookings"
            )

            for i, value in enumerate(cancelled):

                plt.text(
                    i,
                    value,
                    str(value),
                    ha="center"
                )

            set_integer_y_axis()

            plt.xticks(
                rotation=45
            )

            plt.grid(
                axis="y",
                linestyle="--"
            )

            plt.tight_layout()

            plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# REVENUE REPORT MENU
# ============================================================

def revenue_report_menu():

    while True:

        heading("REVENUE REPORT")

        print("1. Daily Revenue")
        print("2. Monthly Revenue")
        print("3. Yearly Revenue")
        print("4. Back")

        try:

            ch = int(
                input("Enter Choice : ")
            )

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

        except ValueError:

            print("Please Enter a Valid Number.")

        except Exception as e:

            print("Error :", e)


# ============================================================
# DAILY REVENUE REPORT
# ============================================================

def daily_revenue_report():

    heading("DAILY REVENUE REPORT")

    try:

        date = input(
            "Enter Date (YYYY-MM-DD) : "
        ).strip()

        cursor.execute(
            """
            SELECT
                COUNT(payment_id),
                COALESCE(SUM(total_amount), 0)
            FROM payments
            WHERE substr(payment_date, 1, 10) = ?
            AND LOWER(TRIM(payment_status)) = 'successful'
            """,
            (date,)
        )

        row = cursor.fetchone()

        total_payments = int(row[0])
        total_revenue = float(row[1])

        table = Table(
            title=f"Daily Revenue Report ({date})",
            show_header=True,
            show_lines=True
        )

        table.add_column("Date")
        table.add_column("Total Payments")
        table.add_column("Total Revenue")

        table.add_row(
            date,
            str(total_payments),
            f"₹ {total_revenue:.2f}"
        )

        console.print(table)

        if total_revenue > 0:

            plt.figure(figsize=(6, 5))

            plt.bar(
                ["Revenue"],
                [total_revenue],
                edgecolor="black"
            )

            plt.title(
                f"Daily Revenue ({date})"
            )

            plt.ylabel("Revenue (₹)")

            plt.text(
                0,
                total_revenue,
                f"₹ {total_revenue:.2f}",
                ha="center",
                va="bottom"
            )

            plt.tight_layout()

            plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# MONTHLY REVENUE REPORT
# ============================================================

def monthly_revenue_report():

    heading("MONTHLY REVENUE REPORT")

    try:

        month = input(
            "Enter Month (YYYY-MM) : "
        ).strip()

        cursor.execute(
            """
            SELECT
                substr(payment_date, 1, 10),
                COUNT(payment_id),
                COALESCE(SUM(total_amount), 0)
            FROM payments
            WHERE substr(payment_date, 1, 7) = ?
            AND LOWER(TRIM(payment_status)) = 'successful'
            GROUP BY substr(payment_date, 1, 10)
            ORDER BY substr(payment_date, 1, 10)
            """,
            (month,)
        )

        rows = cursor.fetchall()

        if not rows:

            print("No Revenue Found.")

            return

        table = Table(
            title=f"Monthly Revenue Report ({month})",
            show_header=True,
            show_lines=True
        )

        table.add_column("Payment Date")
        table.add_column("Total Payments")
        table.add_column("Revenue")

        dates = []
        revenues = []

        for row in rows:

            date = row[0]
            payments = int(row[1])
            revenue = float(row[2])

            table.add_row(
                str(date),
                str(payments),
                f"₹ {revenue:.2f}"
            )

            dates.append(date)
            revenues.append(revenue)

        console.print(table)

        plt.figure(figsize=(10, 5))

        plt.bar(
            dates,
            revenues,
            edgecolor="black"
        )

        plt.title(
            f"Monthly Revenue Report ({month})"
        )

        plt.xlabel("Payment Date")
        plt.ylabel("Revenue (₹)")

        for i, value in enumerate(revenues):

            plt.text(
                i,
                value,
                f"₹{value:.2f}",
                ha="center",
                va="bottom"
            )

        plt.xticks(
            rotation=45
        )

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# YEARLY REVENUE REPORT
# ============================================================

def yearly_revenue_report():

    heading("YEARLY REVENUE REPORT")

    try:

        year = input(
            "Enter Year (YYYY) : "
        ).strip()

        # ----------------------------------------------------
        # YEARLY TOTAL
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                COUNT(payment_id),
                COALESCE(SUM(total_amount), 0)
            FROM payments
            WHERE substr(payment_date, 1, 4) = ?
            AND LOWER(TRIM(payment_status)) = 'successful'
            """,
            (year,)
        )

        row = cursor.fetchone()

        total_payments = int(row[0])
        total_revenue = float(row[1])

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        table = Table(
            title=f"Yearly Revenue Report ({year})",
            show_header=True,
            show_lines=True
        )

        table.add_column("Year")
        table.add_column("Total Payments")
        table.add_column("Total Revenue")

        table.add_row(
            year,
            str(total_payments),
            f"₹ {total_revenue:.2f}"
        )

        console.print(table)

        # ----------------------------------------------------
        # YEARLY CHART
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                substr(payment_date, 1, 4),
                COALESCE(SUM(total_amount), 0)
            FROM payments
            WHERE LOWER(TRIM(payment_status)) = 'successful'
            GROUP BY substr(payment_date, 1, 4)
            ORDER BY substr(payment_date, 1, 4)
            """
        )

        chart_data = cursor.fetchall()

        if not chart_data:

            return

        years = []
        revenues = []

        for row in chart_data:

            years.append(str(row[0]))
            revenues.append(float(row[1]))

        plt.figure(figsize=(8, 5))

        plt.bar(
            years,
            revenues,
            edgecolor="black"
        )

        plt.title(
            "Yearly Revenue Report"
        )

        plt.xlabel("Year")
        plt.ylabel("Revenue (₹)")

        for i, value in enumerate(revenues):

            plt.text(
                i,
                value,
                f"₹{value:.2f}",
                ha="center",
                va="bottom"
            )

        plt.grid(
            axis="y",
            linestyle="--"
        )

        plt.tight_layout()

        plt.show()

    except Exception as e:

        print("Error :", e)


# ============================================================
# RUN REPORT MODULE DIRECTLY
# ============================================================

if __name__ == "__main__":

    try:

        reports_menu()

    finally:

        conn.close()