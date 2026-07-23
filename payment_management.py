from database import get_connection
from rich.console import Console
from rich.table import Table
from datetime import datetime
import random
import string
import smtplib
import os
from email.message import EmailMessage


# ============================================================
# DATABASE
# ============================================================

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "PRAGMA foreign_keys = ON"
)


# ============================================================
# RICH CONSOLE
# ============================================================

console = Console()


# ============================================================
# HEADING
# ============================================================

def heading(title):

    console.print()

    console.rule(
        f"[bold yellow]{title}[/bold yellow]",
        style="blue"
    )

    console.print()


# ============================================================
# GENERATE PNR
# ============================================================

def generate_pnr():

    while True:

        pnr = (
            ''.join(
                random.choices(
                    string.ascii_uppercase,
                    k=3
                )
            )
            +
            ''.join(
                random.choices(
                    string.digits,
                    k=5
                )
            )
        )

        cursor.execute(
            """
            SELECT ticket_id
            FROM tickets
            WHERE pnr_no = ?
            """,
            (pnr,)
        )

        if not cursor.fetchone():

            return pnr


# ============================================================
# CREATE TICKET
# ============================================================

def create_ticket(booking_id):

    cursor.execute(
        """
        SELECT pnr_no
        FROM tickets
        WHERE booking_id = ?
        """,
        (booking_id,)
    )

    ticket = cursor.fetchone()

    if ticket:

        return ticket[0]


    pnr = generate_pnr()

    issue_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute(
        """
        INSERT INTO tickets
        (
            booking_id,
            pnr_no,
            issue_date,
            ticket_status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            booking_id,
            pnr,
            issue_date,
            "Active"
        )
    )

    return pnr


# ============================================================
# SEND TICKET EMAIL
# ============================================================

def send_ticket_email(receiver_email, ticket_text):

    sender_email = "shitoletrupti6@gmail.com"
    app_password = "hyjspiqilotmbanw"

    message = EmailMessage()

    message["Subject"] = "Airline Ticket Confirmation"

    message["From"] = sender_email

    message["To"] = receiver_email

    message.set_content(
        f"""
Dear Passenger,

Your booking has been confirmed successfully.

Your Ticket Details:

{ticket_text}

Have a safe and pleasant journey!

Regards,
Airline Reservation System
"""
    )

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as smtp:

            smtp.starttls()

            smtp.login(
                sender_email,
                app_password
            )

            smtp.send_message(
                message
            )

        print(
            "\nTicket sent successfully."
        )

        return True

    except Exception as e:

        print(
            "\nFailed to send email."
        )

        print(
            f"Error: {e}"
        )

        return False

# ============================================================
# MAKE PAYMENT
# ============================================================

def make_payment(method):

    heading("MAKE PAYMENT")


    try:

        # ----------------------------------------------------
        # BOOKING ID
        # ----------------------------------------------------

        booking_id = int(
            console.input(
                "Enter Booking ID : "
            )
        )


        # ----------------------------------------------------
        # CHECK BOOKING
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                passenger_id,
                flight_id,
                status
            FROM bookings
            WHERE booking_id = ?
            """,
            (booking_id,)
        )

        booking = cursor.fetchone()


        if not booking:

            print(
                "Booking Not Found."
            )

            return


        if booking[2] == "Cancelled":

            print(
                "This Booking is Cancelled."
            )

            return


        # ----------------------------------------------------
        # CHECK EXISTING PAYMENT
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                payment_id,
                total_amount,
                payment_method,
                payment_status
            FROM payments
            WHERE booking_id = ?
            """,
            (booking_id,)
        )

        payment = cursor.fetchone()


        if payment:

            table = Table(
                title="PAYMENT ALREADY EXISTS",
                show_lines=True
            )

            table.add_column(
                "Field"
            )

            table.add_column(
                "Value"
            )

            table.add_row(
                "Payment ID",
                str(payment[0])
            )

            table.add_row(
                "Total Amount",
                f"₹{float(payment[1]):.2f}"
            )

            table.add_row(
                "Payment Method",
                str(payment[2])
            )

            table.add_row(
                "Payment Status",
                str(payment[3])
            )

            console.print(table)

            return


        # ----------------------------------------------------
        # GET FLIGHT FARE
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                flight_number,
                fare
            FROM flights
            WHERE flight_id = ?
            """,
            (booking[1],)
        )

        flight = cursor.fetchone()


        if not flight:

            print(
                "Flight Not Found."
            )

            return


        # ----------------------------------------------------
        # CALCULATE AMOUNT
        # ----------------------------------------------------

        base_amount = float(
            flight[1]
        )

        gst_percentage = 5.0

        gst_amount = round(
            base_amount * 5 / 100,
            2
        )

        total_amount = round(
            base_amount + gst_amount,
            2
        )


        # ----------------------------------------------------
        # PAYMENT DETAILS
        # ----------------------------------------------------

        table = Table(
            title="PAYMENT DETAILS",
            show_lines=True
        )

        table.add_column(
            "Field"
        )

        table.add_column(
            "Value"
        )

        table.add_row(
            "Flight Number",
            str(flight[0])
        )

        table.add_row(
            "Base Fare",
            f"₹{base_amount:.2f}"
        )

        table.add_row(
            "GST",
            f"₹{gst_amount:.2f}"
        )

        table.add_row(
            "Total Amount",
            f"₹{total_amount:.2f}"
        )

        table.add_row(
            "Payment Method",
            method
        )

        console.print(table)


        # ----------------------------------------------------
        # CONFIRM PAYMENT
        # ----------------------------------------------------

        confirm = console.input(
            f"Pay ₹{total_amount:.2f}? (Y/N): "
        ).strip().upper()


        if confirm != "Y":

            print(
                "Payment Cancelled."
            )

            return


        # ----------------------------------------------------
        # INSERT PAYMENT
        # ----------------------------------------------------

        payment_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        cursor.execute(
            """
            INSERT INTO payments
            (
                booking_id,
                base_amount,
                gst_percentage,
                gst_amount,
                total_amount,
                payment_method,
                payment_status,
                payment_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                booking_id,
                base_amount,
                gst_percentage,
                gst_amount,
                total_amount,
                method,
                "Successful",
                payment_date
            )
        )


        # ----------------------------------------------------
        # CONFIRM BOOKING
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE bookings
            SET status = 'Confirmed'
            WHERE booking_id = ?
            """,
            (booking_id,)
        )


        # ----------------------------------------------------
        # CREATE TICKET
        # ----------------------------------------------------

        pnr = create_ticket(
            booking_id
        )


        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        conn.commit()


        # ----------------------------------------------------
        # PAYMENT SUCCESS
        # ----------------------------------------------------

        console.print(
            "\n[green]Payment Successful.[/green]"
        )

        console.print(
            f"PNR Number : {pnr}"
        )


        # ----------------------------------------------------
        # EMAIL OR PRINT
        # ----------------------------------------------------

        choice = console.input(
            "Send Ticket by Email? (Y/N): "
        ).strip().upper()


        if choice == "Y":

            email = console.input(
                "Enter Email Address : "
            ).strip()


            if email:

                ticket = get_ticket_text(
                    booking_id
                )


                if ticket:

                    send_ticket_email(
                        email,
                        ticket
                    )

            else:

                print(
                    "Invalid Email Address."
                )


        else:

            print_ticket(
                booking_id
            )


    except ValueError:

        print(
            "Please Enter a Valid Booking ID."
        )


    except Exception as e:

        conn.rollback()

        print(
            f"Payment Error: {e}"
        )


