from database import get_connection

conn = get_connection()
cursor = conn.cursor()

try:

    # Add total class seat columns
    cursor.execute("""
        ALTER TABLE flights
        ADD COLUMN economy_seats INTEGER NOT NULL DEFAULT 0
    """)

    cursor.execute("""
        ALTER TABLE flights
        ADD COLUMN premium_economy_seats INTEGER NOT NULL DEFAULT 0
    """)

    cursor.execute("""
        ALTER TABLE flights
        ADD COLUMN business_seats INTEGER NOT NULL DEFAULT 0
    """)

    # Add available class seat columns
    cursor.execute("""
        ALTER TABLE flights
        ADD COLUMN available_economy_seats INTEGER NOT NULL DEFAULT 0
    """)

    cursor.execute("""
        ALTER TABLE flights
        ADD COLUMN available_premium_economy_seats
        INTEGER NOT NULL DEFAULT 0
    """)

    cursor.execute("""
        ALTER TABLE flights
        ADD COLUMN available_business_seats
        INTEGER NOT NULL DEFAULT 0
    """)

    conn.commit()

    print("Flights table updated successfully!")

except Exception as e:

    conn.rollback()

    print("Database Error:", e)

finally:

    conn.close()