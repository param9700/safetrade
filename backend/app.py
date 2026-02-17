from flask import Flask, request, jsonify
from database import create_tables, get_db_connection

app = Flask(__name__)

@app.route("/")
def home():
    return "SafeTrade backend running!"

# -------- REGISTER API --------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

# -------- LOGIN API --------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    create_tables()
    app.run(debug=True, use_reloader=False)