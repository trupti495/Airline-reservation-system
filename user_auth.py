from database import get_connection
from getpass import getpass

conn = get_connection()
cursor = conn.cursor()

# ==========================================
# 1.1 Register User
# ==========================================
def register_user():
    print("\n========== REGISTER USER ==========")

    try:
        username = input("Enter Username : ")
        if username == "":
            print("Username cannot be empty.")
            return

        password = getpass("Enter Password : ")
        if password == "":
            print("Password cannot be empty.")
            return

        print("\nSelect Role")
        print("1. Admin")
        print("2. User")

        ch = int(input("Enter Choice : "))

        match ch:
            case 1:
                role = "admin"
            case 2:
                role = "user"
            case _:
                print("Invalid Role.")
                return

        cursor.execute(
            """
            INSERT INTO users(username, password, role)
            VALUES(?, ?, ?)
            """,
            (username, password, role)
        )
        conn.commit()
        print("Registration Successful.")

    except ValueError:
        print("Enter numeric choice only.")
    except Exception as e:
        print("Error :", e)


# ==========================================
# 1.2 Login Menu
# ==========================================
def login():

    while True:

        print("\n========== LOGIN ==========")
        print("1. Login as Admin")
        print("2. Login as User")
        print("3. Back")

        try:
            ch = int(input("Enter Choice : "))

            match ch:

                case 1:
                    login_admin()

                case 2:
                    login_user()

                case 3:
                    break

                case _:
                    print("Invalid Choice.")

        except ValueError:
            print("Enter numeric choice only.")


# ==========================================
# 1.2.1 Login as Admin
# ==========================================
def login_admin():
    print("\n========== ADMIN LOGIN ==========")

    try:
        username = input("Enter Username : ")
        password = getpass("Enter Password : ")

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=? AND LOWER(role)='admin'
            """,
            (username, password)
        )

        row = cursor.fetchone()

        if row:
            print("Admin Login Successful.")
        else:
            print("Invalid Username or Password.")

    except Exception as e:
        print("Error :", e)


# ==========================================
# 1.2.2 Login as User
# ==========================================
def login_user():
    print("\n========== USER LOGIN ==========")

    try:
        username = input("Enter Username : ")
        password = getpass("Enter Password : ")

        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=? AND LOWER(role)='user'
            """,
            (username, password)
        )

        row = cursor.fetchone()

        if row:
            print("User Login Successful.")
        else:
            print("Invalid Username or Password.")

    except Exception as e:
        print("Error :", e)


# ==========================================
# 1.3 Logout
# ==========================================
def logout():
    print("\nLogout Successful.")