# ============================================================
# PAYMENT HISTORY
# ============================================================

def view_all_payments():

    heading("PAYMENT HISTORY")


    cursor.execute(
        """
        SELECT
            payment_id,
            booking_id,
            total_amount,
            payment_method,
            payment_status,
            payment_date
        FROM payments
        ORDER BY payment_id DESC
        """
    )


    rows = cursor.fetchall()


    if not rows:

        print(
            "No Payment History Found."
        )

        return


    table = Table(
        title="PAYMENT HISTORY",
        show_lines=True
    )


    table.add_column(
        "Payment ID"
    )

    table.add_column(
        "Booking ID"
    )

    table.add_column(
        "Total Amount"
    )

    table.add_column(
        "Method"
    )

    table.add_column(
        "Status"
    )

    table.add_column(
        "Date"
    )


    for row in rows:

        table.add_row(
            str(row[0]),
            str(row[1]),
            f"₹{float(row[2]):.2f}",
            str(row[3]),
            str(row[4]),
            str(row[5])
        )


    console.print(table)


# ============================================================
# SEARCH PAYMENT BY PAYMENT ID
# ============================================================

def search_payment_id():

    heading("SEARCH PAYMENT")


    try:

        payment_id = int(
            console.input(
                "Enter Payment ID : "
            )
        )


        cursor.execute(
            """
            SELECT
                payment_id,
                booking_id,
                base_amount,
                gst_amount,
                total_amount,
                payment_method,
                payment_status,
                payment_date
            FROM payments
            WHERE payment_id = ?
            """,
            (payment_id,)
        )


        row = cursor.fetchone()


        if not row:

            print(
                "Payment Not Found."
            )

            return


        show_payment_details(
            row
        )


    except ValueError:

        print(
            "Invalid Payment ID."
        )


