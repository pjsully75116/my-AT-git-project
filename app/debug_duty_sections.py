import sqlite3

conn = sqlite3.connect("qualtrack.db")
cursor = conn.cursor()

print("\n--- Personnel ---")
cursor.execute("SELECT id, name, rate FROM personnel")
for row in cursor.fetchall():
    print(f"👤 ID {row[0]} | {row[1]} ({row[2]})")

print("\n--- Duty Section Assignments ---")
cursor.execute("""
SELECT p.name, p.rate, ds.label
FROM personnel p
JOIN personnel_duty pd ON p.id = pd.personnel_id
JOIN duty_sections ds ON ds.id = pd.duty_section_id
ORDER BY p.name
""")

rows = cursor.fetchall()
for row in rows:
    print(f"{row[0]} ({row[1]}) → Duty Section: {row[2]}")

conn.close()
