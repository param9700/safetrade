import jwt
import datetime
from functools import wraps


from flask import Flask, request, jsonify
from database import create_tables, get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey123'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({"message": "Token invalid"}), 401

        return f(*args, **kwargs)

    return decorated

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "SafeTrade backend running!"

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"message": "Email already registered"}), 400

    finally:
        conn.close()

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):

        token = jwt.encode({
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200

    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ---------------- ADD PRODUCT ----------------
@app.route("/add_product", methods=["POST"])
@token_required
def add_product():
    data = request.json
    title = data["title"]
    description = data["description"]
    price = data["price"]
    seller_email = data["seller_email"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (title, description, price, seller_email) VALUES (?, ?, ?, ?)",
        (title, description, price, seller_email)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Product added successfully"}), 201

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    create_tables()
    app.run(debug=True, use_reloader=False)
