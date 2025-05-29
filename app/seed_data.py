import sqlite3
from datetime import datetime, timedelta

# Connect to the existing database
conn = sqlite3.connect("qualtrack.db")
cursor = conn.cursor()

# Clear existing data (for clean runs)
cursor.execute("DELETE FROM qualifications")
cursor.execute("DELETE FROM personnel")

# Today's date
today = datetime.today()

# Sample test people with dynamic qualification dates
test_people = [
    {
        "name": "ENS Riley Chen",
        "rate": "O-1",
        "quals": [
            # Qualified 3 months ago — fully valid
            {"weapon": "M9", "category": 2, "date_qualified": (today - timedelta(days=90)).strftime("%Y-%m-%d")}
        ]
    },
    {
        "name": "BM2 Marcus Hill",
        "rate": "E-5",
        "quals": [
            # Qualified 7 months ago — sustainment due
            {"weapon": "M4", "category": 2, "date_qualified": (today - timedelta(days=210)).strftime("%Y-%m-%d")}
        ]
    },
    {
        "name": "FC3 Dana Ortiz",
        "rate": "E-4",
        "quals": [
            # Qualified 13 months ago — disqualified
            {"weapon": "M240", "category": 2, "date_qualified": (today - timedelta(days=395)).strftime("%Y-%m-%d")}
        ]
    }
]

# Insert each person and their quals
for person in test_people:
    cursor.execute("INSERT INTO personnel (name, rate) VALUES (?, ?)", (person["name"], person["rate"]))
    person_id = cursor.lastrowid

    for qual in person["quals"]:
        cursor.execute("""
            INSERT INTO qualifications (personnel_id, weapon, category, date_qualified)
            VALUES (?, ?, ?, ?)
        """, (person_id, qual["weapon"], qual["category"], qual["date_qualified"]))

# Save and close
conn.commit()
conn.close()

print("Seed data inserted successfully.")
