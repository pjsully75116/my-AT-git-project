import sqlite3
import os

# Path to the shared project database
db_path = os.path.join(os.path.dirname(__file__), "app", "qualtrack.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Recreate audit_log table with user_id
cursor.execute("DROP TABLE IF EXISTS audit_log")
cursor.execute("""
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT
)
""")

conn.commit()
conn.close()
print("✅ audit_log table created successfully.")
