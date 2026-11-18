from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Database connection
def get_db():
    conn = sqlite3.connect("gdg.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database table
def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            usn TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS event_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            student_name TEXT NOT NULL,
            email TEXT NOT NULL,
            usn TEXT NOT NULL
        )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")

    conn.commit()
    conn.close()

# Home route
@app.route("/")
def home():
    return "GDG RIT Backend is Running!"

# Member registration
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    usn = data.get("usn")
    department = data.get("department")

    if not all([name, email, usn, department]):
        return jsonify({"message": "All fields are required"}), 400

    conn = get_db()

    conn.execute("""
        INSERT INTO members (name, email, usn, department)
        VALUES (?, ?, ?, ?)
    """, (name, email, usn, department))

    conn.commit()
    conn.close()

    return jsonify({"message": "Registration successful!"})

# View registered members
@app.route("/members", methods=["GET"])
def members():

    conn = get_db()

    data = conn.execute("SELECT * FROM members").fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])
@app.route("/event-register", methods=["POST"])
def event_register():

    data = request.get_json()

    event_name = data.get("event_name")
    student_name = data.get("student_name")
    email = data.get("email")
    usn = data.get("usn")

    if not all([event_name, student_name, email, usn]):
        return jsonify({"message": "All fields are required"}), 400

    conn = get_db()

    conn.execute("""
        INSERT INTO event_registrations
        (event_name, student_name, email, usn)
        VALUES (?, ?, ?, ?)
    """, (event_name, student_name, email, usn))

    conn.commit()
    conn.close()

    return jsonify({"message": "Event registration successful!"})


@app.route("/event-registrations", methods=["GET"])
def get_event_registrations():

    conn = get_db()

    data = conn.execute(
        "SELECT * FROM event_registrations"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])
    # SAVE CONTACT MESSAGES
@app.route("/contact", methods=["POST"])
def contact():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    if not all([name, email, subject, message]):
        return jsonify({"message": "Please fill all fields"}), 400

    conn = get_db()

    conn.execute("""
        INSERT INTO contact_messages (name, email, subject, message)
        VALUES (?, ?, ?, ?)
    """, (name, email, subject, message))

    conn.commit()
    conn.close()

    return jsonify({"message": "Message sent successfully!"})


# VIEW CONTACT MESSAGES
@app.route("/contact-messages", methods=["GET"])
def get_contact_messages():

    conn = get_db()

    data = conn.execute(
        "SELECT * FROM contact_messages ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(row) for row in data])
if __name__ == "__main__":
    create_table()
    app.run(debug=True)