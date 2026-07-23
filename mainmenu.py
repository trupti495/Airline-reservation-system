import sys

from rich.console import Console

import user_authentication
import flight_management
import passenger_management
import book_management
import payment_management
import airline_airport_management
import report
import forgot


# ======================================================================
# RICH CONSOLE
# ======================================================================

console = Console()


# ======================================================================
# COMMON HEADING
# ONLY HEADING HAS COLOR
# ======================================================================

def heading(title):

    print()

    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )

    print()


# ======================================================================
# FLIGHT MANAGEMENT MENU
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

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

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

            print(
                "Invalid Choice!"
            )


# ======================================================================
# AIRLINE MANAGEMENT MENU
# ======================================================================

def airline_management_menu():

    while True:

        heading("AIRLINE MANAGEMENT")

        print("1. Add Airline")
        print("2. View Airlines")
        print("3. Update Airline")
        print("4. Delete Airline")
        print("5. Back")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

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

            print(
                "Invalid Choice!"
            )


# ======================================================================
# AIRPORT MANAGEMENT MENU
# ======================================================================

def airport_management_menu():

    while True:

        heading("AIRPORT MANAGEMENT")

        print("1. Add Airport")
        print("2. View Airports")
        print("3. Update Airport")
        print("4. Delete Airport")
        print("5. Back")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

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

            print(
                "Invalid Choice!"
            )


# ======================================================================
# AIRLINE & AIRPORT MANAGEMENT MENU
# ======================================================================

def airport_airline_menu():

    while True:

        heading(
            "AIRLINE & AIRPORT MANAGEMENT"
        )

        print("1. Airline Management")
        print("2. Airport Management")
        print("3. Back")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

        if choice == "1":

            airline_management_menu()

        elif choice == "2":

            airport_management_menu()

        elif choice == "3":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ======================================================================
# MAKE PAYMENT MENU
# ======================================================================

def make_payment_menu():

    while True:

        heading("MAKE PAYMENT")

        print("1. UPI")
        print("2. Credit/Debit Card")
        print("3. Net Banking")
        print("4. Back")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

        if choice == "1":

            payment_management.make_payment(
                "UPI"
            )

        elif choice == "2":

            payment_management.make_payment(
                "Credit/Debit Card"
            )

        elif choice == "3":

            payment_management.make_payment(
                "Net Banking"
            )

        elif choice == "4":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ======================================================================
# PAYMENT HISTORY MENU
# ======================================================================

def payment_history_menu():

    while True:

        heading("PAYMENT HISTORY")

        print("1. View All Payments")
        print("2. Search by Payment ID")
        print("3. Search by Booking ID")
        print("4. Back")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

        if choice == "1":

            payment_management.view_all_payments()

        elif choice == "2":

            payment_management.search_payment_id()

        elif choice == "3":

            payment_management.search_booking_id()

        elif choice == "4":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ======================================================================
# TICKET / RECEIPT MENU
# ======================================================================

def ticket_receipt_menu():

    while True:

        heading("GENERATE TICKET / RECEIPT")

        print("1. Print Ticket")
        print("2. Back")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

        if choice == "1":

            payment_management.print_ticket()

        elif choice == "2":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ======================================================================
# PAYMENT MANAGEMENT MENU
# ======================================================================

def payment_management_menu():

    while True:

        heading("PAYMENT MANAGEMENT")

        print("1. Make Payment")
        print("2. Payment History")
        print("3. Generate Ticket / Receipt")
        print("4. Back")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

        if choice == "1":

            make_payment_menu()

        elif choice == "2":

            payment_history_menu()

        elif choice == "3":

            ticket_receipt_menu()

        elif choice == "4":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ======================================================================
# BOOKING MANAGEMENT MENU
# IMPORTANT:
# Your book_management.py already contains:
# booking_management()
#
# Therefore simply call:
# book_management.booking_management()
# ======================================================================


# ======================================================================
# ADMIN MENU
# ======================================================================

