import random
from database import get_connection

from rich.console import Console
from colorama import init

console = Console()
init(autoreset=True)

def heading(title):
    print()
    console.rule(f"[bold cyan]{title}[/bold cyan]", style="bright_white")
    print()

conn = get_connection()
cursor = conn.cursor()

def forgot_password():

    heading("FORGOT PASSWORD")

    username = input("Enter Username : ")

    # Check whether username exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user is None:
        print(" Username not found!")
        return

    contact_no = input("Enter Registered Contact Number : ")

    otp = random.randint(100000, 999999)

    print("\nOTP Sent Successfully!")
    print("Your OTP is :", otp)      # Demo OTP

    entered_otp = input("Enter OTP : ")

    if entered_otp == str(otp):

        new_password = input("Enter New Password : ")
        confirm_password = input("Confirm New Password : ")

        if new_password == confirm_password:

            cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE username = ? 
            """, (new_password, username))
            conn.commit()

            print("\nPassword Changed Successfully!")

        else:
            print("\nPasswords do not match!")

    else:
        print("\n Invalid OTP!")