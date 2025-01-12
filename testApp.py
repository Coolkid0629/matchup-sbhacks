import os
import json
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from models import create_tables, conn
from embedding_utils import get_embedding
import struct
import subprocess

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend
# --- Create Tables ---
create_tables()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder for profile pictures if not exists

def create_user_wallet():
    """Creates a new Solana wallet and returns the public key and secret key."""
    try:
        result = subprocess.run(["solana-keygen", "new", "--no-outfile"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        pubkey = [line.split(": ")[1] for line in lines if line.startswith("pubkey")][0]
        seed_phrase = [line.split(": ")[1] for line in lines if line.startswith("Save this seed phrase")][0]
        return pubkey, seed_phrase
    except Exception as e:
        print(f"Error creating wallet: {e}")
        return None, None
    
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"}), 200


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

@app.route('/api/signup', methods=['POST'])



def signup():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        interests = data.get('interests')
        lunch_time = data.get('lunch_time', None)  # Default to None if not provided
        profile_picture_data = data.get('profile_picture')  # Base64 encoded string

        if not all([name, email, password, interests]):
            return jsonify({"error": "All fields except lunch time and profile picture are required!"}), 400

        # Ensure the database connection is open
        if not conn.open:
            conn.ping(reconnect=True)

        vector = get_embedding(interests)
        vector_blob = struct.pack(f'{len(vector)}f', *vector)

        # Save profile picture if provided
        profile_picture_path = None
        if profile_picture_data:
            picture_filename = f"{email.replace('@', '_at_')}.png"
            profile_picture_path = os.path.join(UPLOAD_FOLDER, picture_filename)
            with open(profile_picture_path, "wb") as f:
                f.write(base64.b64decode(profile_picture_data))
            print(f"Profile picture saved at: {profile_picture_path}")

        # Execute database queries
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM user_profiles WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email already exists"}), 400

            cursor.execute("""
                INSERT INTO user_profiles (name, email, password, vector, interests, lunch_time, profile_picture)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, email, password, vector_blob, interests, lunch_time, profile_picture_path))
            conn.commit()

        return jsonify({"message": "Signup successful!"}), 200

    except Exception as e:
        print(f"Error during signup: {e}")
        return jsonify({"error": "Signup failed due to an error."}), 500



# --- API to Handle Login ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, email, password FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid login credentials"}), 401

    user_data = {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "password": user[3]
    }
    return jsonify(user_data), 200

# --- API to Fetch User Data ---
@app.route('/api/user-data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # i ove sql :0
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, email, interests, lunch_time, profile_picture FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 404

    user_data = {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "interests": user[3],
        "lunch_time": user[4],
        "profile_picture": f"/api/profile-picture?email={email}" if user[5] else None
    }
    return jsonify(user_data), 200

@app.route('/api/user-count', methods=['GET'])
def get_user_count():
    """Return the total number of users and active users in the database."""
    with conn.cursor() as cursor:
        # Count total users
        cursor.execute("SELECT COUNT(*) FROM user_profiles")
        total_users = cursor.fetchone()[0]

        # Count active users
        cursor.execute("SELECT COUNT(*) FROM user_profiles WHERE status = 'active'")
        active_users = cursor.fetchone()[0]

    return jsonify({"total_users": total_users, "active_users": active_users}), 200

# --- API to Fetch Profile Picture ---
@app.route('/api/profile-picture', methods=['GET'])
def get_profile_picture():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400

    with conn.cursor() as cursor:
        cursor.execute("SELECT profile_picture FROM user_profiles WHERE email = %s", (email,))
        profile_picture_path = cursor.fetchone()

    if not profile_picture_path or not profile_picture_path[0]:
        return jsonify({"error": "Profile picture not found"}), 404

    return send_file(profile_picture_path[0], mimetype='image/png')

def deposit_to_user_wallet(user_wallet_address):
    """Send a request to the Solana middleware to deposit 1 SOL."""
    solana_middleware_url = "http://localhost:3000/mint-token"
    payload = {"userPublicKey": user_wallet_address}

    try:
        response = requests.post(solana_middleware_url, json=payload)
        return response.status_code == 201
    except Exception as e:
        print(f"Error communicating with Solana middleware: {e}")
        return False

# --- API to Fetch Matches ---
@app.route('/api/matches', methods=['POST'])
def get_matches():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, interests, vector, lunch_time FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        current_user = cursor.fetchone()

    if not current_user:
        return jsonify({"error": "Invalid email or password"}), 404

    import numpy as np

    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, interests, vector, lunch_time FROM user_profiles")
        users = cursor.fetchall()

    user_data = [{"id": u[0], "name": u[1], "interests": u[2].lower().split(", "), "vector": np.frombuffer(u[3], dtype=np.float32).tolist(), "lunch_time": u[4]} for u in users]

    matches = []
    for other_user in user_data:
        if current_user[0] == other_user["id"]:
            continue

        if current_user[4] != other_user["lunch_time"]:
            continue

        current_interests = set(current_user[2].lower().split(", "))
        other_interests = set(other_user["interests"])
        common_interests = list(current_interests.intersection(other_interests))

        similarity = np.dot(current_user[3], other_user["vector"]) / (
            np.linalg.norm(current_user[3]) * np.linalg.norm(other_user["vector"])
        )

        if common_interests:
            matches.append({
                "match_name": other_user["name"],
                "common_interests": common_interests,
                "similarity": round(similarity, 2),
                "lunch_time": current_user[4]
            })

    if deposit_to_user_wallet(other_user["wallet_address"]):
        print(f"Deposited 1 SOL to {other_user['wallet_address']}")

    return jsonify(matches), 200

@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    new_status = data.get('status')  # Accepts "active" or "inactive"

    if new_status not in ["active", "inactive"]:
        return jsonify({"error": "Invalid status value. Use 'active' or 'inactive'"}), 400

    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 404

    with conn.cursor() as cursor:
        cursor.execute("UPDATE user_profiles SET status = %s WHERE email = %s", (new_status, email))
        conn.commit()

    return jsonify({"message": f"User status updated to '{new_status}'"}), 200


# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True)
