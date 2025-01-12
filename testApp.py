import os
import json
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from models import create_tables, conn
from embedding_utils import get_embedding
import struct

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# --- Create Tables ---
create_tables()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder for profile pictures if not exists

# --- API to Handle Signup ---
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    interests = data.get('interests')
    lunch_time = data.get('lunch_time')
    profile_picture_data = data.get('profile_picture')  # Base64 encoded string

    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM user_profiles WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 400

    vector = get_embedding(interests)
    vector_blob = struct.pack(f'{len(vector)}f', *vector)

    # Save profile picture if provided
    profile_picture_path = None
    if profile_picture_data:
        picture_filename = f"{email}_profile.png"
        profile_picture_path = os.path.join(UPLOAD_FOLDER, picture_filename)
        with open(profile_picture_path, "wb") as f:
            f.write(base64.b64decode(profile_picture_data))

    sql = """
    INSERT INTO user_profiles (name, email, password, vector, interests, lunch_time, status, profile_picture)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (name, email, password, vector_blob, interests, lunch_time, 'active', profile_picture_path))
        conn.commit()

    return jsonify({"message": "User registered successfully"}), 201

# --- API to Handle Login ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, email FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid login credentials"}), 401

    user_data = {
        "id": user[0],
        "name": user[1],
        "email": user[2],
    }
    return jsonify(user_data), 200

# --- API to Fetch User Data ---
#on principle this should not be a POST routine but i think we are kinda stuck with it ATP 
@app.route('/api/user-data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # i love sql :0
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
