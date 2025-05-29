import sqlite3

conn = sqlite3.connect("qualtrack.db")
cursor = conn.cursor()

# Create duty_sections table
cursor.execute("""
CREATE TABLE IF NOT EXISTS duty_sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL UNIQUE
)
""")

# Create join table: personnel_duty
cursor.execute("""
CREATE TABLE IF NOT EXISTS personnel_duty (
    personnel_id INTEGER,
    duty_section_id INTEGER,
    FOREIGN KEY (personnel_id) REFERENCES personnel(id),
    FOREIGN KEY (duty_section_id) REFERENCES duty_sections(id),
    PRIMARY KEY (personnel_id, duty_section_id)
)
""")

print("✅ Tables created.")

conn.commit()
conn.close()
