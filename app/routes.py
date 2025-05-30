import os
import sqlite3
import io
import csv
from datetime import datetime
from app.audit_logger import log_action

from functools import wraps
from flask import abort
def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role_name:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return wrapper
    return decorator


from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app.qualification_logic import evaluate_qualification
from app.user_model import User
from app.auth import login_manager
from app.database import get_db_connection

main = Blueprint("main", __name__, url_prefix="")

# ⚙️ Allowed weapons list (used across app)
ALLOWED_WEAPONS = ["M9", "M4/M16", "M500"]

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/dashboard")
def dashboard():
    print("📥 Starting dashboard build...")
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "qualtrack.db")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.name, p.rate, q.weapon, q.category, q.date_qualified
    FROM personnel p
    JOIN qualifications q ON p.id = q.personnel_id
    """)
    rows = cursor.fetchall()


    print(f"✅ Rows fetched: {len(rows)}")

    people = {}
    today = datetime.today()

    for name, rate, weapon, category, date_qualified in rows:
        print(f"🧪 {name} | {weapon} | {date_qualified}")
        if name not in people:
            cursor.execute("""
                SELECT ds.label
                FROM duty_sections ds
                JOIN personnel_duty pd ON pd.duty_section_id = ds.id
                JOIN personnel p2 ON pd.personnel_id = p2.id
                WHERE p2.name = ?
               """, (name,))
            duty_sections = [row[0] for row in cursor.fetchall()]

            people[name] = {
                "rate": rate,
                "unit": "",  # Placeholder if you add units later
                "duty_sections": duty_sections,
                "quals": []
            }


        try:
            print(f"🔍 Evaluating {name} - {weapon} on {date_qualified}")
            result = evaluate_qualification(date_qualified, category, today)
            # Apply filter if one was selected
            selected_status = request.args.get("status")
            if selected_status:
                if selected_status == "qualified" and not result["qualified"]:
                    continue
                elif selected_status == "sustainment_due" and not result["sustainment_due"]:
                    continue
                elif selected_status == "disqualified" and not result["disqualified"]:
                    continue

        except Exception as e:
            print(f"❌ Error evaluating {name}: {e}")
            continue

        people[name]["quals"].append({
            "weapon": weapon,
            "date_qualified": date_qualified,
            "status": result
        })
    conn.close()
    return render_template("dashboard.html", people=people)


@main.route("/new", methods=["GET", "POST"])
@login_required
@role_required("rso")
def new_qualification():
    
    print("🟢 Entered /new route")
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "qualtrack.db")

    if request.method == "POST":
        print("📩 POST received")
        name = request.form.get("name", "").strip()
        rate = request.form.get("rate", "").strip()
        duty_sections_raw = request.form.get("duty_sections", "").strip()
        duty_sections = [d.strip() for d in duty_sections_raw.split(",") if d.strip()]
        weapon = request.form.get("weapon", "").strip()
        category = request.form.get("category", "").strip()
        date_qualified = request.form.get("date_qualified", "").strip()

        if not all([name, rate, weapon, category, date_qualified]):
            print("❌ Missing fields")
            flash("All fields are required.", "error")
            return redirect(url_for("main.new_qualification"))

        try:
            category = int(category)
        except ValueError:
            print("❌ Category not a number")
            flash("Category must be a number.", "error")
            return redirect(url_for("main.new_qualification"))

        print("✅ Passed validation")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM personnel WHERE name = ? AND rate = ?", (name, rate))
        row = cursor.fetchone()
        if row:
            person_id = row[0]
            print(f"👤 Found existing person ID: {person_id}")
        else:
            cursor.execute("INSERT INTO personnel (name, rate) VALUES (?, ?)", (name, rate))
            person_id = cursor.lastrowid
            print(f"👤 Created new person ID: {person_id}")
        for section in duty_sections:
            # Add the section to the duty_sections table if not already present
            cursor.execute("INSERT OR IGNORE INTO duty_sections (label) VALUES (?)", (section,))
            # Look up the ID of that section
            cursor.execute("SELECT id FROM duty_sections WHERE label = ?", (section,))
            section_id = cursor.fetchone()[0]
            # Insert link between person and section
            cursor.execute("""
                INSERT OR IGNORE INTO personnel_duty (personnel_id, duty_section_id)
                VALUES (?, ?)
            """, (person_id, section_id))
        cursor.execute("""
            SELECT id FROM qualifications
            WHERE personnel_id = ? AND weapon = ?
        """, (person_id, weapon))
        if cursor.fetchone():
            print("⚠️ Duplicate qualification")
            flash("This qualification already exists for this person.", "warning")
            conn.close()
            return redirect(url_for("main.new_qualification"))

        print("💾 Inserting new qualification")
        cursor.execute("""
            INSERT INTO qualifications (personnel_id, weapon, category, date_qualified)
            VALUES (?, ?, ?, ?)
        """, (person_id, weapon, category, date_qualified))

        conn.commit()
        log_action(current_user.id, "add_qualification", f"{name} | {rate} | {weapon} | {date_qualified}")
        conn.close()
        print("✅ Commit successful")

        flash("Qualification added successfully!", "success")
        return redirect(url_for("main.dashboard"))

    print("📄 GET request — rendering form")
    return render_template("new_qual.html", weapons=ALLOWED_WEAPONS)

@main.route("/upload", methods=["GET", "POST"])
@login_required
@role_required("rso")
def upload_csv():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("No file uploaded.", "error")
            return redirect(url_for("main.upload_csv"))
        import csv
        import io

        # Parse CSV content
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)

        inserted = 0
        skipped = 0

        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "qualtrack.db")
        conn = get_db_connection()
        cursor = conn.cursor()

        for row in reader:
            try:
                name = row["name"].strip()
                rate = row["rate"].strip()
                weapon = row["weapon"].strip()
                if weapon not in ALLOWED_WEAPONS:
                    print(f"⚠️ Skipping invalid weapon: {weapon}")
                    skipped += 1
                    continue


                category = int(row["category"])
                date_qualified = row["date_qualified"].strip()

                if not all([name, rate, weapon, date_qualified]):
                    skipped += 1
                    continue

                # ✅ This logic now runs only if the row is valid
                cursor.execute("SELECT id FROM personnel WHERE name = ? AND rate = ?", (name, rate))
                row_result = cursor.fetchone()
                if row_result:
                    person_id = row_result[0]
                else:
                    cursor.execute("INSERT INTO personnel (name, rate) VALUES (?, ?)", (name, rate))
                    person_id = cursor.lastrowid

                # Skip if already qualified
                cursor.execute("SELECT id FROM qualifications WHERE personnel_id = ? AND weapon = ?", (person_id, weapon))
                if cursor.fetchone():
                    skipped += 1
                    continue

                cursor.execute("""
                    INSERT INTO qualifications (personnel_id, weapon, category, date_qualified)
                    VALUES (?, ?, ?, ?)
                """, (person_id, weapon, category, date_qualified))
                inserted += 1

            except Exception as e:
                print(f"❌ Error in row: {row} → {e}")
                skipped += 1
      
        conn.commit()
        conn.close()
        log_action(current_user.email, "upload_csv", f"{inserted} inserted, {skipped} skipped")
        flash(f"Import complete: {inserted} added, {skipped} skipped.", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("upload.html")

from flask import send_file
import csv
import io

@main.route("/audit-log")
@role_required("admin")  # Only admins should access this
def audit_log_view():
    db_path = os.path.join(os.path.dirname(__file__), "qualtrack.db")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, user_id, action, details FROM audit_log ORDER BY id DESC")
    logs = cursor.fetchall()
    conn.close()
    return render_template("audit_log.html", logs=logs)


@main.route("/export")
@login_required
@role_required("rso")
def export_qualifications():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "qualtrack.db")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.name, p.rate, q.weapon, q.category, q.date_qualified
    FROM personnel p
    JOIN qualifications q ON p.id = q.personnel_id
    """)
    rows = cursor.fetchall()
    conn.close()

    # Create in-memory CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["name", "rate", "weapon", "category", "date_qualified"])

    for row in rows:
        writer.writerow(row)

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="qualifications_export.csv"
    )
@login_manager.user_loader

def load_user(user_id):
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "qualtrack.db")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, password_hash, role FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return User(*row)
    return None

@main.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()
        
        # prints the username/password for Troubleshooting; delete later
        print(f"🔍 Submitted Email: '{email}'")
        print(f"🔍 Submitted Password: '{password}'")
        
# TODO: In CAC-enabled environments, replace this login logic
# with DOD certificate parsing + role lookup using user.email or DOD ID

        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "qualtrack.db")
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, email, password_hash, role FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            user = User(*row)
            from werkzeug.security import check_password_hash
            if check_password_hash(user.password_hash, password):
                login_user(user)
                flash("Login successful!", "success")
                return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("main.login"))

    return render_template("login.html")

@main.app_errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.login"))

@main.route("/audit-log")
@login_required
@role_required("admin")
def view_audit_log():
    db_path = os.path.join(os.path.dirname(__file__), "audit_log.db")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, user_email, action, details FROM audit_log ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return render_template("audit_log.html", logs=logs)
