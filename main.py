from flask import Flask, request, jsonify
import os
import random
import string

app = Flask(__name__)

# User data storage directory
USERS_DIR = "users"
if not os.path.exists(USERS_DIR):
    os.makedirs(USERS_DIR)

def register_user(user_id, password):
    """Register a new user"""
    user_file = os.path.join(USERS_DIR, f"user_{user_id}.txt")
    if os.path.exists(user_file):
        return False  # User already exists
    with open(user_file, "w") as f:
        f.write(f"{password}\n")  # First line - password
    return True

def authenticate_user(user_id, password):
    """Authenticate existing user"""
    user_file = os.path.join(USERS_DIR, f"user_{user_id}.txt")
    if not os.path.exists(user_file):
        return False  # User not found
    with open(user_file, "r") as f:
        stored_password = f.readline().strip()
    return stored_password == password

@app.route('/register', methods=['POST'])
def register():
    """Handle registration requests"""
    data = request.json
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    if register_user(user_id, password):
        return jsonify({"status": "success", "message": "User registered"}), 200
    else:
        return jsonify({"status": "error", "message": "User already exists"}), 400

if __name__ == "__main__":
    app.run(port=5000)