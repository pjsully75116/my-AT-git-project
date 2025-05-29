import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect("qualtrack.db")
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
    personnel_id INTEGER,
    weapon TEXT NOT NULL,
    category INTEGER NOT NULL,
    date_qualified TEXT NOT NULL,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id)
)
""")

# Commit and close
