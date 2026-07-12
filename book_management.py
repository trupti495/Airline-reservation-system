from datetime import datetime
from database import get_connection
from tabulate import tabulate # NEW
from rich.console import Console

console = Console()

def heading(title):
    print()
    console.rule(
        f"[bold bright_yellow]{title}[/bold bright_yellow]",
        style="bright_blue"
    )
    print()
conn = get_connection()
cursor = conn.cursor()

class BookingManagement:

    def __init__(self):
        self.passenger_id = None
        self.flight_id = None

    # Main Menu
    def main(self): 

      try:
        while True:
            heading("BOOKING MANAGEMENT")
            print("1. Book Ticket")
            print("2. View Booking")
            print("3. Cancel Booking")
            print("4. Booking History")
            print("5. Exit")

            choice = int(input("Enter Choice : "))
            match choice:
             case 1:
              self.book_ticket()
             case 2:
              self.view_booking()
             case 3:
              self.cancel_booking()
             case 4:
              self.booking_history()
             case 5:
              break
             case _:
              print("Invalid Choice")

      except ValueError:
        print("Error: Please enter a valid number") 

    # 4.1 Book Ticket
    def book_ticket(self):
        while True:
            try:
                heading("BOOK TICKET")
                print("1. Search Passenger")
                print("2. Search Flight")
                print("3. Confirm Booking")
                print("4. Back")
                ch = int(input("Enter your choice: "))

                match ch:
                    case 1: self.search_passenger()
                    case 2: self.search_flight()
                    case 3: self.confirm_booking()
                    case 4: break
                    case _: print("Invalid Choice")
            except ValueError:
                print("Error: Please enter a valid number")
            except Exception as e:
                print("An error occurred:", e)

    # 4.1.1 Search Passenger
    def search_passenger(self):
        try:
            heading("SEARCH PASSENGER")
            pid = input("Enter Passenger ID: ")
            if pid == "":
                print("Passenger ID cannot be empty")
                return

            cursor.execute("SELECT * FROM passengers WHERE passenger_id=?", (pid,))
            passenger = cursor.fetchone()
            if passenger:
                headers = ["ID", "Name", "Age", "Gender", "Phone"]
                print(tabulate([passenger], headers=headers, tablefmt="grid"))
                self.passenger_id = pid
            else:
                print("Passenger Not Found")
        except Exception as e:
            print("Error:", e)

    # 4.1.2 Search Flight
    def search_flight(self):
        try:
            heading("SEARCH FLIGHT")
            source = input("Enter Source Airport ID: ").strip()
            destination = input("Enter Destination Airport ID: ").strip()
            departure_date = input("Enter Departure Date (YYYY-MM-DD): ").strip()

            cursor.execute("""
                SELECT flight_id, airline_id, source_airport_id,
                       destination_airport_id, departure_date,
                       departure_time, fare, available_seats
                FROM flights
                WHERE source_airport_id=? AND destination_airport_id=? AND departure_date=?
            """, (source, destination, departure_date))

            flights = cursor.fetchall()

            if not flights:
                print("No Flights Available.")
                return

            headers = ["FlightID", "AirlineID", "Source", "Destination", "Date", "Time", "Fare", "Seats"]
            print(tabulate(flights, headers=headers, tablefmt="fancy_grid")) # TABULATE

            fid = input("\nEnter Flight ID to Book: ").strip()
            cursor.execute("SELECT flight_id FROM flights WHERE flight_id=?", (fid,))
            if cursor.fetchone():
                self.flight_id = fid
                print("Flight Selected Successfully")
            else:
                print("Invalid Flight ID")
        except Exception as e:
            print("Error:", e)

    # 4.1.3 Confirm Booking
    def confirm_booking(self):
        try:
            heading("CONFIRM BOOKING")
            passenger_id = input("Enter Passenger ID: ").strip()
            cursor.execute("SELECT * FROM passengers WHERE passenger_id=?", (passenger_id,))
            if cursor.fetchone() is None:
                print("Passenger ID not found.")
                return

            flight_id = input("Enter Flight ID: ").strip()
            cursor.execute("SELECT available_seats FROM flights WHERE flight_id=?", (flight_id,))
            flight_data = cursor.fetchone()
            if flight_data is None:
                print("Flight ID not found.")
                return
            if flight_data[0] <= 0:
                print("No seats available on this flight.")
                return

            seat_no = input("Enter Seat Number: ").strip()
            cursor.execute("SELECT * FROM bookings WHERE flight_id=? AND seat_no=? AND status=?",
                           (flight_id, seat_no, "Confirmed"))
            if cursor.fetchone():
                print("Seat is already booked.")
                return

            booking_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                INSERT INTO bookings (passenger_id, flight_id, seat_no, booking_date, status)
                VALUES(?,?,?,?,?)
            """, (passenger_id, flight_id, seat_no, booking_date, "Confirmed"))

            cursor.execute("UPDATE flights SET available_seats = available_seats - 1 WHERE flight_id=?", (flight_id,))
            conn.commit()
            print("Booking Confirmed Successfully")
        except Exception as e:
            conn.rollback()
            print("Error:", e)

    # 4.2 VIEW BOOKING
    def view_booking(self):
        while True:
            try:
                heading("VIEW BOOKING")
                print("1. View All Bookings")
                print("2. View by Booking ID")
                print("3. View by Passenger ID")
                print("4. Back")
                ch = int(input("Enter choice: "))

                match ch:
                    case 1: self.view_all_bookings()
                    case 2: self.view_by_booking_id()
                    case 3: self.view_by_passenger_id()
                    case 4: break
                    case _: print("Invalid Choice")
            except ValueError:
                print("Error: Please enter a valid number")

    def view_all_bookings(self):
        try:
            heading("VIEW ALL BOOKINGS")
            cursor.execute("SELECT * FROM bookings")
            rows = cursor.fetchall()
            if rows:
                headers = ["BookingID", "PassengerID", "FlightID", "DATE", "SEAT NO", "Status"]
                print(tabulate(rows, headers=headers, tablefmt="pretty")) # TABULATE
            else:
                print("No bookings found")
        except Exception as e:
            print("Database Error:", e)

    def view_by_booking_id(self):
        try:
            heading("CANCEL BOOKING BY ID")
            bid = input("Enter Booking ID: ").strip()
            cursor.execute("SELECT * FROM bookings WHERE booking_id=?", (bid,))
            result = cursor.fetchone()
            if result:
                headers = ["BookingID", "PassengerID", "FlightID", "Date", "SeatNo", "Status"]
                print(tabulate([result], headers=headers, tablefmt="grid"))
            else:
                print("Booking not found")
        except Exception as e:
            print("Database Error:", e)

    def view_by_passenger_id(self):
        try:
            heading(" VIEW BOOKINGS BY PASSENGER ID ")
            pid = input("Enter Passenger ID: ").strip()
            cursor.execute("SELECT * FROM bookings WHERE passenger_id=?", (pid,))
            rows = cursor.fetchall()
            if rows:
                headers = ["BookingID", "PassengerID", "FlightID", "Date", "SeatNo", "Status"]
                print(tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                print("No bookings found for this passenger")
        except Exception as e:
            print("Database Error:", e)

    # 4.3 CANCEL BOOKING
    def cancel_booking(self):
        while True:
            try:
                heading("CANCEL BOOKING")
                print("1. Cancel by Booking ID")
                print("2. Cancel by Passenger ID")
                print("3. Back")
                ch = int(input("Enter choice: "))

                match ch:
                    case 1: self.cancel_by_booking_id()
                    case 2: self.cancel_by_passenger_id()
                    case 3: break
                    case _: print("Invalid choice")
            except ValueError:
                print("Error: Please enter a valid number")

    def cancel_by_booking_id(self):
        try:
            heading("CANCEL BOOKING BY ID")
            bid = input("Enter Booking ID: ")
            cursor.execute("SELECT flight_id FROM bookings WHERE booking_id=? AND status='Confirmed'", (bid,))
            data = cursor.fetchone()
            if not data:
                print("Booking not found or already cancelled")
                return
            flight_id = data[0]
            cursor.execute("UPDATE bookings SET status='Cancelled' WHERE booking_id=?", (bid,))
            cursor.execute("UPDATE flights SET available_seats = available_seats + 1 WHERE flight_id=?", (flight_id,))
            conn.commit()
            print("Booking Cancelled Successfully")
        except Exception as e:
            conn.rollback()
            print("Database Error:", e)

    def cancel_by_passenger_id(self):
        try:
         heading("CANCEL BOOKING")

         pid = input("Enter Passenger ID: ")
         fid = input("Enter Flight ID: ")

        # Check if booking exists for this passenger and flight
         cursor.execute("""
            SELECT status
            FROM bookings
            WHERE passenger_id=? AND flight_id=?
         """, (pid, fid))

         booking = cursor.fetchone()

         if booking is None:
            print("Flight is not present for this passenger.")
            return

         if booking[0] == "Cancelled":
            print("Booking is already cancelled.")
            return

        # Cancel booking
         cursor.execute("""
            UPDATE bookings
            SET status='Cancelled'
            WHERE passenger_id=? AND flight_id=?
         """, (pid, fid))

        # Increase available seats
         cursor.execute("""
            UPDATE flights
            SET available_seats = available_seats + 1
            WHERE flight_id=?
         """, (fid,))

         conn.commit()
         print("Booking cancelled successfully.")

        except Exception as e:
         conn.rollback()
         print("Database Error:", e)

    # 4.4 BOOKING HISTORY
    def booking_history(self):
        while True:
            try:
                heading("BOOKING HISTORY")
                print("1. Passenger Booking History")
                print("2. Flight Booking History")
                print("3. Back")
                ch = int(input("Enter choice: "))

                match ch:
                    case 1: self.passenger_booking_history()
                    case 2: self.flight_booking_history()
                    case 3: break
                    case _: print("Invalid choice")
            except ValueError:
                print("Error: Please enter a valid number")

    def passenger_booking_history(self):
        try:
            heading("PASSENGER BOOKING HISTORY")
            pid = input("Enter Passenger ID: ").strip()
            cursor.execute("SELECT * FROM bookings WHERE passenger_id=?", (pid,))
            rows = cursor.fetchall()
            if rows:
                headers = ["BookingID", "PassengerID", "FlightID", "SeatNo", "Date", "Status"]
                print(tabulate(rows, headers=headers, tablefmt="github")) # TABULATE
            else:
                print("No history found")
        except Exception as e:
            print("Database Error:", e)

    def flight_booking_history(self):
        try:
            heading("FLIGHT BOOKING HISTORY")
            fid = input("Enter Flight ID: ").strip()
            cursor.execute("SELECT * FROM bookings WHERE flight_id=?", (fid,))
            rows = cursor.fetchall()
            if rows:
                headers = ["BookingID", "PassengerID", "FlightID", "SeatNo", "Date", "Status"]
                print(tabulate(rows, headers=headers, tablefmt="github"))
            else:
                print("No history found")
        except Exception as e:
            print("Database Error:", e)

if __name__ == "__main__":
# Main Menu
 obj=BookingManagement()
 obj.main()