# ============================================================
# SEARCH PAYMENT BY BOOKING ID
# ============================================================

def search_booking_id():

    heading("SEARCH BOOKING PAYMENT")


    try:

        booking_id = int(
            console.input(
                "Enter Booking ID : "
            )
        )


        cursor.execute(
            """
            SELECT
                payment_id,
                booking_id,
                base_amount,
                gst_amount,
                total_amount,
                payment_method,
                payment_status,
                payment_date
            FROM payments
            WHERE booking_id = ?
            """,
            (booking_id,)
        )


        row = cursor.fetchone()


        if not row:

            print(
                "Payment Not Found."
            )

            return


        show_payment_details(
            row
        )


    except ValueError:

        print(
            "Invalid Booking ID."
        )


# ============================================================
# SHOW PAYMENT DETAILS
# ============================================================

def show_payment_details(row):

    table = Table(
        title="PAYMENT DETAILS",
        show_lines=True
    )


    table.add_column(
        "Field"
    )

    table.add_column(
        "Value"
    )


    table.add_row(
        "Payment ID",
        str(row[0])
    )

    table.add_row(
        "Booking ID",
        str(row[1])
    )

    table.add_row(
        "Base Amount",
        f"₹{float(row[2]):.2f}"
    )

    table.add_row(
        "GST Amount",
        f"₹{float(row[3]):.2f}"
    )

    table.add_row(
        "Total Amount",
        f"₹{float(row[4]):.2f}"
    )

    table.add_row(
        "Payment Method",
        str(row[5])
    )

    table.add_row(
        "Payment Status",
        str(row[6])
    )

    table.add_row(
        "Payment Date",
        str(row[7])
    )


    console.print(table)


def get_ticket_text(booking_id):

    cursor.execute(
        """
        SELECT
            t.pnr_no,
            p.passenger_name,
            f.flight_number,
            sa.city,
            da.city,
            f.departure_date,
            f.departure_time,
            s.seat_no,
            pay.total_amount,
            pay.payment_status
        FROM bookings b

        JOIN passengers p
            ON b.passenger_id = p.passenger_id

        JOIN flights f
            ON b.flight_id = f.flight_id

        JOIN airports sa
            ON f.source_airport_id = sa.airport_id

        JOIN airports da
            ON f.destination_airport_id = da.airport_id

        JOIN seats s
            ON b.seat_id = s.seat_id

        JOIN payments pay
            ON b.booking_id = pay.booking_id

        JOIN tickets t
            ON b.booking_id = t.booking_id

        WHERE b.booking_id = ?
        """,
        (booking_id,)
    )

    row = cursor.fetchone()

    if not row:
        return None

    ticket = f"""
==================================================
                 AIRLINE TICKET
==================================================

PNR Number      : {row[0]}
Passenger Name  : {row[1]}
Flight Number   : {row[2]}

--------------------------------------------------
                 JOURNEY DETAILS
--------------------------------------------------

From            : {row[3]}
To              : {row[4]}
Departure Date  : {row[5]}
Departure Time  : {row[6]}
Seat Number     : {row[7]}

--------------------------------------------------
                 PAYMENT DETAILS
--------------------------------------------------

Total Amount    : ₹{float(row[8]):.2f}
Payment Status  : {row[9]}

==================================================
           HAVE A SAFE JOURNEY!
==================================================
"""

    return ticket

