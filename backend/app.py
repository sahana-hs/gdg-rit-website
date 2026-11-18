import os
import sqlite3
import hmac
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

app = Flask(__name__)

CORS(app)

# Admin credentials and secret must be configured as environment variables
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
SECRET_KEY = os.environ.get("SECRET_KEY")

if not ADMIN_USERNAME or not ADMIN_PASSWORD or not SECRET_KEY:
    raise RuntimeError("Set ADMIN_USERNAME, ADMIN_PASSWORD and SECRET_KEY")

serializer = URLSafeTimedSerializer(SECRET_KEY)

# Database connection
def get_db():
    conn = sqlite3.connect("gdg.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database tables
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


# Protect admin APIs
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        token = request.headers.get("Authorization", "")

        if not token.startswith("Bearer "):
            return jsonify({"message": "Please log in"}), 401

        try:
            data = serializer.loads(token[7:], max_age=3600)

            if data.get("username") != ADMIN_USERNAME:
                return jsonify({"message": "Invalid login"}), 401

        except (BadSignature, SignatureExpired):
            return jsonify({"message": "Session expired. Log in again."}), 401

        return func(*args, **kwargs)

    return wrapper


# Home route
@app.route("/")
def home():
    return "GDG RIT Backend is Running!"


# Admin login
@app.route("/admin-login", methods=["POST"])
def admin_login():

    data = request.get_json(silent=True) or {}

    username = data.get("username", "")
    password = data.get("password", "")

    if (
        hmac.compare_digest(username, ADMIN_USERNAME)
        and hmac.compare_digest(password, ADMIN_PASSWORD)
    ):
        token = serializer.dumps({"username": ADMIN_USERNAME})

        return jsonify({
            "message": "Login successful",
            "token": token
        })

    return jsonify({"message": "Incorrect username or password"}), 401


# Member registration - public
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

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


# View members - admin only
@app.route("/members", methods=["GET"])
@admin_required
def members():

    conn = get_db()
    data = conn.execute("SELECT * FROM members").fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])


# Event registration - public
@app.route("/event-register", methods=["POST"])
def event_register():

    data = request.get_json(silent=True) or {}

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


# View event registrations - admin only
@app.route("/event-registrations", methods=["GET"])
@admin_required
def get_event_registrations():

    conn = get_db()
    data = conn.execute(
        "SELECT * FROM event_registrations"
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])


# Contact form - public
@app.route("/contact", methods=["POST"])
def contact():

    data = request.get_json(silent=True) or {}

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


# View contact messages - admin only
@app.route("/contact-messages", methods=["GET"])
@admin_required
def get_contact_messages():

    conn = get_db()
    data = conn.execute(
        "SELECT * FROM contact_messages ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in data])


# Create tables when the application starts
create_table()

if __name__ == "__main__":
    app.run(debug=False)