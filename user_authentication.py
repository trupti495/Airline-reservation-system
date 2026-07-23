from database import get_connection
from getpass import getpass
from rich.console import Console
from email.message import EmailMessage
import random


# ============================================================
# RICH CONSOLE
# ============================================================

console = Console()


# ============================================================
# COMMON HEADING
# ONLY HEADING HAS COLOR
# ============================================================

def heading(title):

    print()

    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )

    print()


# ============================================================
# 1.1 REGISTER USER
# ============================================================

def register_user():

    conn = get_connection()
    cursor = conn.cursor()

    heading("USER REGISTRATION")

    try:

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        username = input(
            "Enter Username : "
        ).strip()

        if username == "":
            print("Username cannot be empty.")
            return


        # ----------------------------------------------------
        # CHECK USERNAME
        # ONLY USERNAME MUST BE UNIQUE
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE LOWER(username) = LOWER(?)
            """,
            (username,)
        )

        if cursor.fetchone():

            print(
                "Username already exists. "
                "Please choose another username."
            )

            return


        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        password = getpass(
            "Enter Password : "
        ).strip()

        if password == "":
            print("Password cannot be empty.")
            return

        if len(password) < 6:

            print(
                "Password must contain at least 6 characters."
            )

            return


        # ----------------------------------------------------
        # PASSENGER DETAILS
        # ----------------------------------------------------

        print("\nEnter Passenger Details")


        # ----------------------------------------------------
        # AGE
        # ----------------------------------------------------

        age = int(
            input("Age : ")
        )

        if age <= 0:

            print("Invalid Age.")

            return


        # ----------------------------------------------------
        # GENDER
        # ----------------------------------------------------

        gender = input(
            "Gender (Male/Female/Other) : "
        ).strip().title()

        if gender not in [
            "Male",
            "Female",
            "Other"
        ]:

            print("Invalid Gender.")

            return


        # ----------------------------------------------------
        # PHONE
        # ----------------------------------------------------

        phone = input(
            "Phone Number : "
        ).strip()

        if not phone.isdigit() or len(phone) != 10:

            print(
                "Phone Number must contain exactly 10 digits."
            )

            return


        # ----------------------------------------------------
        # EMAIL
        # DUPLICATE EMAIL IS ALLOWED
        # ----------------------------------------------------

        email = input(
            "Email Address : "
        ).strip()

        if email == "":

            print(
                "Email Address cannot be empty."
            )

            return


        # ----------------------------------------------------
        # USER ROLE
        # ----------------------------------------------------

        role = "user"


        # ====================================================
        # INSERT INTO USERS TABLE
        # ====================================================

        cursor.execute(
            """
            INSERT INTO users(
                username,
                password,
                email,
                contact_no,
                role
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                username,
                password,
                email,
                phone,
                role
            )
        )


        # ----------------------------------------------------
        # GET USER ID
        # ----------------------------------------------------

        user_id = cursor.lastrowid


        # ====================================================
        # INSERT INTO PASSENGERS TABLE
        # user_id connects user and passenger
        # ====================================================

        cursor.execute(
            """
            INSERT INTO passengers(
                user_id,
                passenger_name,
                age,
                gender,
                phone,
                email
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                username,
                age,
                gender,
                phone,
                email
            )
        )


        # ----------------------------------------------------
        # GET PASSENGER ID
        # ----------------------------------------------------

        passenger_id = cursor.lastrowid


        # ----------------------------------------------------
        # SAVE BOTH RECORDS
        # ----------------------------------------------------

        conn.commit()


        # ====================================================
        # REGISTRATION SUCCESSFUL
        # ====================================================

        heading("REGISTRATION SUCCESSFUL")

        print(
            "User Account Created Successfully."
        )

        print(
            "User ID        :",
            user_id
        )

        print(
            "Username       :",
            username
        )

        print(
            "Passenger ID   :",
            passenger_id
        )

        print(
            "Email          :",
            email
        )

        print(
            "Please save your Passenger ID "
            "for future bookings."
        )


    except ValueError:

        conn.rollback()

        print(
            "Please enter valid numeric values."
        )


    except Exception as e:

        conn.rollback()

        print(
            "Registration Error :",
            e
        )


    finally:

        cursor.close()
        conn.close()


# ============================================================
# 1.2 LOGIN MENU
# ============================================================

def login():

    while True:

        heading("LOGIN")

        print("1. Login as Admin")
        print("2. Login as User")
        print("3. Back")

        try:

            choice = int(
                input(
                    "Enter Choice : "
                )
            )


            if choice == 1:

                return login_admin()


            elif choice == 2:

                return login_user()


            elif choice == 3:

                return None


            else:

                print(
                    "Invalid Choice."
                )


        except ValueError:

            print(
                "Enter numeric choice only."
            )

# ============================================================
# IMPORTS
# ============================================================

import time
import random
import smtplib

from email.message import EmailMessage
from getpass import getpass


# ============================================================
# 1.2.1 LOGIN AS ADMIN
# ============================================================

def login_admin():

    conn = get_connection()
    cursor = conn.cursor()

    heading("ADMIN LOGIN")

    try:

        # ====================================================
        # ADMIN USERNAME
        # ====================================================

        username = input(
            "Enter Username : "
        ).strip()


        # ====================================================
        # ADMIN PASSWORD
        # ====================================================

        password = getpass(
            "Enter Password : "
        ).strip()


        # ====================================================
        # CHECK ADMIN USERNAME AND PASSWORD
        # ====================================================

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE LOWER(username) = LOWER(?)
            AND password = ?
            AND LOWER(role) = 'admin'
            """,
            (
                username,
                password
            )
        )

        admin = cursor.fetchone()


        # ====================================================
        # INVALID LOGIN
        # ====================================================

        if not admin:

            print(
                "\nInvalid Username or Password."
            )

            return None


        # ====================================================
        # ENTER EMAIL ADDRESS
        # ====================================================

        receiver_email = input(
            "Enter Your Gmail Address : "
        ).strip()


        # ====================================================
        # CHECK EMAIL
        # ====================================================

        if receiver_email == "":

            print(
                "\nEmail Address cannot be empty."
            )

            return None


        # ====================================================
        # GMAIL DETAILS
        # ====================================================

        sender_email = "shitoletrupti6@gmail.com"

        # Enter your NEW Google App Password here
        app_password = "hyjspiqilotmbanw"


        # ====================================================
        # GENERATE OTP
        # OTP IS GENERATED ONLY ONCE
        # ====================================================

        otp = str(
            random.randint(
                100000,
                999999
            )
        )


        # ====================================================
        # START OTP TIMER
        # OTP VALIDITY = 2 MINUTES
        # ====================================================

        otp_generated_time = time.time()


        # ====================================================
        # CREATE EMAIL
        # ====================================================

        message = EmailMessage()

        message["Subject"] = "Admin Login OTP"

        message["From"] = sender_email

        message["To"] = receiver_email


        message.set_content(
            f"""
Hello Admin,

Your OTP for Admin Login is:

{otp}

This OTP is valid for 2 minutes.

You have a maximum of 3 attempts
to enter the correct OTP.

Do not share this OTP with anyone.

Thank You
Airline Reservation System
"""
        )


        # ====================================================
        # SEND OTP EMAIL
        # ====================================================

        try:

            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465
            ) as server:

                server.login(
                    sender_email,
                    app_password
                )

                server.send_message(
                    message
                )


            print(
                "\nOTP has been sent successfully."
            )


        except Exception as e:

            print(
                "\nFailed to send OTP."
            )

            print(
                "Error :",
                e
            )

            return None


        # ====================================================
        # OTP VERIFICATION
        # MAXIMUM 3 ATTEMPTS
        # ====================================================

        max_attempts = 3

        attempts = 0


        while attempts < max_attempts:


            # =================================================
            # CHECK 2 MINUTE OTP EXPIRY
            # =================================================

            elapsed_time = (
                time.time()
                - otp_generated_time
            )


            if elapsed_time >= 120:

                print(
                    "\nOTP has expired."
                )

                print(
                    "OTP validity is only 2 minutes."
                )

                print(
                    "Please login again to receive "
                    "a new OTP."
                )

                return None


            # =================================================
            # ENTER OTP
            # =================================================

            entered_otp = input(
                "\nEnter OTP : "
            ).strip()


            # =================================================
            # CHECK OTP
            # =================================================

            if entered_otp == otp:

                print(
                    "\nAdmin Login Successful."
                )

                return "admin"


            # =================================================
            # WRONG OTP
            # =================================================

            else:

                attempts += 1

                remaining_attempts = (
                    max_attempts
                    - attempts
                )


                if remaining_attempts > 0:

                    print(
                        "\nInvalid OTP."
                    )

                    print(
                        "Remaining Attempts :",
                        remaining_attempts
                    )


                else:

                    print(
                        "\nInvalid OTP."
                    )

                    print(
                        "Maximum OTP attempts exceeded."
                    )

                    print(
                        "Admin Login Failed."
                    )

                    return None


        # ====================================================
        # OTP VERIFICATION FAILED
        # ====================================================

        return None


    # ========================================================
    # CLOSE DATABASE CONNECTION
    # ========================================================

    finally:

        cursor.close()

        conn.close()

