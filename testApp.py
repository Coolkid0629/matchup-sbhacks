import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import create_tables, conn
from embedding_utils import get_embedding
import struct

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# --- Create Tables ---
create_tables()

# --- API to Handle Signup ---
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    interests = data.get('interests')
    lunch_time = data.get('lunch_time')

    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM user_profiles WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 400

    vector = get_embedding(interests)
    vector_blob = struct.pack(f'{len(vector)}f', *vector)

    sql = """
    INSERT INTO user_profiles (name, email, password, vector, interests, lunch_time, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with conn.cursor() as cursor:
        cursor.execute(sql, (name, email, password, vector_blob, interests, lunch_time, 'active'))
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

# --- API to Get User Data ---
@app.route('/api/user-data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, email, interests, lunch_time FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 404

    user_data = {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "interests": user[3],
        "lunch_time": user[4],
    }
    return jsonify(user_data), 200

# --- API to Get Matches ---
@app.route('/api/matches', methods=['POST'])
def get_matches():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Verify user credentials
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, interests, vector, lunch_time FROM user_profiles WHERE email = %s AND password = %s", (email, password))
        current_user = cursor.fetchone()

    if not current_user:
        return jsonify({"error": "Invalid email or password"}), 404

    import numpy as np

    # Fetch all users to find matches
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, interests, vector, lunch_time FROM user_profiles")
        users = cursor.fetchall()

    user_data = [{"id": u[0], "name": u[1], "interests": u[2].lower().split(", "), "vector": np.frombuffer(u[3], dtype=np.float32).tolist(), "lunch_time": u[4]} for u in users]

    matches = []
    for other_user in user_data:
        if current_user[0] == other_user["id"]:
            continue  # Skip if it's the same user

        if current_user[4] != other_user["lunch_time"]:
            continue  # Skip if lunch times don't match

        # Calculate similarity and common interests
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

# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True)