def admin_menu():

    while True:

        heading(
            "AIRLINE RESERVATION SYSTEM"
        )

        print(
            "Logged in as : ADMIN\n"
        )

        print(
            "1. Passenger Management"
        )

        print(
            "2. Airport & Airline Management"
        )

        print(
            "3. Flight Management"
        )

        print(
            "4. Booking Management"
        )

        print(
            "5. Payment Management"
        )

        print(
            "6. Reports"
        )

        print(
            "7. Logout"
        )

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

        # --------------------------------------------------
        # PASSENGER MANAGEMENT
        # --------------------------------------------------

        if choice == "1":

            passenger_management.passenger_management()

        # --------------------------------------------------
        # AIRPORT & AIRLINE MANAGEMENT
        # --------------------------------------------------

        elif choice == "2":

            airport_airline_menu()

        # --------------------------------------------------
        # FLIGHT MANAGEMENT
        # --------------------------------------------------

        elif choice == "3":

            flight_management_menu()

        # --------------------------------------------------
        # BOOKING MANAGEMENT
        # --------------------------------------------------

        elif choice == "4":

            book_management.booking_management()

        # --------------------------------------------------
        # PAYMENT MANAGEMENT
        # --------------------------------------------------

        elif choice == "5":

            payment_management_menu()

        # --------------------------------------------------
        # REPORTS
        # --------------------------------------------------

        elif choice == "6":

            report.reports_menu()

        # --------------------------------------------------
        # LOGOUT
        # --------------------------------------------------

        elif choice == "7":

            heading("LOGOUT")

            print(
                "Logged Out Successfully."
            )

            break

        else:

            print(
                "Invalid Choice!"
            )


# ======================================================================
# USER MENU
# ======================================================================

def user_menu():

    while True:

        heading(
            "AIRLINE RESERVATION SYSTEM"
        )

        print(
            "Logged in as : USER\n"
        )

        print("1. View Flights")
        print("2. Search Flight")
        print("3. Book Ticket")
        print("4. View Booking")
        print("5. Cancel Booking")
        print("6. Payment")
        print("7. Generate Ticket")
        print("8. Logout")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

        # --------------------------------------------------
        # VIEW FLIGHTS
        # --------------------------------------------------

        if choice == "1":

            flight_management.view_flight_menu()

        # --------------------------------------------------
        # SEARCH FLIGHT
        # --------------------------------------------------

        elif choice == "2":

            flight_management.search_flight_menu()

        # --------------------------------------------------
        # BOOK TICKET
        # --------------------------------------------------

        elif choice == "3":

            book_management.book_ticket()

        # --------------------------------------------------
        # VIEW BOOKING
        # --------------------------------------------------

        elif choice == "4":

            book_management.view_booking()

        # --------------------------------------------------
        # CANCEL BOOKING
        # --------------------------------------------------

        elif choice == "5":

            book_management.cancel_booking()

        # --------------------------------------------------
        # PAYMENT
        # --------------------------------------------------

        elif choice == "6":

            payment_management_menu()

        # --------------------------------------------------
        # GENERATE TICKET
        # --------------------------------------------------

        elif choice == "7":

            payment_management.generate_ticket()

        # --------------------------------------------------
        # LOGOUT
        # --------------------------------------------------

        elif choice == "8":

            heading("LOGOUT")

            print(
                "Logged Out Successfully."
            )

            break

        else:

            print(
                "Invalid Choice!"
            )


# ======================================================================
# MAIN MENU
# ======================================================================

def main():

    while True:

        heading(
            "WELCOME TO AIRLINE RESERVATION SYSTEM"
        )

        print("1. Login")
        print("2. Register")
        print("3. Forgot Password")
        print("4. Exit")

        choice = input(
            "\nEnter Your Choice : "
        ).strip()

        # --------------------------------------------------
        # LOGIN
        # --------------------------------------------------

        if choice == "1":

            role = user_authentication.login()

            if role == "admin":

                admin_menu()

            elif role == "user":

                user_menu()

        # --------------------------------------------------
        # REGISTER
        # --------------------------------------------------

        elif choice == "2":

            user_authentication.register_user()

        # --------------------------------------------------
        # FORGOT PASSWORD
        # --------------------------------------------------

        elif choice == "3":

            forgot.forgot_password()

        # --------------------------------------------------
        # EXIT
        # --------------------------------------------------

        elif choice == "4":

            heading("THANK YOU")

            print(
                "Exiting Airline Reservation System..."
            )

            sys.exit()

        else:

            print(
                "Invalid Choice!"
            )


# ======================================================================
# START APPLICATION
# ======================================================================

if __name__ == "__main__":

    main()