from database import get_connection

conn = get_connection()
cursor = conn.cursor()

# ---------------- Users ----------------
users = [
    ("admin", "admin123", "admin"),
    ("trupti", "1234", "user"),
    ("jay", "1234", "user"),
    ("pranjal", "1234", "user"),
    ("samiksha", "1234", "user"),
    ("diksha", "1234", "user"),
    ("vedant", "1234", "user"),
    ("sneha", "1234", "user"),
    ("rohan", "1234", "user"),
    ("priya", "1234", "user")
]

cursor.executemany(
    "INSERT INTO users(username, password, role) VALUES(?, ?, ?)",
    users
)

# ---------------- Airlines ----------------
airlines = [
    ("Air India",),
    ("IndiGo",),
    ("SpiceJet",),
    ("Akasa Air",),
    ("Vistara",),
    ("AirAsia India",),
    ("Alliance Air",),
    ("Star Air",),
    ("Go First",),
    ("Emirates",)
]

cursor.executemany(
    "INSERT INTO airlines(airline_name) VALUES(?)",
    airlines
)

# ---------------- Airports ----------------
airports = [
    ("Chhatrapati Shivaji Airport", "Mumbai"),
    ("Pune Airport", "Pune"),
    ("Indira Gandhi Airport", "Delhi"),
    ("Kempegowda Airport", "Bengaluru"),
    ("Rajiv Gandhi Airport", "Hyderabad"),
    ("Chennai Airport", "Chennai"),
    ("Netaji Subhas Airport", "Kolkata"),
    ("Goa Airport", "Goa"),
    ("Ahmedabad Airport", "Ahmedabad"),
    ("Jaipur Airport", "Jaipur")
]

cursor.executemany(
    "INSERT INTO airports(airport_name, city) VALUES(?, ?)",
    airports
)

# ---------------- Flights ----------------
flights = [
    (1, 1, 2, "2026-07-15", "09:00", 4500, 120),
    (2, 2, 3, "2026-07-16", "10:30", 5200, 100),
    (3, 3, 4, "2026-07-17", "08:15", 6000, 90),
    (4, 4, 5, "2026-07-18", "12:00", 4800, 110),
    (5, 5, 6, "2026-07-19", "15:00", 5500, 80),
    (6, 6, 7, "2026-07-20", "07:45", 6200, 95),
    (7, 7, 8, "2026-07-21", "13:30", 4300, 105),
    (8, 8, 9, "2026-07-22", "18:20", 5100, 98),
    (9, 9, 10, "2026-07-23", "16:10", 5700, 88),
    (10, 10, 1, "2026-07-24", "11:40", 8900, 140)
]

cursor.executemany("""
INSERT INTO flights(
airline_id,
source_airport_id,
destination_airport_id,
departure_date,
departure_time,
fare,
available_seats
)
VALUES(?, ?, ?, ?, ?, ?, ?)
""", flights)

# ---------------- Passengers ----------------
passengers = [
    ("Amit Sharma", 28, "Male", "9876543210"),
    ("Priya Patil", 24, "Female", "9876543211"),
    ("Rahul Joshi", 35, "Male", "9876543212"),
    ("Sneha Kulkarni", 30, "Female", "9876543213"),
    ("Rohan Deshmukh", 27, "Male", "9876543214"),
    ("Neha Pawar", 32, "Female", "9876543215"),
    ("Kiran More", 40, "Male", "9876543216"),
    ("Pooja Jadhav", 22, "Female", "9876543217"),
    ("Sagar Shinde", 29, "Male", "9876543218"),
    ("Anjali Kale", 26, "Female", "9876543219")
]

cursor.executemany("""
INSERT INTO passengers(
passenger_name,
age,
gender,
phone
)
VALUES(?, ?, ?, ?)
""", passengers)

# ---------------- Bookings ----------------
bookings = [
    (1, 1, "2026-07-10", "A1", "Confirmed"),
    (2, 2, "2026-07-10", "A2", "Confirmed"),
    (3, 3, "2026-07-11", "B1", "Confirmed"),
    (4, 4, "2026-07-11", "B2", "Cancelled"),
    (5, 5, "2026-07-12", "C1", "Confirmed"),
    (6, 6, "2026-07-12", "C2", "Confirmed"),
    (7, 7, "2026-07-13", "D1", "Confirmed"),
    (8, 8, "2026-07-13", "D2", "Cancelled"),
    (9, 9, "2026-07-14", "E1", "Confirmed"),
    (10, 10, "2026-07-14", "E2", "Confirmed")
]

cursor.executemany("""
INSERT INTO bookings(
passenger_id,
flight_id,
booking_date,
seat_no,
status
)
VALUES(?, ?, ?, ?, ?)
""", bookings)
# ---------------- Payments ----------------
payments = [
    (1, 4500, "UPI", "Success", "2026-07-10"),
    (2, 5200, "Card", "Success", "2026-07-10"),
    (3, 6000, "Net Banking", "Success", "2026-07-11"),
    (4, 4800, "UPI", "Failed", "2026-07-11"),
    (5, 5500, "Card", "Success", "2026-07-12"),
    (6, 6200, "UPI", "Success", "2026-07-12"),
    (7, 4300, "Card", "Success", "2026-07-13"),
    (8, 5100, "UPI", "Refund", "2026-07-13"),
    (9, 5700, "Net Banking", "Success", "2026-07-14"),
    (10, 8900, "Card", "Success", "2026-07-14")
]

cursor.executemany("""
INSERT INTO payments(
booking_id,
amount,
payment_method,
payment_status,
payment_date
)
VALUES (?, ?, ?, ?, ?)
""", payments)

conn.commit()

# ---------------- Tickets ----------------
tickets = [
    (1, "PNR100001"),
    (2, "PNR100002"),
    (3, "PNR100003"),
    (4, "PNR100004"),
    (5, "PNR100005"),
    (6, "PNR100006"),
    (7, "PNR100007"),
    (8, "PNR100008"),
    (9, "PNR100009"),
    (10, "PNR100010")
]

cursor.executemany("""
INSERT INTO tickets(
booking_id,
pnr_no
)
VALUES(?, ?)
""", tickets)

conn.commit()
conn.close()

print("Sample data inserted successfully.")