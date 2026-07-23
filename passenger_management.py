from database import get_connection
from rich.console import Console
from rich.table import Table


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
# COMMON HEADING FUNCTION
# ============================================================

def heading(title):

    print()

    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )

    print()


# ============================================================
# 1. ADD PASSENGER
# ============================================================

def add_passenger():

    heading("ADD PASSENGER")

    try:

        # ====================================================
        # PASSENGER DETAILS
        # ====================================================

        passenger_name = input(
            "Enter Passenger Name : "
        ).strip().title()

        age_input = input(
            "Enter Age : "
        ).strip()

        gender = input(
            "Enter Gender (Male/Female/Other) : "
        ).strip().title()

        phone = input(
            "Enter Contact Number : "
        ).strip()

        email = input(
            "Enter Email : "
        ).strip().lower()

        # ====================================================
        # USER LOGIN DETAILS
        # ====================================================

        username = input(
            "Enter Username : "
        ).strip()

        password = input(
            "Enter Password : "
        ).strip()

        # ====================================================
        # VALIDATION
        # ====================================================

        if not passenger_name:

            print("Passenger Name Cannot Be Empty!")
            return

        if not age_input.isdigit():

            print("Age Must Be Numeric!")
            return

        age = int(age_input)

        if age <= 0:

            print("Invalid Age!")
            return

        if gender not in ["Male", "Female", "Other"]:

            print("Invalid Gender!")
            return

        if len(phone) != 10 or not phone.isdigit():

            print("Contact Number Must Be 10 Digits!")
            return

        if not email or "@" not in email:

            print("Enter a Valid Email Address!")
            return

        if not username:

            print("Username Cannot Be Empty!")
            return

        if len(password) < 6:

            print(
                "Password Must Contain At Least 6 Characters!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE PHONE
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM passengers
            WHERE phone=?
            """,
            (phone,)
        )

        if cursor.fetchone():

            print(
                "Contact Number Already Exists!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE USER CONTACT NUMBER
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE contact_no=?
            """,
            (phone,)
        )

        if cursor.fetchone():

            print(
                "Contact Number Already Exists!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE USERNAME
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE LOWER(username)=LOWER(?)
            """,
            (username,)
        )

        if cursor.fetchone():

            print(
                "Username Already Exists!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE EMAIL IN USERS
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE LOWER(email)=LOWER(?)
            """,
            (email,)
        )

        if cursor.fetchone():

            print(
                "Email Already Exists!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE EMAIL IN PASSENGERS
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM passengers
            WHERE LOWER(email)=LOWER(?)
            """,
            (email,)
        )

        if cursor.fetchone():

            print(
                "Email Already Exists!"
            )
            return

        # ====================================================
        # INSERT INTO USERS TABLE
        # ====================================================
        role=input("enter role:(user/admin):")
        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                email,
                contact_no,
                role
            )
            VALUES (?, ?, ?, ?,?)
            """,
            (
                username,
                password,
                email,
                phone,
                role
            )
        )

        # Get generated user ID
        user_id = cursor.lastrowid

        # ====================================================
        # INSERT INTO PASSENGERS TABLE
        # ====================================================

        cursor.execute(
            """
            INSERT INTO passengers
            (
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
                passenger_name,
                age,
                gender,
                phone,
                email
            )
        )

        # Get generated passenger ID
        passenger_id = cursor.lastrowid
        conn.commit()
        heading(
            "PASSENGER ADDED SUCCESSFULLY"
        )

        print("Passenger ID :",passenger_id)

        print(
            "User ID      :",
            user_id
        )

        print(
            "Passenger Name :",
            passenger_name
        )

        print(
            "Username     :",
            username
        )

        print(
            "Email        :",
            email
        )

        print(
            "Contact No   :",
            phone
        )

        print(
            "Role         : ",role
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error :",
            e
        )


# ============================================================
# 2. VIEW ALL PASSENGERS
# ============================================================

def view_all_passengers():

    heading("ALL PASSENGERS")

    try:

        cursor.execute(
            """
            SELECT
                p.passenger_id,
                p.user_id,
                p.passenger_name,
                p.age,
                p.gender,
                p.phone,
                p.email,
                u.username
            FROM passengers p
            JOIN users u
            ON p.user_id = u.user_id
            ORDER BY p.passenger_id
            """
        )

        passengers = cursor.fetchall()

        if not passengers:

            print(
                "No Passenger Records Found!"
            )
            return

        table = Table(
            title="Passenger Details"
        )

        table.add_column(
            "Passenger ID",
            justify="center",
            style="cyan"
        )

        table.add_column(
            "User ID",
            justify="center"
        )

        table.add_column(
            "Passenger Name",
            style="green"
        )

        table.add_column(
            "Age",
            justify="center"
        )

        table.add_column(
            "Gender",
            justify="center"
        )

        table.add_column(
            "Phone",
            justify="center"
        )

        table.add_column(
            "Email"
        )

        table.add_column(
            "Username"
        )

        for passenger in passengers:

            table.add_row(
                str(passenger[0]),
                str(passenger[1]),
                passenger[2],
                str(passenger[3]),
                passenger[4],
                passenger[5],
                passenger[6],
                passenger[7]
            )

        console.print(table)

    except Exception as e:

        print(
            "Error :",
            e
        )


# ============================================================
# 3. VIEW PASSENGER BY ID
# ============================================================

def view_passenger_by_id():

    heading("VIEW PASSENGER BY ID")

    try:

        passenger_id = int(
            input(
                "Enter Passenger ID : "
            )
        )

        cursor.execute(
            """
            SELECT
                p.passenger_id,
                p.user_id,
                p.passenger_name,
                p.age,
                p.gender,
                p.phone,
                p.email,
                u.username,
                u.role
            FROM passengers p
            JOIN users u
            ON p.user_id = u.user_id
            WHERE p.passenger_id=?
            """,
            (passenger_id,)
        )

        passenger = cursor.fetchone()

        if not passenger:

            print(
                "Passenger ID Not Found!"
            )
            return

        table = Table(
            title="Passenger Details"
        )

        table.add_column(
            "Field",
            style="cyan"
        )

        table.add_column(
            "Details",
            style="green"
        )

        table.add_row(
            "Passenger ID",
            str(passenger[0])
        )

        table.add_row(
            "User ID",
            str(passenger[1])
        )

        table.add_row(
            "Passenger Name",
            passenger[2]
        )

        table.add_row(
            "Age",
            str(passenger[3])
        )

        table.add_row(
            "Gender",
            passenger[4]
        )

        table.add_row(
            "Phone",
            passenger[5]
        )

        table.add_row(
            "Email",
            passenger[6]
        )

        table.add_row(
            "Username",
            passenger[7]
        )

        table.add_row(
            "Role",
            passenger[8]
        )

        console.print(table)

    except ValueError:

        print(
            "Passenger ID Must Be Numeric!"
        )

    except Exception as e:

        print(
            "Error :",
            e
        )


# ============================================================
# 4. VIEW PASSENGER BY NAME
# ============================================================

def view_passenger_by_name():

    heading("VIEW PASSENGER BY NAME")

    try:

        passenger_name = input(
            "Enter Passenger Name : "
        ).strip()

        if not passenger_name:

            print(
                "Passenger Name Cannot Be Empty!"
            )
            return

        cursor.execute(
            """
            SELECT
                p.passenger_id,
                p.user_id,
                p.passenger_name,
                p.age,
                p.gender,
                p.phone,
                p.email,
                u.username
            FROM passengers p
            JOIN users u
            ON p.user_id = u.user_id
            WHERE LOWER(p.passenger_name)
            LIKE ?
            """,
            (
                "%" +
                passenger_name.lower() +
                "%",
            )
        )

        passengers = cursor.fetchall()

        if not passengers:

            print(
                "Passenger Not Found!"
            )
            return

        table = Table(
            title="Passenger Details"
        )

        table.add_column(
            "Passenger ID",
            justify="center",
            style="cyan"
        )

        table.add_column(
            "User ID",
            justify="center"
        )

        table.add_column(
            "Passenger Name",
            style="green"
        )

        table.add_column(
            "Age",
            justify="center"
        )

        table.add_column(
            "Gender",
            justify="center"
        )

        table.add_column(
            "Phone",
            justify="center"
        )

        table.add_column(
            "Email"
        )

        table.add_column(
            "Username"
        )

        for passenger in passengers:

            table.add_row(
                str(passenger[0]),
                str(passenger[1]),
                passenger[2],
                str(passenger[3]),
                passenger[4],
                passenger[5],
                passenger[6],
                passenger[7]
            )

        console.print(table)

    except Exception as e:

        print(
            "Error :",
            e
        )


# ============================================================
# 5. UPDATE PASSENGER
# ============================================================

def update_passenger():

    heading("UPDATE PASSENGER")

    try:

        passenger_id = int(
            input(
                "Enter Passenger ID : "
            )
        )

        # ====================================================
        # GET EXISTING PASSENGER
        # ====================================================

        cursor.execute(
            """
            SELECT
                passenger_id,
                user_id
            FROM passengers
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        passenger = cursor.fetchone()

        if not passenger:

            print(
                "Passenger ID Not Found!"
            )
            return

        user_id = passenger[1]

        # ====================================================
        # NEW DETAILS
        # ====================================================

        passenger_name = input(
            "Enter New Passenger Name : "
        ).strip().title()

        age_input = input(
            "Enter New Age : "
        ).strip()

        gender = input(
            "Enter New Gender (Male/Female/Other) : "
        ).strip().title()

        phone = input(
            "Enter New Contact Number : "
        ).strip()

        email = input(
            "Enter New Email : "
        ).strip().lower()

        # ====================================================
        # VALIDATION
        # ====================================================

        if not passenger_name:

            print(
                "Passenger Name Cannot Be Empty!"
            )
            return

        if not age_input.isdigit():

            print(
                "Age Must Be Numeric!"
            )
            return

        age = int(age_input)

        if age <= 0:

            print(
                "Invalid Age!"
            )
            return

        if gender not in [
            "Male",
            "Female",
            "Other"
        ]:

            print(
                "Invalid Gender!"
            )
            return

        if len(phone) != 10 or not phone.isdigit():

            print(
                "Contact Number Must Be 10 Digits!"
            )
            return

        if not email or "@" not in email:

            print(
                "Enter a Valid Email Address!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE PHONE IN PASSENGERS
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM passengers
            WHERE phone=?
            AND passenger_id!=?
            """,
            (
                phone,
                passenger_id
            )
        )

        if cursor.fetchone():

            print(
                "Contact Number Already Exists!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE CONTACT IN USERS
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE contact_no=?
            AND user_id!=?
            """,
            (
                phone,
                user_id
            )
        )

        if cursor.fetchone():

            print(
                "Contact Number Already Exists!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE EMAIL IN PASSENGERS
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM passengers
            WHERE LOWER(email)=LOWER(?)
            AND passenger_id!=?
            """,
            (
                email,
                passenger_id
            )
        )

        if cursor.fetchone():

            print(
                "Email Already Exists!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE EMAIL IN USERS
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE LOWER(email)=LOWER(?)
            AND user_id!=?
            """,
            (
                email,
                user_id
            )
        )

        if cursor.fetchone():

            print(
                "Email Already Exists!"
            )
            return

        # ====================================================
        # UPDATE PASSENGERS TABLE
        # ====================================================

        cursor.execute(
            """
            UPDATE passengers
            SET
                passenger_name=?,
                age=?,
                gender=?,
                phone=?,
                email=?
            WHERE passenger_id=?
            """,
            (
                passenger_name,
                age,
                gender,
                phone,
                email,
                passenger_id
            )
        )

        # ====================================================
        # UPDATE USERS TABLE
        # ====================================================

        cursor.execute(
            """
            UPDATE users
            SET
                email=?,
                contact_no=?
            WHERE user_id=?
            """,
            (
                email,
                phone,
                user_id
            )
        )

        # ====================================================
        # COMMIT
        # ====================================================

        conn.commit()

        print(
            "Passenger Details Updated Successfully!"
        )

        print(
            "Users Table Also Updated Successfully!"
        )

    except ValueError:

        print(
            "Passenger ID and Age Must Be Numeric!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error :",
            e
        )


# ============================================================
# 6. UPDATE CONTACT NUMBER
# ============================================================

def update_contact_number():

    heading("UPDATE CONTACT NUMBER")

    try:

        passenger_id = int(
            input(
                "Enter Passenger ID : "
            )
        )

        phone = input(
            "Enter New Contact Number : "
        ).strip()

        # ====================================================
        # VALIDATION
        # ====================================================

        if len(phone) != 10 or not phone.isdigit():

            print(
                "Contact Number Must Be 10 Digits!"
            )
            return

        # ====================================================
        # GET USER ID
        # ====================================================

        cursor.execute(
            """
            SELECT user_id
            FROM passengers
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        passenger = cursor.fetchone()

        if not passenger:

            print(
                "Passenger ID Not Found!"
            )
            return

        user_id = passenger[0]

        # ====================================================
        # CHECK DUPLICATE PHONE
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM passengers
            WHERE phone=?
            AND passenger_id!=?
            """,
            (
                phone,
                passenger_id
            )
        )

        if cursor.fetchone():

            print(
                "Contact Number Already Exists!"
            )
            return

        # ====================================================
        # CHECK DUPLICATE USER CONTACT
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM users
            WHERE contact_no=?
            AND user_id!=?
            """,
            (
                phone,
                user_id
            )
        )

        if cursor.fetchone():

            print(
                "Contact Number Already Exists!"
            )
            return

        # ====================================================
        # UPDATE PASSENGERS
        # ====================================================

        cursor.execute(
            """
            UPDATE passengers
            SET phone=?
            WHERE passenger_id=?
            """,
            (
                phone,
                passenger_id
            )
        )

        # ====================================================
        # UPDATE USERS
        # ====================================================

        cursor.execute(
            """
            UPDATE users
            SET contact_no=?
            WHERE user_id=?
            """,
            (
                phone,
                user_id
            )
        )

        conn.commit()

        print(
            "Contact Number Updated Successfully!"
        )

        print(
            "Users Table Also Updated Successfully!"
        )

    except ValueError:

        print(
            "Passenger ID Must Be Numeric!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error :",
            e
        )


# ============================================================
# 7. EMERGENCY INFORMATION
# ============================================================

def add_emergency_info():

    heading("ADD EMERGENCY INFORMATION")

    try:

        passenger_id = int(
            input(
                "Enter Passenger ID : "
            )
        )

        # ====================================================
        # CHECK PASSENGER
        # ====================================================

        cursor.execute(
            """
            SELECT passenger_name
            FROM passengers
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        passenger = cursor.fetchone()

        if not passenger:

            print(
                "Passenger ID Not Found!"
            )
            return

        # ====================================================
        # CHECK EXISTING EMERGENCY INFO
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM passenger_emergency_info
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        if cursor.fetchone():

            print(
                "Emergency Information Already Exists!"
            )
            print(
                "Use Update Emergency Information."
            )
            return

        # ====================================================
        # INPUT DETAILS
        # ====================================================

        blood_group = input(
            "Enter Blood Group : "
        ).strip().upper()

        emergency_name = input(
            "Enter Emergency Contact Name : "
        ).strip().title()

        emergency_phone = input(
            "Enter Emergency Contact Number : "
        ).strip()

        relationship = input(
            "Enter Relationship : "
        ).strip().title()

        # ====================================================
        # VALIDATION
        # ====================================================

        if not blood_group:

            print(
                "Blood Group Cannot Be Empty!"
            )
            return

        if not emergency_name:

            print(
                "Emergency Contact Name Cannot Be Empty!"
            )
            return

        if len(emergency_phone) != 10 or not emergency_phone.isdigit():

            print(
                "Emergency Contact Number Must Be 10 Digits!"
            )
            return

        if not relationship:

            print(
                "Relationship Cannot Be Empty!"
            )
            return

        # ====================================================
        # INSERT
        # ====================================================

        cursor.execute(
            """
            INSERT INTO passenger_emergency_info
            (
                passenger_id,
                blood_group,
                emergency_contact_name,
                emergency_contact_no,
                relationship
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                passenger_id,
                blood_group,
                emergency_name,
                emergency_phone,
                relationship
            )
        )

        conn.commit()

        print(
            "Emergency Information Added Successfully!"
        )

    except ValueError:

        print(
            "Passenger ID Must Be Numeric!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error :",
            e
        )


# ============================================================
# 8. VIEW EMERGENCY INFORMATION
# ============================================================

def view_emergency_info():

    heading("VIEW EMERGENCY INFORMATION")

    try:

        passenger_id = int(
            input(
                "Enter Passenger ID : "
            )
        )

        cursor.execute(
            """
            SELECT
                p.passenger_name,
                e.blood_group,
                e.emergency_contact_name,
                e.emergency_contact_no,
                e.relationship
            FROM passengers p
            JOIN passenger_emergency_info e
            ON p.passenger_id = e.passenger_id
            WHERE p.passenger_id=?
            """,
            (passenger_id,)
        )

        emergency = cursor.fetchone()

        if not emergency:

            print(
                "Emergency Information Not Found!"
            )
            return

        table = Table(
            title="Emergency Information"
        )

        table.add_column(
            "Field",
            style="cyan"
        )

        table.add_column(
            "Details",
            style="green"
        )

        table.add_row(
            "Passenger Name",
            emergency[0]
        )

        table.add_row(
            "Blood Group",
            emergency[1]
        )

        table.add_row(
            "Emergency Contact Name",
            emergency[2]
        )

        table.add_row(
            "Emergency Contact Number",
            emergency[3]
        )

        table.add_row(
            "Relationship",
            emergency[4]
        )

        console.print(table)

    except ValueError:

        print(
            "Passenger ID Must Be Numeric!"
        )

    except Exception as e:

        print(
            "Error :",
            e
        )


# ============================================================
# 9. UPDATE EMERGENCY INFORMATION
# ============================================================

def update_emergency_info():

    heading("UPDATE EMERGENCY INFORMATION")

    try:

        passenger_id = int(
            input(
                "Enter Passenger ID : "
            )
        )

        # ====================================================
        # CHECK EXISTING RECORD
        # ====================================================

        cursor.execute(
            """
            SELECT 1
            FROM passenger_emergency_info
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        if not cursor.fetchone():

            print(
                "Emergency Information Not Found!"
            )
            return

        # ====================================================
        # INPUT
        # ====================================================

        blood_group = input(
            "Enter New Blood Group : "
        ).strip().upper()

        emergency_name = input(
            "Enter New Emergency Contact Name : "
        ).strip().title()

        emergency_phone = input(
            "Enter New Emergency Contact Number : "
        ).strip()

        relationship = input(
            "Enter New Relationship : "
        ).strip().title()

        # ====================================================
        # VALIDATION
        # ====================================================

        if not blood_group:

            print(
                "Blood Group Cannot Be Empty!"
            )
            return

        if not emergency_name:

            print(
                "Emergency Contact Name Cannot Be Empty!"
            )
            return

        if len(emergency_phone) != 10 or not emergency_phone.isdigit():

            print(
                "Emergency Contact Number Must Be 10 Digits!"
            )
            return

        if not relationship:

            print(
                "Relationship Cannot Be Empty!"
            )
            return

        # ====================================================
        # UPDATE
        # ====================================================

        cursor.execute(
            """
            UPDATE passenger_emergency_info
            SET
                blood_group=?,
                emergency_contact_name=?,
                emergency_contact_no=?,
                relationship=?
            WHERE passenger_id=?
            """,
            (
                blood_group,
                emergency_name,
                emergency_phone,
                relationship,
                passenger_id
            )
        )

        conn.commit()

        print(
            "Emergency Information Updated Successfully!"
        )

    except ValueError:

        print(
            "Passenger ID Must Be Numeric!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error :",
            e
        )


# ============================================================
# 10. DELETE PASSENGER BY ID
# ============================================================

def delete_passenger_by_id():

    heading("DELETE PASSENGER")

    try:

        passenger_id = int(
            input(
                "Enter Passenger ID : "
            )
        )

        # ====================================================
        # CHECK PASSENGER
        # ====================================================

        cursor.execute(
            """
            SELECT
                user_id,
                passenger_name
            FROM passengers
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        passenger = cursor.fetchone()

        if not passenger:

            print(
                "Passenger ID Not Found!"
            )
            return

        user_id = passenger[0]
        passenger_name = passenger[1]

        # ====================================================
        # CHECK BOOKINGS
        # ====================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        booking_count = cursor.fetchone()[0]

        if booking_count > 0:

            print(
                f"Cannot Delete Passenger!"
            )

            print(
                f"{passenger_name} has "
                f"{booking_count} booking(s)."
            )

            print(
                "Please cancel/delete bookings first."
            )

            return

        # ====================================================
        # CONFIRMATION
        # ====================================================

        confirm = input(
            "Are You Sure You Want To Delete "
            "This Passenger? (Yes/No) : "
        ).strip().lower()

        if confirm != "yes":

            print(
                "Delete Operation Cancelled."
            )
            return

        # ====================================================
        # DELETE PASSENGER
        # ====================================================

        cursor.execute(
            """
            DELETE FROM passengers
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        # ====================================================
        # DELETE USER
        # ====================================================

        cursor.execute(
            """
            DELETE FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )

        conn.commit()

        print(
            "Passenger Deleted Successfully!"
        )

        print(
            "Associated User Account Deleted Successfully!"
        )

        print(
            "Emergency Information Deleted Automatically!"
        )

    except ValueError:

        print(
            "Passenger ID Must Be Numeric!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error :",
            e
        )


# ============================================================
# 11. DELETE PASSENGER BY NAME
# ============================================================

def delete_passenger_by_name():

    heading("DELETE PASSENGER BY NAME")

    try:

        passenger_name = input(
            "Enter Passenger Name : "
        ).strip()

        if not passenger_name:

            print(
                "Passenger Name Cannot Be Empty!"
            )
            return

        cursor.execute(
            """
            SELECT
                passenger_id,
                passenger_name
            FROM passengers
            WHERE LOWER(passenger_name)=LOWER(?)
            """,
            (passenger_name,)
        )

        passengers = cursor.fetchall()

        if not passengers:

            print(
                "Passenger Name Not Found!"
            )
            return

        if len(passengers) > 1:

            print(
                "Multiple Passengers Found "
                "With This Name."
            )

            table = Table(
                title="Matching Passengers"
            )

            table.add_column(
                "Passenger ID",
                justify="center"
            )

            table.add_column(
                "Passenger Name"
            )

            for passenger in passengers:

                table.add_row(
                    str(passenger[0]),
                    passenger[1]
                )

            console.print(table)

            print(
                "Please use Delete by Passenger ID."
            )

            return

        passenger_id = passengers[0][0]

        # ====================================================
        # CHECK BOOKINGS
        # ====================================================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        booking_count = cursor.fetchone()[0]

        if booking_count > 0:

            print(
                "Cannot Delete Passenger!"
            )

            print(
                "Passenger has existing bookings."
            )

            return

        # ====================================================
        # GET USER ID
        # ====================================================

        cursor.execute(
            """
            SELECT user_id
            FROM passengers
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        user = cursor.fetchone()

        if not user:

            print(
                "User Account Not Found!"
            )
            return

        user_id = user[0]

        # ====================================================
        # CONFIRMATION
        # ====================================================

        confirm = input(
            "Are You Sure You Want To Delete "
            "This Passenger? (Yes/No) : "
        ).strip().lower()

        if confirm != "yes":

            print(
                "Delete Operation Cancelled."
            )
            return

        # ====================================================
        # DELETE PASSENGER
        # ====================================================

        cursor.execute(
            """
            DELETE FROM passengers
            WHERE passenger_id=?
            """,
            (passenger_id,)
        )

        # ====================================================
        # DELETE USER
        # ====================================================

        cursor.execute(
            """
            DELETE FROM users
            WHERE user_id=?
            """,
            (user_id,)
        )

        conn.commit()

        print(
            "Passenger Deleted Successfully!"
        )

        print(
            "Associated User Account Deleted Successfully!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error :",
            e
        )


# ============================================================
# 12. PASSENGER VIEW MENU
# ============================================================

def passenger_view_menu():

    while True:

        heading("VIEW PASSENGERS")

        print(
            "1. View All Passengers"
        )

        print(
            "2. View by Passenger ID"
        )

        print(
            "3. View by Name"
        )

        print(
            "4. View Emergency Information"
        )

        print(
            "5. Back"
        )

        view_choice = input(
            "\nEnter Your Choice : "
        )

        if view_choice == "1":

            view_all_passengers()

        elif view_choice == "2":

            view_passenger_by_id()

        elif view_choice == "3":

            view_passenger_by_name()

        elif view_choice == "4":

            view_emergency_info()

        elif view_choice == "5":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ============================================================
# 13. PASSENGER UPDATE MENU
# ============================================================

def passenger_update_menu():

    while True:

        heading("UPDATE PASSENGER")

        print(
            "1. Update Passenger Details"
        )

        print(
            "2. Update Contact Number"
        )

        print(
            "3. Update Emergency Information"
        )

        print(
            "4. Back"
        )

        update_choice = input(
            "\nEnter Your Choice : "
        )

        if update_choice == "1":

            update_passenger()

        elif update_choice == "2":

            update_contact_number()

        elif update_choice == "3":

            update_emergency_info()

        elif update_choice == "4":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ============================================================
# 14. PASSENGER DELETE MENU
# ============================================================

def passenger_delete_menu():

    while True:

        heading("DELETE PASSENGER")

        print(
            "1. Delete by Passenger ID"
        )

        print(
            "2. Delete by Name"
        )

        print(
            "3. Back"
        )

        delete_choice = input(
            "\nEnter Your Choice : "
        )

        if delete_choice == "1":

            delete_passenger_by_id()

        elif delete_choice == "2":

            delete_passenger_by_name()

        elif delete_choice == "3":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ============================================================
# 15. EMERGENCY INFORMATION MENU
# ============================================================

def emergency_information_menu():

    while True:

        heading("EMERGENCY INFORMATION")

        print(
            "1. Add Emergency Information"
        )

        print(
            "2. View Emergency Information"
        )

        print(
            "3. Update Emergency Information"
        )

        print(
            "4. Back"
        )

        choice = input(
            "\nEnter Your Choice : "
        )

        if choice == "1":

            add_emergency_info()

        elif choice == "2":

            view_emergency_info()

        elif choice == "3":

            update_emergency_info()

        elif choice == "4":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ============================================================
# 16. PASSENGER MANAGEMENT MENU
# ============================================================

def passenger_management():

    while True:

        heading("PASSENGER MANAGEMENT")

        print(
            "1. Add Passenger"
        )

        print(
            "2. View Passengers"
        )

        print(
            "3. Update Passenger"
        )

        print(
            "4. Emergency Information"
        )

        print(
            "5. Delete Passenger"
        )

        print(
            "6. Back"
        )

        choice = input(
            "\nEnter Your Choice : "
        )

        # ====================================================
        # ADD
        # ====================================================

        if choice == "1":

            add_passenger()

        # ====================================================
        # VIEW
        # ====================================================

        elif choice == "2":

            passenger_view_menu()

        # ====================================================
        # UPDATE
        # ====================================================

        elif choice == "3":

            passenger_update_menu()

        # ====================================================
        # EMERGENCY INFORMATION
        # ====================================================

        elif choice == "4":

            emergency_information_menu()

        # ====================================================
        # DELETE
        # ====================================================

        elif choice == "5":

            passenger_delete_menu()

        # ====================================================
        # BACK
        # ====================================================

        elif choice == "6":

            break

        else:

            print(
                "Invalid Choice!"
            )


# ============================================================
# RUN PASSENGER MANAGEMENT
# ============================================================

if __name__ == "__main__":

    try:

        passenger_management()

    finally:

        conn.close()