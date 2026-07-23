from database import get_connection
from datetime import datetime, timedelta


# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = get_connection()
cursor = conn.cursor()

# Enable Foreign Keys
cursor.execute("PRAGMA foreign_keys = ON")


try:

    # ========================================================
    # 1. INSERT USERS
    # ========================================================

    users = [
        ("admin", "admin123", "admin@gmail.com", "9876543210", "admin"),

        ("trupti", "trupti123", "shared@gmail.com", "9876543211", "user"),
        ("jay", "jay12345", "shared@gmail.com", "9876543212", "user"),
        ("pranjal", "pranjal123", "pranjal@gmail.com", "9876543213", "user"),
        ("samiksha", "samiksha123", "samiksha@gmail.com", "9876543214", "user"),
        ("diksha", "diksha123", "diksha@gmail.com", "9876543215", "user"),
        ("vedant", "vedant123", "vedant@gmail.com", "9876543216", "user"),
        ("sneha", "sneha123", "sneha@gmail.com", "9876543217", "user"),
        ("rahul", "rahul123", "rahul@gmail.com", "9876543218", "user"),
        ("priya", "priya123", "priya@gmail.com", "9876543219", "user"),
        ("amit", "amit123", "amit@gmail.com", "9876543220", "user"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO users
        (
            username,
            password,
            email,
            contact_no,
            role
        )
        VALUES (?, ?, ?, ?, ?)
    """, users)


    # ========================================================
    # 2. INSERT AIRLINES
    # ========================================================

    airlines = [
        ("Air India",),
        ("IndiGo",),
        ("Vistara",),
        ("Akasa Air",),
        ("SpiceJet",),
        ("Go First",),
        ("Air India Express",),
        ("Alliance Air",),
        ("Emirates",),
        ("Qatar Airways",),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO airlines
        (
            airline_name
        )
        VALUES (?)
    """, airlines)


    # ========================================================
    # 3. INSERT AIRPORTS
    # ========================================================

    airports = [
        ("Chhatrapati Shivaji Maharaj International Airport", "Mumbai"),
        ("Pune International Airport", "Pune"),
        ("Indira Gandhi International Airport", "Delhi"),
        ("Kempegowda International Airport", "Bengaluru"),
        ("Rajiv Gandhi International Airport", "Hyderabad"),
        ("Chennai International Airport", "Chennai"),
        ("Netaji Subhas Chandra Bose International Airport", "Kolkata"),
        ("Sardar Vallabhbhai Patel International Airport", "Ahmedabad"),
        ("Goa International Airport", "Goa"),
        ("Cochin International Airport", "Kochi"),
        ("Dubai International Airport", "Dubai"),
        ("Hamad International Airport", "Doha"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO airports
        (
            airport_name,
            city
        )
        VALUES (?, ?)
    """, airports)


    # ========================================================
    # 4. INSERT FLIGHTS
    # ========================================================

    flights = [
        (
            "AI101",
            1,
            1,
            3,
            "2026-08-01",
            "06:30",
            5500,
            30,
            30
        ),

        (
            "6E202",
            2,
            2,
            1,
            "2026-08-02",
            "08:00",
            4500,
            40,
            40
        ),

        (
            "UK303",
            3,
            3,
            4,
            "2026-08-03",
            "10:15",
            6500,
            35,
            35
        ),

        (
            "QP404",
            4,
            4,
            5,
            "2026-08-04",
            "12:30",
            5000,
            25,
            25
        ),

        (
            "SG505",
            5,
            5,
            6,
            "2026-08-05",
            "14:45",
            4800,
            30,
            30
        ),

        (
            "G8106",
            6,
            6,
            7,
            "2026-08-06",
            "16:00",
            5200,
            35,
            35
        ),

        (
            "IX707",
            7,
            7,
            8,
            "2026-08-07",
            "18:15",
            4300,
            30,
            30
        ),

        (
            "9I808",
            8,
            8,
            9,
            "2026-08-08",
            "19:30",
            4000,
            20,
            20
        ),

        (
            "EK909",
            9,
            9,
            11,
            "2026-08-09",
            "21:00",
            25000,
            50,
            50
        ),

        (
            "QR010",
            10,
            10,
            12,
            "2026-08-10",
            "23:00",
            30000,
            50,
            50
        ),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO flights
        (
            flight_number,
            airline_id,
            source_airport_id,
            destination_airport_id,
            departure_date,
            departure_time,
            fare,
            total_seats,
            available_seats
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, flights)


    # ========================================================
    # 5. INSERT PASSENGERS
    # ========================================================

    # Get user IDs
    cursor.execute("""
        SELECT user_id, username
        FROM users
        ORDER BY user_id
    """)

    user_rows = cursor.fetchall()

    passengers = []

    passenger_details = [
        ("Trupti Shitole", 18, "Female", "9876500001", "shared@gmail.com"),
        ("Jay Patil", 20, "Male", "9876500002", "shared@gmail.com"),
        ("Pranjal Bochar", 19, "Female", "9876500003", "pranjal@gmail.com"),
        ("Samiksha Kokate", 20, "Female", "9876500004", "samiksha@gmail.com"),
        ("Diksha Wawale", 19, "Female", "9876500005", "diksha@gmail.com"),
        ("Vedant Gaikwad", 21, "Male", "9876500006", "vedant@gmail.com"),
        ("Sneha Jadhav", 20, "Female", "9876500007", "sneha@gmail.com"),
        ("Rahul Sharma", 25, "Male", "9876500008", "rahul@gmail.com"),
        ("Priya Patil", 23, "Female", "9876500009", "priya@gmail.com"),
        ("Amit Kulkarni", 30, "Male", "9876500010", "amit@gmail.com"),
    ]

    # Skip admin user
    user_rows = [
        row for row in user_rows
        if row[1].lower() != "admin"
    ]

    for i, user in enumerate(user_rows[:10]):

        passengers.append(
            (
                user[0],
                passenger_details[i][0],
                passenger_details[i][1],
                passenger_details[i][2],
                passenger_details[i][3],
                passenger_details[i][4]
            )
        )

    cursor.executemany("""
        INSERT OR IGNORE INTO passengers
        (
            user_id,
            passenger_name,
            age,
            gender,
            phone,
            email
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, passengers)


    # ========================================================
    # 6. INSERT PASSENGER EMERGENCY INFORMATION
    # ========================================================

    emergency_data = [
        ("O+",
         "Suresh Shitole",
         "9000000001",
         "Father"),

        ("A+",
         "Ramesh Patil",
         "9000000002",
         "Father"),

        ("B+",
         "Sunita Bochar",
         "9000000003",
         "Mother"),

        ("O-",
         "Kiran Kokate",
         "9000000004",
         "Father"),

        ("AB+",
         "Mahesh Wawale",
         "9000000005",
         "Father"),

        ("A-",
         "Vijay Gaikwad",
         "9000000006",
         "Father"),

        ("B-",
         "Meena Jadhav",
         "9000000007",
         "Mother"),

        ("O+",
         "Rajesh Sharma",
         "9000000008",
         "Brother"),

        ("A+",
         "Sunil Patil",
         "9000000009",
         "Father"),

        ("B+",
         "Anil Kulkarni",
         "9000000010",
         "Brother"),
    ]

    cursor.execute("""
        SELECT passenger_id
        FROM passengers
        ORDER BY passenger_id
        LIMIT 10
    """)

    passenger_rows = cursor.fetchall()

    emergency_records = []

    for i, passenger in enumerate(passenger_rows):

        emergency_records.append(
            (
                passenger[0],
                emergency_data[i][0],
                emergency_data[i][1],
                emergency_data[i][2],
                emergency_data[i][3]
            )
        )

    cursor.executemany("""
        INSERT OR IGNORE INTO passenger_emergency_info
        (
            passenger_id,
            blood_group,
            emergency_contact_name,
            emergency_contact_no,
            relationship
        )
        VALUES (?, ?, ?, ?, ?)
    """, emergency_records)


    # ========================================================
    # 7. INSERT SEATS
    # ========================================================

    # We create 10 seats for each flight.
    # This gives you 100 seats to test Booking Management.

    seat_records = []

    seat_numbers = [
        ("A1", "Economy", "Window"),
        ("A2", "Economy", "Middle"),
        ("A3", "Economy", "Aisle"),

        ("B1", "Premium Economy", "Window"),
        ("B2", "Premium Economy", "Middle"),
        ("B3", "Premium Economy", "Aisle"),

        ("C1", "Business", "Window"),
        ("C2", "Business", "Middle"),
        ("C3", "Business", "Aisle"),

        ("D1", "First Class", "Window"),
    ]

    # Get all flights
    cursor.execute("""
        SELECT flight_id
        FROM flights
        ORDER BY flight_id
    """)

    flight_rows = cursor.fetchall()

    for flight in flight_rows:

        flight_id = flight[0]

        for seat_no, seat_class, seat_type in seat_numbers:

            seat_records.append(
                (
                    flight_id,
                    seat_no,
                    seat_class,
                    seat_type,
                    "Available"
                )
            )

    cursor.executemany("""
        INSERT OR IGNORE INTO seats
        (
            flight_id,
            seat_no,
            seat_class,
            seat_type,
            seat_status
        )
        VALUES (?, ?, ?, ?, ?)
    """, seat_records)


    # ========================================================
    # 8. INSERT BOOKINGS
    # ========================================================

    # Get passengers
    cursor.execute("""
        SELECT passenger_id
        FROM passengers
        ORDER BY passenger_id
        LIMIT 10
    """)

    passenger_rows = cursor.fetchall()

    # Get available seats
    cursor.execute("""
        SELECT seat_id, flight_id
        FROM seats
        WHERE seat_status = 'Available'
        ORDER BY seat_id
        LIMIT 10
    """)

    seat_rows = cursor.fetchall()

    booking_records = []

    for i in range(10):

        passenger_id = passenger_rows[i][0]

        seat_id = seat_rows[i][0]

        flight_id = seat_rows[i][1]

        booking_date = (
            datetime.now() -
            timedelta(days=10 - i)
        ).strftime("%Y-%m-%d %H:%M:%S")

        booking_records.append(
            (
                passenger_id,
                flight_id,
                seat_id,
                booking_date,
                "Confirmed"
            )
        )

    cursor.executemany("""
        INSERT OR IGNORE INTO bookings
        (
            passenger_id,
            flight_id,
            seat_id,
            booking_date,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, booking_records)


    # ========================================================
    # UPDATE BOOKED SEATS
    # ========================================================

    for seat in seat_rows:

        cursor.execute("""
            UPDATE seats
            SET seat_status = 'Booked'
            WHERE seat_id = ?
        """, (seat[0],))


    # ========================================================
    # UPDATE AVAILABLE SEATS
    # ========================================================

    for flight in flight_rows:

        flight_id = flight[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM seats
            WHERE flight_id = ?
            AND seat_status = 'Available'
        """, (flight_id,))

        available_seats = cursor.fetchone()[0]

        cursor.execute("""
            UPDATE flights
            SET available_seats = ?
            WHERE flight_id = ?
        """, (
            available_seats,
            flight_id
        ))


    # ========================================================
    # 9. INSERT PAYMENTS
    # ========================================================

    cursor.execute("""
        SELECT
            booking_id,
            flight_id
        FROM bookings
        ORDER BY booking_id
        LIMIT 10
    """)

    booking_rows = cursor.fetchall()

    payment_methods = [
        "UPI",
        "Card",
        "Net Banking",
        "UPI",
        "Card",
        "Net Banking",
        "UPI",
        "Card",
        "Net Banking",
        "UPI"
    ]

    payment_records = []

    for i, booking in enumerate(booking_rows):

        booking_id = booking[0]

        flight_id = booking[1]

        # Get flight fare
        cursor.execute("""
            SELECT fare
            FROM flights
            WHERE flight_id = ?
        """, (flight_id,))

        fare_row = cursor.fetchone()

        base_amount = float(fare_row[0])

        gst_percentage = 5.0

        gst_amount = round(
            base_amount *
            gst_percentage /
            100,
            2
        )

        total_amount = round(
            base_amount +
            gst_amount,
            2
        )

        payment_date = (
            datetime.now() -
            timedelta(days=9 - i)
        ).strftime("%Y-%m-%d %H:%M:%S")

        payment_records.append(
            (
                booking_id,
                base_amount,
                gst_percentage,
                gst_amount,
                total_amount,
                payment_methods[i],
                "Successful",
                payment_date,
                0,
                None,
                "Not Applicable"
            )
        )

    cursor.executemany("""
        INSERT OR IGNORE INTO payments
        (
            booking_id,
            base_amount,
            gst_percentage,
            gst_amount,
            total_amount,
            payment_method,
            payment_status,
            payment_date,
            refund_amount,
            refund_date,
            refund_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, payment_records)


    # ========================================================
    # 10. INSERT TICKETS
    # ========================================================

    cursor.execute("""
        SELECT booking_id
        FROM bookings
        ORDER BY booking_id
        LIMIT 10
    """)

    booking_rows = cursor.fetchall()

    ticket_records = []

    for i, booking in enumerate(booking_rows):

        booking_id = booking[0]

        pnr = f"PNR{i + 1:03d}2026"

        issue_date = (
            datetime.now() -
            timedelta(days=8 - i)
        ).strftime("%Y-%m-%d %H:%M:%S")

        ticket_records.append(
            (
                booking_id,
                pnr,
                issue_date,
                "Active"
            )
        )

    cursor.executemany("""
        INSERT OR IGNORE INTO tickets
        (
            booking_id,
            pnr_no,
            issue_date,
            ticket_status
        )
        VALUES (?, ?, ?, ?)
    """, ticket_records)


    # ========================================================
    # 11. INSERT REVIEWS
    # ========================================================

    review_records = [

        (2, 1, 5,
         "Excellent flight experience.",
         "2026-08-05"),

        (3, 2, 4,
         "Good service and comfortable journey.",
         "2026-08-06"),

        (4, 3, 5,
         "Very good flight experience.",
         "2026-08-07"),

        (5, 4, 3,
         "Average service.",
         "2026-08-08"),

        (6, 5, 4,
         "Good staff and clean aircraft.",
         "2026-08-09"),

        (7, 6, 5,
         "Very comfortable journey.",
         "2026-08-10"),

        (8, 7, 3,
         "Flight was delayed but overall good.",
         "2026-08-11"),

        (9, 8, 4,
         "Good overall experience.",
         "2026-08-12"),

        (10, 9, 5,
         "Excellent international flight.",
         "2026-08-13"),

        (11, 10, 5,
         "Amazing service and experience.",
         "2026-08-14"),
    ]

    cursor.executemany("""
        INSERT INTO reviews
        (
            user_id,
            flight_id,
            rating,
            review_text,
            review_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, review_records)


    # ========================================================
    # COMMIT ALL DATA
    # ========================================================

    conn.commit()


    print()
    print("=" * 60)
    print("       SAMPLE DATA INSERTED SUCCESSFULLY")
    print("=" * 60)
    print()
    print("Users                  : 11")
    print("Airlines               : 10")
    print("Airports               : 12")
    print("Flights                : 10")
    print("Passengers             : 10")
    print("Emergency Information  : 10")
    print("Seats                  : 100")
    print("Bookings               : 10")
    print("Payments               : 10")
    print("Tickets                : 10")
    print("Reviews                : 10")
    print()
    print("You can now test all project modules.")
    print("=" * 60)


except Exception as e:

    conn.rollback()

    print()
    print("Error while inserting data:")
    print(e)


finally:

    conn.close()