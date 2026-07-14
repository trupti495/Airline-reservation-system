from database import get_connection
from getpass import getpass
from rich.console import Console

console = Console()

def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()
conn = get_connection()
cursor = conn.cursor()

# ==========================================
# 1.1 Register User
# ==========================================
def register_user():

    heading("USER REGISTRATION")

    try:
        # ---------------- Username ----------------
        username = input("Enter Username : ").strip()

        if username == "":
            print("Username cannot be empty.")
            return

        # Check if username already exists
        cursor.execute("""
            SELECT 1
            FROM users
            WHERE LOWER(username) = LOWER(?)
        """, (username,))

        if cursor.fetchone():
            print("Username already exists. Please choose another username.")
            return

        # ---------------- Password ----------------
        password = getpass("Enter Password : ").strip()

        if password == "":
            print("Password cannot be empty.")
            return

        if len(password) < 6:
            print("Password must contain at least 6 characters.")
            return

        # ---------------- Passenger Details ----------------
        print("\nEnter Passenger Details")

        age = int(input("Age : "))

        if age <= 0:
            print("Invalid Age.")
            return

        gender = input("Gender (Male/Female/Other) : ").strip().title()

        if gender not in ["Male", "Female", "Other"]:
            print("Invalid Gender.")
            return

        phone = input("Phone Number : ").strip()

        if not phone.isdigit() or len(phone) != 10:
            print("Phone Number must contain exactly 10 digits.")
            return

        email = input("Email Address : ").strip()


        # ---------------- Insert into Users ----------------
        role = "user"

        cursor.execute("""
            INSERT INTO users(username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))

        # ---------------- Insert into Passengers ----------------
        cursor.execute("""
    INSERT INTO passengers
    (
        passenger_name,
        age,
        gender,
        phone
    )
    VALUES (?, ?, ?, ?)
""", (
    username,
    age,
    gender,
    phone,
))
        conn.commit()

        passenger_id = cursor.lastrowid

        heading("REGISTRATION SUCCESSFUL")

        print("User Account Created Successfully.")
        print("Username       :", username)
        print("Passenger ID   :", passenger_id)
        print("Please save your Passenger ID for future bookings.")

    except ValueError:
        print("Please enter valid numeric values.")

    except Exception as e:
        conn.rollback()
        print("Error :", e)


# ==========================================
# 1.2 Login Menu
# ==========================================
def login():

    while True:

        heading("LOGIN")

        print("1. Login as Admin")
        print("2. Login as User")
        print("3. Back")

        try:
            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    return login_admin()

                case 2:
                    return login_user()

                case 3:
                    return None

                case _:
                    print("Invalid Choice.")

        except ValueError:
            print("Enter numeric choice only.")

# ==========================================
# 1.2.1 Login as Admin
# ==========================================
def login_admin():
    heading("ADMIN LOGIN")

    username = input("Enter Username : ")
    password = getpass("Enter Password : ")

    cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=? AND LOWER(role)='admin'
    """, (username, password))

    row = cursor.fetchone()

    if row:
        print("Admin Login Successful.")
        return "admin"

    print("Invalid Username or Password.")
    return None
# ==========================================
# 1.2.2 Login as User
# ==========================================
def login_user():
    heading("USER LOGIN")

    username = input("Enter Username : ")
    password = getpass("Enter Password : ")

    # Check user login
    cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ? AND password = ? AND LOWER(role) = 'user'
    """, (username, password))

    user = cursor.fetchone()

    if user:

        # Fetch Passenger ID
        cursor.execute("""
        SELECT passenger_id
        FROM passengers
        WHERE LOWER(passenger_name) = LOWER(?)
        """, (username,))

        passenger = cursor.fetchone()

        print("\n====================================")
        print("     USER LOGIN SUCCESSFUL")
        print("====================================")

        if passenger:
            print("Your Passenger ID :", passenger[0])
            print("Please keep this Passenger ID for booking tickets.")
            return "user"
        else:
            print("Passenger record not found.")

        print("====================================\n")

        return None

    else:
        print("Invalid Username or Password.")
        return None
# ==========================================
# 1.3 Logout
# ==========================================
def logout():
    heading("LOGOUT")
    print("Logout Successful.")

