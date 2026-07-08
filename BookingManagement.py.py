import sqlite3
from datetime import datetime
from database import get_connection

conn = get_connection()
cursor = conn.cursor()
class BookingManagement:

    def __init__(self):
        self.passenger_id = None
        self.flight_id = None
    # 4.1 Book Ticket
    def book_ticket(self):
        while True:
            print("\n========== BOOK TICKET ==========")
            print("1. Search Passenger")
            print("2. Search Flight")
            print("3. Confirm Booking")
            print("4. Back")
            ch = int(input("Enter your choice: "))
            match ch:
                case 1:
                    self.search_passenger()
                case 2:
                    self.search_flight()
                case 3:
                    self.confirm_booking()
                case 4:
                    break
                case _:
                    print("Invalid Choice")



    # 4.1.1 Search Passenger
    def search_passenger(self):

         print("\n===== SEARCH PASSENGER =====")
         pid = int(input("Enter Passenger ID: "))
         if pid == "":
            print("Passenger ID cannot be empty")
            return
         cursor.execute(
            "SELECT * FROM passengers WHERE passenger_id=?",
            (pid,)
        )
         passenger = cursor.fetchone()
         if passenger:

            print("\nPassenger Found")
            print("----------------")
            print("ID :", passenger[0])
            print("Name :", passenger[1])
            print("Age :", passenger[2])
            print("Gender :", passenger[3])
            print("Phone :", passenger[4])
            self.passenger_id = pid
         else:
            print("Passenger Not Found")

    # 4.1.2 Search Flight
    def search_flight(self):

     print("\n4.1.2 =====Search Flight=====")

     source = input("Enter Source Airport ID: ")
     destination = input("Enter Destination Airport ID: ")
     departure_date = input("Enter Departure Date (YYYY-MM-DD): ")

     cursor.execute("""
        SELECT flight_id, airline_id, source_airport_id,
               destination_airport_id, departure_date,
               departure_time, fare, available_seats
        FROM flights
        WHERE source_airport_id=? 
        AND destination_airport_id=? 
        AND departure_date=?
     """, (source, destination, departure_date))

     flights = cursor.fetchall()

     if not flights:
        print("No Flights Available.")
        return

     print("\n===== AVAILABLE FLIGHTS ======")

     for flight in flights:
        print("----------------------------------------")
        print("Flight ID       :", flight[0])
        print("Airline ID      :", flight[1])
        print("Source Airport  :", flight[2])
        print("Destination     :", flight[3])
        print("Departure Date  :", flight[4])
        print("Departure Time  :", flight[5])
        print("Fare            :", flight[6])
        print("Available Seats :", flight[7])
     fid = input("\nEnter Flight ID to Book: ")

     cursor.execute(
        "SELECT flight_id FROM flights WHERE flight_id=?",
        (fid,)
     )
     flight = cursor.fetchone()
     if flight:
        self.flight_id = fid
        print("Flight Selected Successfully")
     else:
        print("Invalid Flight ID")

    # 4.1.3 Confirm Booking
    def confirm_booking(self):
     print("\n4.1.3 Confirm Booking")
     passenger_id = input("Enter Passenger ID: ")
     cursor.execute(
        "SELECT * FROM passengers WHERE passenger_id=?",
        (passenger_id,)
     )
     if cursor.fetchone() is None:
        print("Passenger ID not found.")
        return

     flight_id = input("Enter Flight ID: ")
     cursor.execute(
        "SELECT * FROM flights WHERE flight_id=?",
        (flight_id,)
     )
     if cursor.fetchone() is None:
        print("Flight ID not found.")
        return
     
     seat_no = input("Enter Seat Number: ")
     cursor.execute(
        """
        SELECT * FROM bookings
        WHERE flight_id=? 
        AND seat_no=? 
        AND status=?
        """,
        (flight_id, seat_no, "Confirmed")
    )
     if cursor.fetchone():
        print("Seat is already booked.")
        return

     booking_date = datetime.now().strftime("%Y-%m-%d")
     cursor.execute(
        """
        INSERT INTO bookings
        (passenger_id, flight_id, seat_no, booking_date, status)
        VALUES(?,?,?,?,?)
        """,
        (passenger_id, flight_id, seat_no, booking_date, "Confirmed")
    )
     cursor.execute(
        """
        UPDATE flights
        SET available_seats = available_seats - 1
        WHERE flight_id=?
        """,
        (flight_id,)
    )
     conn.commit()
     print("Booking Confirmed Successfully")

    # 4.2 VIEW BOOKING
    def view_booking(self):
        print("\n=========== VIEW BOOKING ==========")
        print("1. View All Bookings")
        print("2. View by Booking ID")
        print("3. View by Passenger ID")
        print("4.Back")
        ch = int(input("Enter choice: "))
        match ch:
            case 1:
                self.view_all_bookings()
            case 2:
                self.view_by_booking_id()
            case 3:
                self.view_by_booking_id()    
            
            case _:
                print("Inavalid choice")    


    def view_all_bookings(self):
        print("\n4.2.1 =====View All Bookings=====")
        cursor.execute("SELECT * FROM bookings")
        for row in cursor.fetchall():
            print(row)

    def view_by_booking_id(self):
        print("\n4.2.2====== View by Booking ID======")
        bid = input("Enter Booking ID: ")
        cursor.execute("SELECT * FROM bookings WHERE booking_id=?", (bid,))
        print(cursor.fetchone())

    def view_by_passenger_id(self):
        print("\n4.2.3 =====View by Passenger ID======")
        pid = input("Enter Passenger ID: ")
        cursor.execute("SELECT * FROM bookings WHERE passenger_id=?", (pid,))
        for row in cursor.fetchall():
            print(row)

    # 4.3 CANCEL BOOKING
    def cancel_booking(self):
        print("\n===== CANCEL BOOKING ======")
        print("1. Cancel by Booking ID")
        print("2. Cancel by Passenger ID")
        ch =int( input("Enter choice: "))
        match ch:
            case 1:
                self.cancel_by_booking_id()
            case 2:   
                self.cancel_by_passenger_id()
            case _:
                print("Invalid choice")    

    def cancel_by_booking_id(self):
        print("\n4.3.1 ======Cancel by Booking ID======")
        bid = input("Enter Booking ID: ")
        cursor.execute("UPDATE bookings SET status='Cancelled' WHERE booking_id=?", (bid,))
        conn.commit()
        print("Booking Cancelled")

    def cancel_by_passenger_id(self):
        print("\n4.3.2 =====Cancel by Passenger ID=====")
        pid = input("Enter Passenger ID: ")
        cursor.execute("UPDATE bookings SET status='Cancelled' WHERE passenger_id=?", (pid,))
        conn.commit()
        print("All bookings of passenger cancelled")

    # 4.4 BOOKING HISTORY
    def booking_history(self):
        print("\n===== BOOKING HISTORY ======")
        print("1. Passenger Booking History")
        print("2. Flight Booking History")
        ch = int(input("Enter choice: "))
        match ch:
            case 1:
                 self.passenger_booking_history()
            case 2:
                self.flight_booking_history()
            case _:
                print("Invalid choice")    


       

    def passenger_booking_history(self):
        print("\n4.4.1===== Passenger Booking History=====")
        pid = input("Enter Passenger ID: ")
        cursor.execute("SELECT * FROM bookings WHERE passenger_id=?", (pid,))
        for row in cursor.fetchall():
            print(row)

    def flight_booking_history(self):
        print("\n4.4.2 ======Flight Booking History=====")
        fid = input("Enter Flight ID: ")
        cursor.execute("SELECT * FROM bookings WHERE flight_id=?", (fid,))
        for row in cursor.fetchall():
            print(row)


# Main Menu
obj = BookingManagement()

obj = BookingManagement()

while True:

    print("\n========== Booking Managment ==========")
    print("\n1.book ticket\n2.view booking\n3.cancle booking\n4.booking history")
    choice = int(input("Enter Choice : "))

    match choice:

        case 1:
           obj.book_ticket()

        case 2:
           obj.view_booking()

        case 3:
            obj.cancel_booking()

        case 4:
            obj.booking_history()        
        case _:
            print("Invalid Choice")

conn.close()

conn.close()