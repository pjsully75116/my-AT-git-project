import sqlite3
from werkzeug.security import generate_password_hash

# Update these with the admin credentials you want to use
name = "Admin User"
email = "admin@example.com"
password = "AdminPassword123"
role = "admin"

db_path = "app/qualtrack.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

hashed = generate_password_hash(password)

cursor.execute("""
    INSERT INTO users (name, email, password_hash, role)
    VALUES (?, ?, ?, ?)
""", (name, email, hashed, role))

conn.commit()
conn.close()
print("✅ Admin user created.")
