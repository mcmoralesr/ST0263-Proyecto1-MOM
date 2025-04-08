# mom-nodes/mom1/api_client.py

import requests
import os

API_URL = "http://localhost:5000"
TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")

def login_user(username: str, password: str):
    response = requests.post(f"{API_URL}/api/auth/login", json={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json().get("token")
        save_token(token)
        print("✅ Token guardado.")
        return token
    else:
        print("❌ Error de login:", response.json())
        return None

def save_token(token: str):
    with open(TOKEN_PATH, "w") as f:
        f.write(token)

def load_token():
    if not os.path.exists(TOKEN_PATH):
        print("⚠️ No hay token guardado. Ejecuta login primero.")
        return None
    with open(TOKEN_PATH, "r") as f:
        return f.read().strip()
