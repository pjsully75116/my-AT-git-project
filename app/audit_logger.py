# app/audit_logger.py
import os
import sqlite3
from datetime import datetime



def log_action(user_id, action, details=""):
    db_path = os.path.join(os.path.dirname(__file__), "qualtrack.db")
    print(f"🔍 Logging to: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    timestamp = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO audit_log (timestamp, user_id, action, details)
        VALUES (?, ?, ?, ?)
    """, (timestamp, user_id, action, details))


    conn.commit()
    conn.close()
