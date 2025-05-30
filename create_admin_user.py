import os
import sqlite3
from werkzeug.security import generate_password_hash
from app.database import get_db_connection

# Update these with the admin credentials you want to use
name = "Admin User"
email = "admin2@example.com"
password = "AdminPassword123"
role = "admin"

conn = get_db_connection()
try:
    cursor = conn.cursor()
    hashed = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO users (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    """, (name, email, hashed, role))
    conn.commit()
    print("✅ Admin user created.")
finally:
    conn.close()
print("✅ Admin user created.")
