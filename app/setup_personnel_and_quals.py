# app/setup_personnel_and_quals.py

import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "..", "qualtrack.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create personnel table
cursor.execute("""
CREATE TABLE IF NOT EXISTS personnel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rate TEXT NOT NULL
)
""")

# Create qualifications table
cursor.execute("""
CREATE TABLE IF NOT EXISTS qualifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personnel_id INTEGER NOT NULL,
    weapon TEXT NOT NULL,
    category INTEGER NOT NULL,
    date_qualified TEXT NOT NULL,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id)
)
""")

conn.commit()
conn.close()
print("✅ Created personnel and qualifications tables.")
