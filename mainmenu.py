import sys
from rich.console import Console

console = Console()

def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()

import user_authentication
import flight_management
import passenger_management
import book_management
import payment_management 
import airline_airport_management
import report

# ======================================================================
# STEP 2: FLIGHT MANAGEMENT MENU
# ======================================================================

def flight_management_menu():
    while True:
        heading("FLIGHT MANAGEMENT")
        print("1. Add Flight")
        print("2. View Flights")
        print("3. Search Flight")
        print("4. Update Flight")
        print("5. Delete Flight")
        print("6. Back")
        choice = input("Enter your choice: ")

        if choice == "1":
            flight_management.add_flight()
        elif choice == "2":
            flight_management.view_flight_menu()
        elif choice == "3":
            flight_management.search_flight_menu()
        elif choice == "4":
            flight_management.update_flight_menu()
        elif choice == "5":
            flight_management.delete_flight_menu()
        elif choice == "6":
            break
        else:
            print("Invalid Choice")


# ======================================================================
# STEP 3: AIRLINE & AIRPORT MANAGEMENT MENUS
# ======================================================================

def airline_management_menu():
    while True:
        heading("AIRLINE MANAGEMENT")
        print("1. Add Airline")
        print("2. View Airlines")
        print("3. Update Airline")
        print("4. Delete Airline")
        print("5. Back")
        choice = input("Enter Choice : ")

        if choice == "1":
            airline_airport_management.add_airline()
        elif choice == "2":
            airline_airport_management.view_airlines()
        elif choice == "3":
            airline_airport_management.update_airline()
        elif choice == "4":
            airline_airport_management.delete_airline()
        elif choice == "5":
            break
        else:
            print("Invalid Choice!")


def airport_management_menu():
    while True:
        heading("AIRPORT MANAGEMENT")
        print("1. Add Airport")
        print("2. View Airports")
        print("3. Update Airport")
        print("4. Delete Airport")
        print("5. Back")
        choice = input("Enter Choice : ")

        if choice == "1":
            airline_airport_management.add_airport()
        elif choice == "2":
            airline_airport_management.view_airports()
        elif choice == "3":
            airline_airport_management.update_airport()
        elif choice == "4":
            airline_airport_management.delete_airport()
        elif choice == "5":
            break
        else:
            print("Invalid Choice!")


def airport_airline_menu():
    while True:
        heading("Airline And Airport Management")
        print("1. Airline Management")
        print("2. Airport Management")
        print("3. Back")
        choice = input("Enter Choice : ")

        if choice == "1":
            airline_management_menu()
        elif choice == "2":
            airport_management_menu()
        elif choice == "3":
            break
        else:
            print("Invalid Choice!")


# ======================================================================
# STEP 4: PAYMENT MANAGEMENT MENUS
# ======================================================================

def make_payment_menu():
    while True:
        heading("MAKE PAYMENT")
        print("1. UPI")
        print("2. Credit/Debit Card")
        print("3. Net Banking")
        print("4. Back")
        choice = input("Enter Choice : ")

        if choice == "1":
            payment_management.make_payment("UPI")
        elif choice == "2":
            payment_management.make_payment("Credit/Debit Card")
        elif choice == "3":
            payment_management.make_payment("Net Banking")
        elif choice == "4":
            break
        else:
            print("Invalid Choice!")


def payment_history_menu():
    while True:
        heading(" PAYMENT HISTORY")
        print("1. View All Payments")
        print("2. Search by Payment ID")
        print("3. Search by Booking ID")
        print("4. Back")
        choice = input("Enter Choice : ")

        if choice == "1":
            payment_management.view_all_payments()
        elif choice == "2":
            payment_management.search_payment_id()
        elif choice == "3":
            payment_management.search_booking_id()
        elif choice == "4":
            break
        else:
            print("Invalid Choice!")


def ticket_receipt_menu():
    while True:
        heading("GENERATE TICKET / RECEIPT ")
        print("1. Generate Ticket")
        print("2. Generate Receipt")
        print("3. Print Ticket")
        print("4. Back")
        choice = input("Enter Choice : ")

        if choice == "1":
            payment_management.generate_ticket()
        elif choice == "2":
            payment_management.generate_receipt()
        elif choice == "3":
            payment_management.print_ticket()
        elif choice == "4":
            break
        else:
            print("Invalid Choice!")


def payment_management_menu():
    while True:
        heading(" PAYMENT MANAGEMENT")
        print("1. Make Payment")
        print("2. Payment History")
        print("3. Generate Ticket / Receipt")
        print("4. Back")
        choice = input("Enter Choice : ")

        if choice == "1":
            make_payment_menu()
        elif choice == "2":
            payment_history_menu()
        elif choice == "3":
            ticket_receipt_menu()
        elif choice == "4":
            break
        else:
            print("Invalid Choice!")


# ======================================================================
# STEP 5: ADMIN AND USER MENUS
# ======================================================================
def admin_menu():

    while True:

        heading("AIRLINE RESERVATION SYSTEM")

        print("Logged in as : ADMIN\n")

        print("  1. Flight Management")
        print("  2. Passenger Management")
        print("  3. Booking Management")
        print("  4. Payment Management")
        print("  5. Airport & Airline Management")
        print("  6. Reports")
        print("  7. Logout")

        choice = input("\nEnter Choice : ")

        if choice == "1":
            flight_management_menu()

        elif choice == "2":
            passenger_management.passenger_management()

        elif choice == "3":
            booking = book_management.BookingManagement()
            booking.main()

        elif choice == "4":
            payment_management_menu()

        elif choice == "5":
            airport_airline_menu()

        elif choice == "6":
            report.reports_menu()

        elif choice == "7":
            heading("LOGOUT")
            print("Logged Out Successfully.\n")
            break

        else:
            print("Invalid Choice!")


def user_menu():
    while True:
        print("\n=========================================")
        print("       AIRLINE RESERVATION SYSTEM")
        print("=========================================")
        print("Logged in as : USER\n")
        print("1. View Flights")
        print("2. Search Flight")
        print("3. Book Ticket")
        print("4. View My Bookings")
        print("5. Cancel Booking")
        print("6. Payment")
        print("7. Generate Ticket")
        print("8. Logout")

        choice = input("\nEnter Choice : ")

        if choice == "1":
            flight_management.view_flight_menu()
        elif choice == "2":
            flight_management.search_flight_menu()
        elif choice == "3":
            booking = book_management.BookingManagement()
            booking.book_ticket()
        elif choice == "4":
            booking = book_management.BookingManagement()
            booking.view_by_passenger_id()
        elif choice == "5":
            booking = book_management.BookingManagement()
            booking.cancel_booking()
        elif choice == "6":
            payment_management_menu()
        elif choice == "7":
            payment_management.generate_ticket()
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid Choice!")


def main():
    while True:

        heading("WELCOME TO AIRLINE SYSTEM")

        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":

            role = user_authentication.login()

            if role == "admin":
                admin_menu()

            elif role == "user":
                user_menu()

        elif choice == "2":

            user_authentication.register_user()

        elif choice == "3":

            heading("THANK YOU")
            print("Exiting Airline Reservation System...")
            sys.exit()

        else:

            print("Invalid Choice!")

if __name__ == "__main__":
    main()
