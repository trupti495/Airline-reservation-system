from database import get_connection
conn = get_connection()
cursor = conn.cursor()
from database import get_connection
from rich.console import Console
from rich.table import Table

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
            WHERE booking_id=?
        """, (booking,))

        row = cursor.fetchone()

        if row:
            heading("PAYMENT DETAILS")
            print("Payment ID     :", row[0])
            print("Booking ID     :", row[1])
            print("Amount         :", row[2])
            print("Payment Method :", row[3])
            print("Payment Status :", row[4])
            return

        # If payment does not exist, create a new one
        amount = float(input("Enter Amount : "))

        status = "Paid"

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

    except ValueError:
        print("Invalid Input!")

    except Exception as e:
        print("Error:", e)
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
    WHERE b.booking_id=?
    """, (booking,))
    row = cursor.fetchone()
    if row:

        heading("AIRLINE TICKET")
        print("Passenger Name :", row[1])
        print("Booking ID     :", row[0])
        print("Amount Paid    :", row[2])
        print("Payment Method :", row[3])
        print("Payment Status :", row[4])
        

    else:
        print("Booking Not Found")


# =====================================================

def generate_receipt():
    heading("PAYMENT RECEIPT")
    pid = int(input("Enter Payment ID : "))

    cursor.execute("""
    SELECT
    pay.payment_id,
    p.passenger_name,
    pay.booking_id,
    pay.amount,
    pay.payment_method,
    pay.payment_status
    FROM payments pay
    JOIN bookings b
    ON pay.booking_id=b.booking_id
    JOIN passengers p
    ON b.passenger_id=p.passenger_id
    WHERE pay.payment_id=?
    """, (pid,))
    row = cursor.fetchone()
    if row:
        print("\n========== PAYMENT RECEIPT ==========")
        print("Receipt No     :", row[0])
        print("Passenger Name :", row[1])
        print("Booking ID     :", row[2])
        print("Amount Paid    :", row[3])
        print("Method         :", row[4])
        print("Status         :", row[5])
        print("====================================")
    else:
        print("Receipt Not Found")

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
