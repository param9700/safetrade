import requests

# -------- REGISTER TEST --------
register_url = "http://127.0.0.1:5000/register"

register_data = {
    "username": "nigesh",
    "email": "paramr509@gmail.com",
    "password": "1234"
}
register_url = "http://127.0.0.1:5000/register"
print("Trying to connect to:", register_url)
r = requests.post(register_url, json=register_data)
print("Register:", r.text)

# -------- LOGIN TEST --------
login_url = "http://127.0.0.1:5000/login"

login_data = {
    "email": "paramr509@gmail.com",
    "password": "1234"
}

r = requests.post(login_url, json=login_data)
login_response = r.json()

print("Login:", login_response)

token = login_response["token"]

# -------- ADD PRODUCT TEST --------
product_url = "http://127.0.0.1:5000/add_product"

product_data = {
    "title": "Honda Activa",
    "description": "Good condition scooty",
    "price": 35000,
    "seller_email": "paramr509@gmail.com"
}
headers = {
    "Authorization": f"Bearer {token}"
}

r = requests.post(product_url, json=product_data, headers=headers)
print("Add Product:", r.text)


