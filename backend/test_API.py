import requests

# -------- REGISTER TEST --------
register_url = "http://127.0.0.1:5000/register"

register_data = {
    "username": "nigesh",
    "email": "nigesh@gmail.com",
    "password": "1234"
}

r = requests.post(register_url, json=register_data)
print("Register:", r.json())

# -------- LOGIN TEST --------
login_url = "http://127.0.0.1:5000/login"

login_data = {
    "email": "nigesh@gmail.com",
    "password": "1234"
}

r = requests.post(login_url, json=login_data)
print("Login:", r.json())
