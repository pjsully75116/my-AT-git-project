import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("qualtrack.db")
cursor = conn.cursor()

# Add viewer user
cursor.execute("SELECT * FROM users WHERE email = ?", ("viewer@example.com",))
if not cursor.fetchone():
    cursor.execute("""
    INSERT INTO users (name, email, password_hash, role)
    VALUES (?, ?, ?, ?)
    """, (
        "Viewer User",
        "viewer@example.com",
        generate_password_hash("viewer123"),
        "viewer"
    ))
    print("✅ Viewer user added.")
else:
    print("⚠️ Viewer user already exists.")

conn.commit()
conn.close()
