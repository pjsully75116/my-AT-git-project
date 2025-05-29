import sqlite3
import os

# Centralize DB location
db_path = os.path.join(os.path.dirname(__file__), "app", "qualtrack.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔧 Initializing database...")

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# PERSONNEL
cursor.execute("""
CREATE TABLE IF NOT EXISTS personnel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rate TEXT NOT NULL
)
""")

# QUALIFICATIONS
cursor.execute("""
CREATE TABLE IF NOT EXISTS qualifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personnel_id INTEGER,
    weapon TEXT NOT NULL,
    category TEXT NOT NULL,
    date_qualified TEXT NOT NULL,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id)
)
""")

# DUTY SECTIONS
cursor.execute("""
CREATE TABLE IF NOT EXISTS duty_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL
)
""")

# PERSONNEL-DUTY LINK
cursor.execute("""
CREATE TABLE IF NOT EXISTS personnel_duty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    personnel_id INTEGER,
    duty_section_id INTEGER,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id),
    FOREIGN KEY (duty_section_id) REFERENCES duty_sections(id)
)
""")

# AUDIT LOG
cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT
)
""")

conn.commit()
conn.close()
print(f"✅ Database initialized at: {db_path}")
