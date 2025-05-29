import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("qualtrack.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Add sample user (email = rso@example.com, password = test123)
cursor.execute("SELECT * FROM users WHERE email = ?", ("rso@example.com",))
if not cursor.fetchone():
    cursor.execute("""
    INSERT INTO users (name, email, password_hash, role)
    VALUES (?, ?, ?, ?)
    """, (
        "RSO Sample User",
        "rso@example.com",
        generate_password_hash("test123"),
        "rso"
    ))

conn.commit()
conn.close()

print("Users table created and sample user added.")
