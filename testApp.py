import os
import json
import base64
import random
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from models import create_tables, create_connection
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
        print("test1")
        data = request.get_json()
        print("test2")
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        interests = data.get('interests')
        lunch_time = data.get('lunch_time', None)  # Default to None if not provided
        profile_picture_data = data.get('profile_picture')  # Base64 encoded string
        bio = data.get('bio', '')  # Optional short bio, defaults to empty string if not provided

        if not all([name, email, password, interests]):
            return jsonify({"error": "All fields except lunch time, bio, and profile picture are required!"}), 400
        conn = create_connection()
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

            # Insert new user with bio
            cursor.execute("""
                INSERT INTO user_profiles (name, email, password, vector, interests, lunch_time, profile_picture, bio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, password, vector_blob, interests, lunch_time, profile_picture_path, bio))
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
    conn = create_connection()
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

@app.route('/api/user_data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = create_connection()
    with conn.cursor() as cursor:
        # Fetch the user's profile data, including bio
        cursor.execute("""
            SELECT id, name, email, interests, lunch_time, location, bio, profile_picture
            FROM user_profiles
            WHERE email = %s AND password = %s
        """, (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 404

    user_data = {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "interests": user[3],
        "lunch_time": user[4],
        "location": user[5],
        "bio": user[6],  # Include bio in the response
        "profile_picture": user[7] if user[7] else None  # Add profile picture if it exists
    }

    return jsonify(user_data), 200

    
@app.route('/api/user-count', methods=['POST'])
def user_count():
    """Return the total count of users."""
    try:
        conn = create_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM user_profiles")
            count = cursor.fetchone()[0]
        return jsonify({"user_count": count}), 200
    except Exception as e:
        print(f"Error fetching user count: {e}")
        return jsonify({"error": "Failed to fetch user count."}), 500


# --- API to Fetch Profile Picture ---
@app.route('/api/profile-picture', methods=['GET'])
def get_profile_picture():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    conn = create_connection()
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

import numpy as np

def generate_conversation_starter(bio1, bio2, interests1, interests2):
    common_interests = interests1.intersection(interests2)
    if common_interests:
        interest = random.choice(list(common_interests))
        return f"Both of you are interested in {interest}. What got you into it?"

    if bio1 and bio2:
        return f"You both seem really passionate. {bio1.split('.')[0]}. How does that align with your goals?"

    return "What do you usually enjoy discussing during lunch?"


import random

def generate_conversation_starter(bio1, bio2, interests1, interests2):
    """Generates a conversation starter based on bios and common interests."""
    common_interests = interests1.intersection(interests2)
    if common_interests:
        interest = random.choice(list(common_interests))
        return f"Both of you are interested in {interest}. What got you into it?"

    if bio1 and bio2:
        return f"You both seem passionate! {bio1.split('.')[0]}. What inspires you to keep going?"

    return "What do you usually enjoy discussing during lunch?"

@app.route('/api/matches', methods=['POST'])
def get_matches():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, interests, vector, lunch_time, location, bio FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        current_user = cursor.fetchone()

    if not current_user:
        return jsonify({"error": "Invalid email or password"}), 404

    current_user_vector = np.frombuffer(current_user[3], dtype=np.float32)
    current_user_location = current_user[5]
    current_user_bio = current_user[6]

    conn = create_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, email, interests, vector, lunch_time, location, bio FROM user_profiles")
        users = cursor.fetchall()

    user_data = []
    for u in users:
        vector = np.frombuffer(u[4], dtype=np.float32)
        user_data.append({
            "id": u[0],
            "name": u[1],
            "email": u[2],
            "interests": u[3].lower().split(", "),
            "vector": vector,
            "lunch_time": u[5],
            "location": u[6],
            "bio": u[7]
        })

    matches = []
    most_similar_user = None
    highest_similarity = 0.0

    for other_user in user_data:
        if current_user[0] == other_user["id"]:
            continue

        if current_user[4] != other_user["lunch_time"]:
            continue

        if current_user_location != other_user["location"]:
            continue

        current_interests = set(current_user[2].lower().split(", "))
        other_interests = set(other_user["interests"])
        common_interests = list(current_interests.intersection(other_interests))

        similarity = np.dot(current_user_vector, other_user["vector"]) / (
            np.linalg.norm(current_user_vector) * np.linalg.norm(other_user["vector"])
        )

        similarity = float(similarity)

        if common_interests:
            matches.append({
                "match_name": other_user["name"],
                "email": other_user["email"],
                "bio": other_user["bio"],
                "common_interests": common_interests,
                "similarity": round(similarity, 2),
                "lunch_time": current_user[4],
                "location": current_user_location
            })

            if similarity > highest_similarity:
                highest_similarity = similarity
                most_similar_user = other_user

    # Generate conversation starter based on common interests and bios
    conversation_starter = None
    if most_similar_user:
        conversation_starter = generate_conversation_starter(
            current_user_bio, most_similar_user["bio"], current_interests, other_interests
        )

        most_similar_info = {
            "id": most_similar_user["id"],
            "name": most_similar_user["name"],
            "email": most_similar_user["email"],
            "similarity": round(highest_similarity, 2),
            "conversation_starter": conversation_starter
        }

        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE user_profiles
                SET most_similar_matches = %s
                WHERE email = %s
            """, (json.dumps(most_similar_info), email))
            conn.commit()

    return jsonify({
        "matches": matches,
        "most_similar_user": most_similar_info if most_similar_user else None,
        "conversation_starter": conversation_starter
    }), 200







@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    new_status = data.get('status')  # Accepts "active" or "inactive"

    if new_status not in ["active", "inactive"]:
        return jsonify({"error": "Invalid status value. Use 'active' or 'inactive'"}), 400
    conn = create_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 404
    with conn.cursor() as cursor:
        cursor.execute("UPDATE user_profiles SET status = %s WHERE email = %s", (new_status, email))
        conn.commit()

    return jsonify({"message": f"User status updated to '{new_status}'"}), 200

@app.route('/api/update-lunch-time', methods=['POST'])
def update_lunch_time():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    new_lunch_time = data.get('lunch_time')  # e.g., "12:00 PM"

    # Validate input
    if not new_lunch_time:
        return jsonify({"error": "Lunch time is required"}), 400
    conn = create_connection()
    # Verify user with email and password
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 404
    conn = create_connection()
    # Update lunch time
    with conn.cursor() as cursor:
        cursor.execute("UPDATE user_profiles SET lunch_time = %s WHERE email = %s", (new_lunch_time, email))
        conn.commit()
        

    return jsonify({"message": f"Lunch time updated to '{new_lunch_time}'"}), 200



# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True)
