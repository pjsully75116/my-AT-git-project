import sqlite3
from datetime import datetime
from qualification_logic import evaluate_qualification

# Connect to the database
conn = sqlite3.connect("qualtrack.db")
cursor = conn.cursor()

# Get all personnel with their qualifications
cursor.execute("""
SELECT p.name, p.rate, q.weapon, q.category, q.date_qualified
FROM personnel p
JOIN qualifications q ON p.id = q.personnel_id
""")

rows = cursor.fetchall()

# Group results by person
people = {}

for name, rate, weapon, category, date_qualified in rows:
    if name not in people:
        people[name] = {
            "rate": rate,
            "quals": []
        }

    people[name]["quals"].append({
        "weapon": weapon,
        "category": category,
        "date_qualified": date_qualified
    })

# Evaluate and print
today = datetime.today()
for name, info in people.items():
    print(f"\nEvaluating: {name} ({info['rate']})")
    for qual in info["quals"]:
        result = evaluate_qualification(
            date_qualified=qual["date_qualified"],
            category=qual["category"],
            today=today
        )
        print(f"  Weapon: {qual['weapon']}")
        for key, value in result.items():
            print(f"    {key}: {value}")

conn.close()
