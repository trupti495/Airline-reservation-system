import sqlite3

conn = sqlite3.connect("airline.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM airlines")
print(cursor.fetchall())

cursor.execute("SELECT * FROM airports")
print(cursor.fetchall())

conn.close()