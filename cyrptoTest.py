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
    """Creates a new Solana wallet and returns the public key and seed phrase (for recovery)."""
    try:
        # Run Solana keygen command with a timeout to avoid hanging processes
        result = subprocess.run(
            ["solana-keygen", "new", "--no-outfile"],
            capture_output=True,
            text=True,
            timeout=10  # Timeout after 10 seconds if Solana keygen hangs
        )
        
        # Parse the command output
        lines = result.stdout.splitlines()
        pubkey = next((line.split(": ")[1] for line in lines if line.startswith("pubkey")), None)
        seed_phrase = next((line.split(": ")[1] for line in lines if "seed phrase" in line.lower()), None)

        if not pubkey or not seed_phrase:
            print("Error: Solana keygen output missing expected lines.")
            return None, None

        # Warning: Do not print the seed phrase in production logs!
        print(f"Public key created: {pubkey}")

        return pubkey, seed_phrase

    except subprocess.TimeoutExpired:
        print("Error: Solana keygen timed out. Ensure Solana CLI is installed and configured.")
        return None, None
    except Exception as e:
        print(f"Unexpected error during wallet creation: {e}")
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
        bio = data.get('bio', '')  # Optional short bio, defaults to empty string if not provided

        #wallet_public_key, wallet_secret_key = create_user_wallet()
        # Temporary placeholder wallet keys
        wallet_public_key = "TEMP_PUBLIC_KEY_12345"
        wallet_secret_key = "TEMP_SECRET_KEY_12345"

        if not all([name, email, password, interests]):
            return jsonify({"error": "All fields except lunch time, bio, and profile picture are required!"}), 400

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
            INSERT INTO user_profiles (email, name, password, interests, lunch_time, bio, wallet_public_key, wallet_secret_key)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (email, name, password, interests, lunch_time, bio, wallet_public_key, wallet_secret_key))
            conn.commit()

        return jsonify({"message": "Signup successful!", "wallet_public_key": wallet_public_key}), 201

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
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Check if email and password are provided
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400

        # Query the database for the user
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT name, email, interests, lunch_time, profile_picture, status 
                FROM user_profiles WHERE email = %s AND password = %s
            """, (email, password))
            user = cursor.fetchone()

        if not user:
            return jsonify({"message": "Invalid email or password."}), 401

        # Build the user data response
        user_data = {
            "name": user[0],
            "email": user[1],
            "interests": user[2],
            "lunch_time": user[3] or "Not Set",
            "profile_picture": user[4] or "No profile picture",
            "status": user[5] or "active"  # Default to "active" if not set
        }

        return jsonify(user_data), 200

    except Exception as e:
        print(f"Error fetching user data: {e}")
        return jsonify({"message": "An error occurred."}), 500


@app.route('/api/user-count', methods=['POST'])
def user_count():
    """Return the total count of users."""
    try:
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

import numpy as np

@app.route('/api/matches', methods=['POST'])
def get_matches():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Fetch the current user
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, interests, vector, lunch_time, bio, wallet_public_key 
            FROM user_profiles WHERE email = %s AND password = %s
        """, (email, password))
        current_user = cursor.fetchone()

    if not current_user:
        return jsonify({"error": "Invalid email or password"}), 404

    current_user_id, current_name, current_interests, current_vector_blob, current_lunch_time, current_bio, current_wallet_public_key = current_user
    current_user_vector = np.frombuffer(current_vector_blob, dtype=np.float32)
    current_user_bio = current_bio or ""  # Handle missing bio

    # Generate bio embedding
    current_user_bio_vector = get_embedding(current_user_bio)

    # Fetch all other users
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, interests, vector, lunch_time, bio, wallet_public_key 
            FROM user_profiles
        """)
        users = cursor.fetchall()

    user_data = []
    for user in users:
        other_user_id, other_name, other_interests, other_vector_blob, other_lunch_time, other_bio, other_wallet_public_key = user
        if current_user_id == other_user_id:
            continue  # Skip matching the user with themselves

        # Handle vector and bio embedding
        other_user_vector = np.frombuffer(other_vector_blob, dtype=np.float32)
        other_user_bio_vector = get_embedding(other_bio or "")

        user_data.append({
            "id": other_user_id,
            "name": other_name,
            "interests": other_interests.lower().split(", "),
            "vector": other_user_vector,
            "lunch_time": other_lunch_time,
            "bio_vector": other_user_bio_vector,
            "wallet_public_key": other_wallet_public_key
        })

    matches = []
    for other_user in user_data:
        if current_lunch_time != other_user["lunch_time"]:
            continue  # Skip if lunch times do not match

        # Calculate common interests
        current_interest_set = set(current_interests.lower().split(", "))
        other_interest_set = set(other_user["interests"])
        common_interests = list(current_interest_set.intersection(other_interest_set))

        # Cosine similarity for interests and bio
        interests_similarity = np.dot(current_user_vector, other_user["vector"]) / (
            np.linalg.norm(current_user_vector) * np.linalg.norm(other_user["vector"])
        )
        bio_similarity = np.dot(current_user_bio_vector, other_user["bio_vector"]) / (
            np.linalg.norm(current_user_bio_vector) * np.linalg.norm(other_user["bio_vector"])
        )

        # Weighted average similarity (70% interests, 30% bio)
        combined_similarity = 0.7 * interests_similarity + 0.3 * bio_similarity

        # Convert similarities to float for JSON serialization
        interests_similarity = float(interests_similarity)
        bio_similarity = float(bio_similarity)
        combined_similarity = float(combined_similarity)

        if common_interests:
            matches.append({
                "match_name": other_user["name"],
                "common_interests": common_interests,
                "interests_similarity": round(interests_similarity, 2),
                "bio_similarity": round(bio_similarity, 2),
                "combined_similarity": round(combined_similarity, 2),
                "lunch_time": current_lunch_time
            })

            # Mint token for each match (placeholder function)
            if other_user["wallet_public_key"]:
                print(f"Minting token to {other_user['wallet_public_key']}")
                # mint_token(other_user["wallet_public_key"])  # Uncomment to mint

    if not matches:
        return jsonify({"message": "No matches found."}), 200

    return jsonify(matches), 200





@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    status = data.get('status')  # "active" or "inactive"

    if not status or status not in ['active', 'inactive']:
        return jsonify({"error": "Invalid status value. Use 'active' or 'inactive'"}), 400

    # Verify user with email and password
    with conn.cursor() as cursor:
        cursor.execute("SELECT email FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 404

    # Update user status
    with conn.cursor() as cursor:
        cursor.execute("UPDATE user_profiles SET status = %s WHERE email = %s", (status, email))
        conn.commit()

    return jsonify({"message": f"User status updated to '{status}'"}), 200


@app.route('/api/update-lunch-time', methods=['POST'])
def update_lunch_time():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    new_lunch_time = data.get('lunch_time')  # e.g., "12:00 PM"

    if not new_lunch_time:
        return jsonify({"error": "Lunch time is required"}), 400

    # Verify user with email and password
    with conn.cursor() as cursor:
        cursor.execute("SELECT email FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 404

    # Update lunch time
    with conn.cursor() as cursor:
        cursor.execute("UPDATE user_profiles SET lunch_time = %s WHERE email = %s", (new_lunch_time, email))
        conn.commit()

    return jsonify({"message": f"Lunch time updated to '{new_lunch_time}'"}), 200




# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True)
