from flask import Flask, request, redirect, url_for, session, render_template_string, jsonify
from models import create_tables
from embedding_utils import get_embedding
import json
from models import conn
import struct
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for sessions

# Create database tables
create_tables()

# Function to seed sample users (optional)
def seed_users():
    with open("sample_users.json", "r") as f:
        sample_users = json.load(f)

    with conn.cursor() as cursor:
        for user in sample_users:
            vector = get_embedding(user["interests"])
            vector_blob = struct.pack(f'{len(vector)}f', *vector)
            sql = "INSERT IGNORE INTO user_profiles (name, email, vector, interests, lunch_time, status, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (user["name"], user["email"], vector_blob, user["interests"], user["lunch_time"], 'active', 'password123'))
        conn.commit()
    print("Sample users loaded!")

# --- Routes ---
@app.route('/')
def home():
    if "user_id" in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        interests = request.form['interests']
        lunch_time = request.form['lunch_time']
        vector = get_embedding(interests)
        vector_blob = struct.pack(f'{len(vector)}f', *vector)

        with conn.cursor() as cursor:
            # Check if email is already registered
            cursor.execute("SELECT 1 FROM user_profiles WHERE email = %s", (email,))
            if cursor.fetchone():
                return "Email already exists! <a href='/signup'>Try Again</a>"

            sql = "INSERT INTO user_profiles (name, email, vector, interests, lunch_time, status, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, email, vector_blob, interests, lunch_time, 'active', password))
            conn.commit()
        return redirect(url_for('login'))
    
    return '''
    <h1>Signup</h1>
    <form method="POST">
        Name: <input type="text" name="name" required><br>
        Email: <input type="email" name="email" required><br>
        Password: <input type="password" name="password" required><br>
        Interests (comma-separated): <input type="text" name="interests" required><br>
        Lunch Time: <input type="text" name="lunch_time" required><br>
        <button type="submit">Sign Up</button>
    </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name FROM user_profiles WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user[0]
                session['name'] = user[1]
                return redirect(url_for('dashboard'))
            else:
                return "Invalid login credentials! <a href='/login'>Try Again</a>"
    
    return '''
    <h1>Login</h1>
    <form method="POST">
        Email: <input type="email" name="email" required><br>
        Password: <input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    <a href="/signup">Don't have an account? Sign up here</a>
    '''

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect(url_for('login'))

    user_name = session['name']
    return f'''
    <h1>Welcome, {user_name}!</h1>
    <p><a href="/matches">View your lunch matches</a></p>
    <p><a href="/logout">Logout</a></p>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/matches")
def display_matches():
    if "user_id" not in session:
        return redirect(url_for('login'))

    import numpy as np

    # Retrieve current user
    user_id = session["user_id"]
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, interests, vector FROM user_profiles")
        users = cursor.fetchall()

    user_data = [{"id": u[0], "name": u[1], "interests": u[2], "vector": np.frombuffer(u[3], dtype=np.float32).tolist()} for u in users]
    matches = []
    matched_pairs = set()

    for current_user in user_data:
        if current_user["id"] != user_id:
            continue

        best_match = None
        best_similarity = -1

        for other_user in user_data:
            if current_user["id"] == other_user["id"]:
                continue

            pair = tuple(sorted([current_user["id"], other_user["id"]]))
            if pair in matched_pairs:
                continue

            similarity = np.dot(current_user["vector"], other_user["vector"]) / (
                np.linalg.norm(current_user["vector"]) * np.linalg.norm(other_user["vector"])
            )

            if similarity > best_similarity:
                current_interests = set(current_user["interests"].split(", "))
                other_interests = set(other_user["interests"].split(", "))
                common_interests = list(current_interests.intersection(other_interests))
                best_match = {
                    "name": other_user["name"],
                    "common_interests": common_interests,
                    "similarity": similarity,
                    "match_id": other_user["id"]
                }
                best_similarity = similarity

        if best_match:
            matches.append({
                "user": current_user["name"],
                "match": best_match["name"],
                "common_interests": best_match["common_interests"],
                "similarity": best_similarity,
            })
            matched_pairs.add((current_user["id"], best_match["match_id"]))

    return jsonify(matches)

# Run the app
if __name__ == "__main__":
    with app.app_context():
        seed_users()
    app.run(debug=True)
