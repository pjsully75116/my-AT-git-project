import sqlite3

db_path = "app/qualtrack.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_email TEXT NOT NULL,
    action TEXT NOT NULL,
    details TEXT
)
""")

conn.commit()
conn.close()
print("✅ audit_log table created.")
