import sqlite3

conn = sqlite3.connect("qualtrack.db")
cursor = conn.cursor()

print("\n--- PERSONNEL ---")
for row in cursor.execute("SELECT * FROM personnel"):
    print(row)

print("\n--- QUALIFICATIONS ---")
for row in cursor.execute("SELECT * FROM qualifications"):
    print(row)

conn.close()