def generate_ticket():

    heading("AIRLINE TICKET")


    try:

        booking_id = int(
            console.input(
                "Enter Booking ID : "
            )
        )


        print_ticket(
            booking_id
        )


    except ValueError:

        print(
            "Invalid Booking ID."
        )


# ============================================================
# PRINT TICKET
# ============================================================

def print_ticket(booking_id=None):

    if booking_id is None:

        try:

            booking_id = int(
                console.input(
                    "Enter Booking ID : "
                )
            )

        except ValueError:

            print(
                "Invalid Booking ID."
            )

            return


    cursor.execute(
        """
        SELECT
            t.pnr_no,
            p.passenger_name,
            f.flight_number,
            sa.city,
            da.city,
            f.departure_date,
            f.departure_time,
            s.seat_no,
            pay.total_amount,
            pay.payment_status
        FROM bookings b

        JOIN passengers p
            ON b.passenger_id = p.passenger_id

        JOIN flights f
            ON b.flight_id = f.flight_id

        JOIN airports sa
            ON f.source_airport_id = sa.airport_id

        JOIN airports da
            ON f.destination_airport_id = da.airport_id

        JOIN seats s
            ON b.seat_id = s.seat_id

        JOIN payments pay
            ON b.booking_id = pay.booking_id

        JOIN tickets t
            ON b.booking_id = t.booking_id

        WHERE b.booking_id = ?
        """,
        (booking_id,)
    )


    row = cursor.fetchone()


    if not row:

        print(
            "Ticket Not Found."
        )

        return


    table = Table(
        title="✈ AIRLINE TICKET ✈",
        show_lines=True,
        border_style="blue"
    )


    table.add_column(
        "Information",
        style="cyan"
    )

    table.add_column(
        "Details"
    )


    table.add_row(
        "PNR Number",
        str(row[0])
    )

    table.add_row(
        "Passenger Name",
        str(row[1])
    )

    table.add_row(
        "Flight Number",
        str(row[2])
    )

    table.add_row(
        "From",
        str(row[3])
    )

    table.add_row(
        "To",
        str(row[4])
    )

    table.add_row(
        "Departure Date",
        str(row[5])
    )

    table.add_row(
        "Departure Time",
        str(row[6])
    )

    table.add_row(
        "Seat Number",
        str(row[7])
    )

    table.add_row(
        "Total Amount",
        f"₹{float(row[8]):.2f}"
    )

    table.add_row(
        "Payment Status",
        str(row[9])
    )


    console.print(
        table
    )


# ============================================================
# REFUND PAYMENT
# ============================================================

