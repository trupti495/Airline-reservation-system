from database import get_connection
import random
import smtplib
import time
from rich.console import Console
from email.message import EmailMessage
console = Console()

def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()

# heading(), send_otp(), forgot_password()
def send_otp(receiver_email, otp):

    sender_email = "shitoletrupti6@gmail.com"
    app_password = "hyjspiqilotmban"

    msg = EmailMessage()
    msg["Subject"] = "Password Reset OTP"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(f"""
Hello,

Your OTP for password reset is:

{otp}

This OTP is valid for 2 minutes.

Do not share this OTP with anyone.

Thank You.
Airline Reservation System
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)    

def forgot_password():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        heading("FORGOT PASSWORD")

        username = input("Enter Username : ").strip()

        # Check username
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            print("Username not found!")
            return

        # Ask email
        receiver_email = input("Enter Your Gmail Address : ").strip()

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        try:
            send_otp(receiver_email, otp)
            print("\nOTP has been sent to your Gmail.")

        except Exception as e:
            print("Failed to send OTP.")
            print(e)
            return

        otp_time = time.time()
        attempts = 3

        while attempts > 0:

            # OTP Expiry (2 minutes)
            if time.time() - otp_time > 120:
                print("\nOTP Expired!")
                return

            entered_otp = input("Enter OTP : ").strip()

            if entered_otp == otp:

                new_password = input("Enter New Password : ").strip()
                confirm_password = input("Confirm New Password : ").strip()

                if new_password != confirm_password:
                    print("Passwords do not match!")
                    return

                cursor.execute("""
                    UPDATE users
                    SET password = ?
                    WHERE username = ?
                """, (new_password, username))

                conn.commit()

                print("\nPassword Changed Successfully!")
                return

            attempts -= 1

            if attempts > 0:
                print(f"Invalid OTP! {attempts} attempt(s) remaining.")

        print("\nMaximum OTP attempts exceeded.")

    except Exception as e:
        conn.rollback()
        print("Error :", e)

    finally:
        cursor.close()
        conn.close()