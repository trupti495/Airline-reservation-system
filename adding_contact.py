from database import get_connection
conn = get_connection()
cursor = conn.cursor()
import sqlite3
conn = sqlite3.connect("airline.db")
cursor = conn.cursor()
try:
    cursor.execute("""
    ALTER TABLE flights
    ADD COLUMN total_seats INTEGER
    """)
    conn.commit()
    print("total_seats column added successfully.")

    cursor.execute("""
    ALTER TABLE users
    ADD COLUMN contact_no TEXT
    """)
    conn.commit()
    print("contact_no column added successfully.")

except sqlite3.OperationalError as e:
    print(e)

finally:
    
 conn.commit()