def refund_payment():

    heading("REFUND PAYMENT")


    try:

        booking_id = int(
            console.input(
                "Enter Booking ID : "
            )
        )


        cursor.execute(
            """
            SELECT
                payment_id,
                total_amount,
                payment_status,
                refund_status
            FROM payments
            WHERE booking_id = ?
            """,
            (booking_id,)
        )


        payment = cursor.fetchone()


        if not payment:

            print(
                "Payment Not Found."
            )

            return


        if payment[2] != "Successful":

            print(
                "Payment is not successful."
            )

            return


        if payment[3] == "Successful":

            print(
                "Refund Already Processed."
            )

            return


        total_amount = float(
            payment[1]
        )


        print(
            f"Total Paid Amount : ₹{total_amount:.2f}"
        )


        refund_amount = float(
            console.input(
                "Enter Refund Amount : "
            )
        )


        if (
            refund_amount <= 0
            or refund_amount > total_amount
        ):

            print(
                "Invalid Refund Amount."
            )

            return


        confirm = console.input(
            "Confirm Refund? (Y/N): "
        ).strip().upper()


        if confirm != "Y":

            print(
                "Refund Cancelled."
            )

            return


        refund_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # ----------------------------------------------------
        # UPDATE PAYMENT
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE payments
            SET
                refund_amount = ?,
                refund_date = ?,
                refund_status = 'Successful'
            WHERE booking_id = ?
            """,
            (
                refund_amount,
                refund_date,
                booking_id
            )
        )


        # ----------------------------------------------------
        # GET BOOKING
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                flight_id,
                seat_id
            FROM bookings
            WHERE booking_id = ?
            """,
            (booking_id,)
        )


        booking = cursor.fetchone()


        if not booking:

            print(
                "Booking Not Found."
            )

            conn.rollback()

            return


        # ----------------------------------------------------
        # RELEASE SEAT
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE seats
            SET seat_status = 'Available'
            WHERE seat_id = ?
            """,
            (booking[1],)
        )


        # ----------------------------------------------------
        # UPDATE FLIGHT SEATS
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE flights
            SET available_seats =
                CASE
                    WHEN available_seats < total_seats
                    THEN available_seats + 1
                    ELSE available_seats
                END
            WHERE flight_id = ?
            """,
            (booking[0],)
        )


        # ----------------------------------------------------
        # CANCEL BOOKING
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE bookings
            SET
                status = 'Cancelled',
                cancellation_reason = 'Payment refunded'
            WHERE booking_id = ?
            """,
            (booking_id,)
        )


        # ----------------------------------------------------
        # CANCEL TICKET
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE tickets
            SET ticket_status = 'Cancelled'
            WHERE booking_id = ?
            """,
            (booking_id,)
        )


        conn.commit()


        console.print(
            "\n[green]Refund Successful.[/green]"
        )


        table = Table(
            title="REFUND DETAILS",
            show_lines=True
        )


        table.add_column(
            "Field"
        )

        table.add_column(
            "Value"
        )


        table.add_row(
            "Booking ID",
            str(booking_id)
        )

        table.add_row(
            "Refund Amount",
            f"₹{refund_amount:.2f}"
        )

        table.add_row(
            "Refund Status",
            "Successful"
        )

        table.add_row(
            "Booking Status",
            "Cancelled"
        )


        console.print(table)


    except ValueError:

        print(
            "Enter Valid Numeric Values."
        )


    except Exception as e:

        conn.rollback()

        print(
            f"Refund Error: {e}"
        )


# ============================================================
# PAYMENT MANAGEMENT MENU
# ============================================================

def payment_management_menu():

    while True:

        heading("PAYMENT MANAGEMENT")


        print("1. Make Payment")
        print("2. Payment History")
        print("3. Search Payment by Payment ID")
        print("4. Search Payment by Booking ID")
        print("5. Generate / View Ticket")
        print("6. Refund Payment")
        print("7. Exit")


        choice = console.input(
            "\nEnter Choice : "
        ).strip()


        # ----------------------------------------------------
        # MAKE PAYMENT
        # ----------------------------------------------------

        if choice == "1":

            heading("SELECT PAYMENT METHOD")

            print("1. UPI")
            print("2. Card")
            print("3. Net Banking")


            method = console.input(
                "Enter Payment Method : "
            ).strip()


            if method == "1":

                make_payment(
                    "UPI"
                )

            elif method == "2":

                make_payment(
                    "Card"
                )

            elif method == "3":

                make_payment(
                    "Net Banking"
                )

            else:

                print(
                    "Invalid Payment Method."
                )


        # ----------------------------------------------------
        # PAYMENT HISTORY
        # ----------------------------------------------------

        elif choice == "2":

            view_all_payments()


        # ----------------------------------------------------
        # SEARCH PAYMENT
        # ----------------------------------------------------

        elif choice == "3":

            search_payment_id()


        # ----------------------------------------------------
        # SEARCH BOOKING PAYMENT
        # ----------------------------------------------------

        elif choice == "4":

            search_booking_id()


        # ----------------------------------------------------
        # VIEW TICKET
        # ----------------------------------------------------

        elif choice == "5":

            generate_ticket()


        # ----------------------------------------------------
        # REFUND
        # ----------------------------------------------------

        elif choice == "6":

            refund_payment()


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "7":

            break


        else:

            print(
                "Invalid Choice."
            )


# ============================================================
# RUN MODULE
# ============================================================

if __name__ == "__main__":

    try:

        payment_management_menu()

    finally:

        conn.close()