def login_user():

    conn = get_connection()
    cursor = conn.cursor()

    heading("USER LOGIN")

    try:

        # ----------------------------------------------------
        # USERNAME
        # ----------------------------------------------------

        username = input(
            "Enter Username : "
        ).strip()


        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        password = getpass(
            "Enter Password : "
        ).strip()


        # ----------------------------------------------------
        # CHECK USER LOGIN
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                email
            FROM users
            WHERE LOWER(username) = LOWER(?)
            AND password = ?
            AND LOWER(role) = 'user'
            """,
            (
                username,
                password
            )
        )


        user = cursor.fetchone()


        if not user:

            print(
                "Invalid Username or Password."
            )

            return None


        # ----------------------------------------------------
        # GET USER ID
        # ----------------------------------------------------

        user_id = user[0]


        # ----------------------------------------------------
        # GET PASSENGER USING USER ID
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                passenger_id,
                passenger_name,
                phone,
                email
            FROM passengers
            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )


        passenger = cursor.fetchone()


        # ====================================================
        # LOGIN SUCCESSFUL
        # ====================================================

        print()

        print(
            "===================================="
        )

        print(
            "     USER LOGIN SUCCESSFUL"
        )

        print(
            "===================================="
        )


        print(
            "User ID        :",
            user_id
        )


        if passenger:

            print(
                "Passenger ID   :",
                passenger[0]
            )

            print(
                "Passenger Name :",
                passenger[1]
            )

            print(
                "Phone          :",
                passenger[2]
            )

            print(
                "Email          :",
                passenger[3]
            )

            print(
                "Please keep your Passenger ID "
                "for booking tickets."
            )


        else:

            print(
                "Passenger record not found."
            )


        print(
            "===================================="
        )

        print()


        return "user"


    finally:

        cursor.close()
        conn.close()


# ============================================================
# 1.3 LOGOUT
# ============================================================

def logout():

    heading("LOGOUT")

    print(
        "Logout Successful."
    )


# ============================================================
# RUN MODULE DIRECTLY
# ============================================================

if __name__ == "__main__":

    while True:

        heading(
            "USER AUTHENTICATION"
        )


        print("1. Register User")
        print("2. Login")
        print("3. Logout")
        print("4. Exit")


        choice = input(
            "Enter Choice : "
        ).strip()


        if choice == "1":

            register_user()


        elif choice == "2":

            login()


        elif choice == "3":

            logout()


        elif choice == "4":

            print(
                "Exiting User Authentication..."
            )

            break


        else:

            print(
                "Invalid Choice."
            )