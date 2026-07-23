from database import get_connection


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = get_connection()
cursor = conn.cursor()

# Enable Foreign Key Support
cursor.execute("PRAGMA foreign_keys = ON")


try:

    # ========================================================
    # 1. USERS TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        email TEXT NOT NULL,

        contact_no TEXT,

        role TEXT NOT NULL
    )
    """)


    # ========================================================
    # 2. AIRLINES TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airlines(
        airline_id INTEGER PRIMARY KEY AUTOINCREMENT,

        airline_name TEXT UNIQUE NOT NULL
    )
    """)


    # ========================================================
    # 3. AIRPORTS TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airports(
        airport_id INTEGER PRIMARY KEY AUTOINCREMENT,

        airport_name TEXT NOT NULL,

        city TEXT NOT NULL
    )
    """)


        # ========================================================
    # 4. FLIGHTS TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights(
        flight_id INTEGER PRIMARY KEY AUTOINCREMENT,

        flight_number TEXT UNIQUE NOT NULL,

        airline_id INTEGER NOT NULL,

        source_airport_id INTEGER NOT NULL,

        destination_airport_id INTEGER NOT NULL,

        departure_date TEXT NOT NULL,

        departure_time TEXT NOT NULL,

        fare REAL NOT NULL,

        -- TOTAL SEATS
        total_seats INTEGER NOT NULL,

        -- SEATS BY CLASS
        economy_seats INTEGER NOT NULL DEFAULT 0,

        premium_economy_seats INTEGER NOT NULL DEFAULT 0,

        business_seats INTEGER NOT NULL DEFAULT 0,

        -- TOTAL AVAILABLE SEATS
        available_seats INTEGER NOT NULL,

        -- AVAILABLE SEATS BY CLASS
        available_economy_seats INTEGER NOT NULL DEFAULT 0,

        available_premium_economy_seats INTEGER NOT NULL DEFAULT 0,

        available_business_seats INTEGER NOT NULL DEFAULT 0,

        FOREIGN KEY(airline_id)
            REFERENCES airlines(airline_id),

        FOREIGN KEY(source_airport_id)
            REFERENCES airports(airport_id),

        FOREIGN KEY(destination_airport_id)
            REFERENCES airports(airport_id),

        CHECK(total_seats > 0),

        CHECK(economy_seats >= 0),

        CHECK(premium_economy_seats >= 0),

        CHECK(business_seats >= 0),

        CHECK(available_seats >= 0),

        CHECK(available_economy_seats >= 0),

        CHECK(available_premium_economy_seats >= 0),

        CHECK(available_business_seats >= 0),

        CHECK(available_seats <= total_seats),

        CHECK(
            available_economy_seats <= economy_seats
        ),

        CHECK(
            available_premium_economy_seats
            <= premium_economy_seats
        ),

        CHECK(
            available_business_seats
            <= business_seats
        ),

        CHECK(
            source_airport_id != destination_airport_id
        )
    )
    """)

    # ========================================================
    # 7. SEATS TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS seats(
        seat_id INTEGER PRIMARY KEY AUTOINCREMENT,

        flight_id INTEGER NOT NULL,

        seat_no TEXT NOT NULL,

        seat_class TEXT NOT NULL,

        seat_type TEXT,

        seat_status TEXT NOT NULL DEFAULT 'Available',

        FOREIGN KEY(flight_id)
            REFERENCES flights(flight_id)
            ON DELETE CASCADE,

        UNIQUE(flight_id, seat_no),

        CHECK(seat_class IN (
            'Economy',
            'Premium Economy',
            'Business',
            'First Class'
        )),

        CHECK(seat_type IN (
            'Window',
            'Middle',
            'Aisle'
        )),

        CHECK(seat_status IN (
            'Available',
            'Booked'
        ))
    )
    """)


    # ========================================================
    # 8. BOOKINGS TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,

        passenger_id INTEGER NOT NULL,

        flight_id INTEGER NOT NULL,

        seat_id INTEGER NOT NULL,

        booking_date TEXT NOT NULL,

        status TEXT NOT NULL DEFAULT 'Confirmed',

        cancellation_reason TEXT,

        FOREIGN KEY(passenger_id)
            REFERENCES passengers(passenger_id),

        FOREIGN KEY(flight_id)
            REFERENCES flights(flight_id),

        FOREIGN KEY(seat_id)
            REFERENCES seats(seat_id),

        CHECK(status IN (
            'Confirmed',
            'Cancelled'
        )),

        UNIQUE(flight_id, seat_id)
    )
    """)


    # ========================================================
    # 9. PAYMENTS TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,

        booking_id INTEGER NOT NULL,

        base_amount REAL NOT NULL,

        gst_percentage REAL NOT NULL DEFAULT 5,

        gst_amount REAL NOT NULL,

        total_amount REAL NOT NULL,

        payment_method TEXT NOT NULL,

        payment_status TEXT NOT NULL DEFAULT 'Pending',

        payment_date TEXT,

        refund_amount REAL DEFAULT 0,

        refund_date TEXT,

        refund_status TEXT NOT NULL DEFAULT 'Not Applicable',

        FOREIGN KEY(booking_id)
            REFERENCES bookings(booking_id),

        CHECK(base_amount >= 0),

        CHECK(gst_percentage >= 0),

        CHECK(gst_amount >= 0),

        CHECK(total_amount >= 0),

        CHECK(refund_amount >= 0),

        CHECK(refund_amount <= total_amount),

        CHECK(payment_method IN (
            'UPI',
            'Card',
            'Net Banking'
        )),

        CHECK(payment_status IN (
            'Pending',
            'Successful',
            'Failed'
        )),

        CHECK(refund_status IN (
            'Not Applicable',
            'Pending',
            'Successful',
            'Failed'
        ))
    )
    """)


    # ========================================================
    # 10. TICKETS TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,

        booking_id INTEGER UNIQUE NOT NULL,

        pnr_no TEXT UNIQUE NOT NULL,

        issue_date TEXT,

        ticket_status TEXT NOT NULL DEFAULT 'Active',

        FOREIGN KEY(booking_id)
            REFERENCES bookings(booking_id),

        CHECK(ticket_status IN (
            'Active',
            'Cancelled'
        ))
    )
    """)


    # ========================================================
    # 11. REVIEWS TABLE
    # ========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        flight_id INTEGER NOT NULL,

        rating INTEGER NOT NULL,

        review_text TEXT,

        review_date TEXT,

        FOREIGN KEY(user_id)
            REFERENCES users(user_id),

        FOREIGN KEY(flight_id)
            REFERENCES flights(flight_id),

        CHECK(rating >= 1 AND rating <= 5)
    )
    """)


    # ========================================================
    # COMMIT ALL CHANGES
    # ========================================================

    conn.commit()

    print(
        "Database and all 11 tables created successfully."
    )


except Exception as e:

    conn.rollback()

    print(
        "Database Error:",
        e
    )


finally:

    cursor.close()

    conn.close()