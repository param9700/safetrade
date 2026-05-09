import requests

# ---------------- REGISTER ----------------
register_url = "https://safetrade-backend.onrender.com/register"

register_data = {
    "username": "nigesh",
    "email": "paramr509@gmail.com",
    "password": "1234"
}

r = requests.post(register_url, json=register_data)
print("Register:", r.text)


# ---------------- LOGIN ----------------
login_url = "https://safetrade-backend.onrender.com/login"

login_data = {
    "email": "paramr509@gmail.com",
    "password": "1234"
}

r = requests.post(login_url, json=login_data)

print("Raw Login Response:", r.text)


# ---------------- ADD PRODUCT ----------------
product_url = "https://safetrade-backend.onrender.com/add_product"

product_data = {
    "title": "Honda Activa",
    "description": "Good condition scooty",
    "price": 35000
}

r = requests.post(product_url, json=product_data)

print("Add Product:", r.text)