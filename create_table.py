from database import get_connection

conn = get_connection()
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Airlines Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS airlines(
    airline_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airline_name TEXT NOT NULL
)
""")

# Airports Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS airports(
    airport_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airport_name TEXT NOT NULL,
    city TEXT NOT NULL
)
""")

# Flights Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS flights(
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airline_id INTEGER,
    source_airport_id INTEGER,
    destination_airport_id INTEGER,
    departure_date TEXT,
    departure_time TEXT,
    fare REAL,
    available_seats INTEGER,

    FOREIGN KEY(airline_id) REFERENCES airlines(airline_id),
    FOREIGN KEY(source_airport_id) REFERENCES airports(airport_id),
    FOREIGN KEY(destination_airport_id) REFERENCES airports(airport_id)
)
""")

# Passengers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS passengers(
    passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    phone TEXT
)
""")

# Bookings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_id INTEGER,
    flight_id INTEGER,
    booking_date TEXT,
    seat_no TEXT,
    status TEXT,

    FOREIGN KEY(passenger_id) REFERENCES passengers(passenger_id),
    FOREIGN KEY(flight_id) REFERENCES flights(flight_id)
)
""")

# Payments Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments(
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    amount REAL,
    payment_method TEXT,
    payment_status TEXT,
    FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
)
""")
cursor.execute("""
ALTER TABLE payments
ADD COLUMN payment_date TEXT
""")
conn.commit()

# Tickets Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    pnr_no TEXT UNIQUE,

    FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
)
""")

conn.commit()
conn.close()

print("Database and all tables created successfully.")