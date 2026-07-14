from database import get_connection
conn = get_connection()
cursor = conn.cursor()
from database import get_connection
from rich.console import Console
from rich.table import Table
import smtplib
from email.message import EmailMessage

def send_ticket_email(receiver_email, ticket):

    sender_email = "shitoletrupti6@gmail.com"      # Your Gmail
    app_password = "gkggkjfeenrljdmm"   # Gmail App Password

    msg = EmailMessage()
    msg["Subject"] = "Airline Ticket Confirmation"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(f"""
Dear Passenger,

Thank you for choosing our Airline Reservation System.

Your booking has been confirmed.

Your Ticket Details:

{ticket}

Have a safe and pleasant journey!

Regards,
Airline Reservation System
""")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        print("\nTicket has been sent successfully!")
        return True

    except Exception as e:
        print("\nFailed to send email.")
        print("Error:", e)
        return False

console = Console()

def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()


def make_payment(method):

    heading("MAKE PAYMENT")

    try:
        booking = int(input("Enter Booking ID : "))

        # Check if payment already exists
        cursor.execute("""
            SELECT payment_id,
                   booking_id,
                   amount,
                   payment_method,
                   payment_status
            FROM payments
            WHERE booking_id = ?
        """, (booking,))
        conn.commit()

        payment = cursor.fetchone()

        if payment:
            heading("PAYMENT DETAILS")
            print("Payment ID     :", payment[0])
            print("Booking ID     :", payment[1])
            print("Amount         : ₹", payment[2])
            print("Payment Method :", payment[3])
            print("Payment Status :", payment[4])
            return

        # Get fare for the booking
        cursor.execute("""
            SELECT f.fare
            FROM bookings b
            JOIN flights f
                ON b.flight_id = f.flight_id
            WHERE b.booking_id = ?
        """, (booking,))

        fare = cursor.fetchone()

        if not fare:
            print("Invalid Booking ID.")
            return

        amount = fare[0]

        print(f"\nAmount to Pay : ₹{amount}")

        # Payment confirmation
        confirm = input("Are you sure you want to pay this amount? (Y/N): ").strip().upper()

        if confirm != "Y":
            print(" Payment Cancelled.")
            return

        status = "Paid"

        # Insert payment
        cursor.execute("""
            INSERT INTO payments
            (
                booking_id,
                amount,
                payment_method,
                payment_status
            )
            VALUES (?,?,?,?)
        """, (booking, amount, method, status))

        conn.commit()
        
        print("\nPayment Successful!")
        print("Booking ID     :", booking)
        print("Amount Paid    : ₹", amount)
        print("Payment Method :", method)
        print("Payment Status :", status)

        cursor.execute("""
        UPDATE bookings
        SET status = 'Confirmed'
        WHERE booking_id = ?
        """, (booking,))
        conn.commit()

        # Ask user how they want the ticket
        choice = input("\nDo you want to receive the ticket online? (Y/N): ").strip().upper()

        if choice == "Y":

            email = input("Enter your Email Address: ").strip()

            # Generate ticket (if your function returns ticket text)
            ticket = generate_ticket()

            # Send ticket to email
            send_ticket_email(email, ticket)

            print(f"\nTicket has been sent successfully to {email}")

        else:
            print("\nPrinting Ticket...\n")
            print_ticket()      # or generate_ticket(booking) if that function prints the ticket
    
    except Exception as e:
        print(" Error:", e)


# =====================================================
# 5.2 PAYMENT HISTORY
# =====================================================

def view_all_payments():
    cursor.execute("SELECT * FROM payments")
    rows = cursor.fetchall()
    if rows:
        heading("PAYMENT HISTORY")
        for row in rows:
            print("---------------------------")
            print("Payment ID :", row[0])
            print("Booking ID :", row[1])
            print("Amount     :", row[2])
            print("Method     :", row[3])
            print("Status     :", row[4])
    else:
        print("No Payment History Found.")
# =====================================================
def search_payment_id():
    heading("SEARCH PAYMENT")
    pid = int(input("Enter Payment ID : "))
    cursor.execute(
        "SELECT * FROM payments WHERE payment_id=?",
        (pid,)
    )
    row = cursor.fetchone()
    if row:
        print("\nPayment Found")
        print("---------------------------")
        print("Payment ID :", row[0])
        print("Booking ID :", row[1])
        print("Amount     :", row[2])
        print("Method     :", row[3])
        print("Status     :", row[4])
    else:
        print("Payment Not Found")
# =====================================================

def search_booking_id():
    heading("SEARCH BOOKING PAYMENT")
    booking = int(input("Enter Booking ID : "))
    cursor.execute(
        "SELECT * FROM payments WHERE booking_id=?",
        (booking,)
    )
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print("---------------------------")
            print("Payment ID :", row[0])
            print("Booking ID :", row[1])
            print("Amount     :", row[2])
            print("Method     :", row[3])
            print("Status     :", row[4])
    else:
        print("Booking ID Not Found")
# =====================================================
# 5.3 GENERATE TICKET
# =====================================================
def generate_ticket():
    heading("AIRLINE TICKET")

    booking = int(input("Enter Booking ID : "))

    cursor.execute("""
    SELECT
        b.booking_id,
        p.passenger_name,
        pay.amount,
        pay.payment_method,
        pay.payment_status
    FROM bookings b
    JOIN passengers p
        ON b.passenger_id = p.passenger_id
    JOIN payments pay
        ON b.booking_id = pay.booking_id
    WHERE b.booking_id = ?
    """, (booking,))

    row = cursor.fetchone()

    if row:

        ticket = f"""
==============================
       AIRLINE TICKET
==============================
Passenger Name : {row[1]}
Booking ID     : {row[0]}
Amount Paid    : ₹{row[2]}
Payment Method : {row[3]}
Payment Status : {row[4]}
==============================
"""

        print(ticket)

        return ticket      # Return the ticket string

    else:
        print("Booking Not Found")
        return None

# =====================================================


def print_ticket():
    heading("PRINT TICKET")
    booking = int(input("Enter Booking ID : "))
    cursor.execute("""
    SELECT
    p.passenger_name,
    b.booking_id,
    pay.amount,
    pay.payment_method,
    pay.payment_status
    FROM bookings b
    JOIN passengers p
    ON b.passenger_id=p.passenger_id
    JOIN payments pay
    ON b.booking_id=pay.booking_id
    WHERE b.booking_id=?
    """, (booking,))
    row = cursor.fetchone()
    if row:
        print("\nPrinting Ticket...\n")
        print("******** AIRLINE TICKET ********")
        print("Passenger :", row[0])
        print("Booking ID:", row[1])
        print("Amount    :", row[2])
        print("Method    :", row[3])
        print("Status    :", row[4])
        print("********************************")
    else:
        print("Booking Not Found")
