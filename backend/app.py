import jwt
import datetime
from flask_cors import CORS
from functools import wraps

from flask import Flask, request, jsonify
from database import create_tables, get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'mysecretkey123'

# 🔥 IMPORTANT FOR RENDER
create_tables()

# ---------------- TOKEN DECORATOR ----------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from Authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            data = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )

            request.user_email = data["email"]

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

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except:
        return jsonify({
            "message": "Email already registered"
        }), 400

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

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user["password"], password):

        token = jwt.encode({
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        app.config['SECRET_KEY'],
        algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200

    else:
        return jsonify({
            "message": "Invalid credentials"
        }), 401


# ---------------- ADD PRODUCT ----------------
@app.route("/add_product", methods=["POST"])
@token_required
def add_product():

    data = request.json

    title = data["title"]
    description = data["description"]
    price = data["price"]

    # 🔥 seller email comes from JWT
    seller_email = request.user_email

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (title, description, price, seller_email) VALUES (?, ?, ?, ?)",
        (title, description, price, seller_email)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Product added successfully"
    }), 201


# ---------------- GET PRODUCTS ----------------
@app.route("/products", methods=["GET"])
def get_products():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    conn.close()

    product_list = [dict(product) for product in products]

    return jsonify(product_list), 200


# ---------------- DELETE PRODUCT ----------------
@app.route("/product/<int:product_id>", methods=["DELETE"])
@token_required
def delete_product(product_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        conn.close()

        return jsonify({
            "message": "Product not found"
        }), 404

    # 🔥 only owner can delete
    if product["seller_email"] != request.user_email:
        conn.close()

        return jsonify({
            "message": "Unauthorized"
        }), 403

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Product deleted successfully"
    }), 200

# ---------------- EDIT PRODUCT ----------------
@app.route("/product/<int:id>", methods=["PUT"])
@token_required
def edit_product(id):

    seller_email = request.user_email
    data = request.json

    title = data["title"]
    description = data["description"]
    price = data["price"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (id,)
    )

    product = cursor.fetchone()

    if not product:
        conn.close()
        return jsonify({
            "message": "Product not found"
        }), 404

    if product["seller_email"] != seller_email:
        conn.close()
        return jsonify({
            "message": "Unauthorized"
        }), 403

    cursor.execute(
        """
        UPDATE products
        SET title = ?, description = ?, price = ?
        WHERE id = ?
        """,
        (title, description, price, id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Product updated successfully"
    }), 200

# ---------------- MY PRODUCTS ----------------

@app.route("/my_products", methods=["GET"])
@token_required
def my_products():

    seller_email = request.user_email

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE seller_email = ?",
        (seller_email,)
    )

    products = cursor.fetchall()

    conn.close()

    product_list = [dict(product) for product in products]

    return jsonify(product_list), 200

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)