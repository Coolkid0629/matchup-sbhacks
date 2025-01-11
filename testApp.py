import json
from flask import Flask, request, session, redirect, url_for, render_template_string, jsonify
from models import create_tables, conn
from embedding_utils import get_embedding
import struct
import os
from datetime import datetime
import pytz

# PST time zone
PST = pytz.timezone('America/Los_Angeles')
SAMPLE_USERS_FILE = "sample_users.json"

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Create database tables
create_tables()

def load_sample_users():
    """Load users from sample_users.json at startup."""
    if os.path.exists(SAMPLE_USERS_FILE):
        with open(SAMPLE_USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_sample_users(users):
    """Save the updated user list to sample_users.json."""
    with open(SAMPLE_USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def is_email_unique(email):
    """Check if an email is unique."""
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 FROM user_profiles WHERE email = %s", (email,))
        return cursor.fetchone() is None
    
def round_to_nearest_quarter_hour(time_obj):
    """Round time to the nearest quarter-hour."""
    minute = time_obj.minute
    if minute < 8:
        rounded_minute = 0
    elif minute < 23:
        rounded_minute = 15
    elif minute < 38:
        rounded_minute = 30
    elif minute < 53:
        rounded_minute = 45
    else:
        rounded_minute = 0
        time_obj = time_obj.replace(hour=(time_obj.hour + 1) % 24)

    return time_obj.replace(minute=rounded_minute, second=0, microsecond=0)


def parse_lunch_time(lunch_time_str):
    """Parse lunch time string and convert it to rounded PST time."""
    if lunch_time_str is None:
        return "N/A"

    try:
        time_obj = datetime.strptime(lunch_time_str.strip().lower(), "%I:%M %p")
    except ValueError:
        try:
            time_obj = datetime.strptime(lunch_time_str.strip().lower(), "%I %p")
        except ValueError:
            return "Invalid Time"

    # Convert to PST and round to the nearest quarter-hour
    time_obj = time_obj.astimezone(PST)
    rounded_time = round_to_nearest_quarter_hour(time_obj)
    return rounded_time.strftime("%I:%M %p")


# --- Signup Route ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        interests = request.form['interests']
        lunch_time = request.form['lunch_time']

        if not is_email_unique(email):
            return f"Email {email} already exists. Please use a different email."

        # Convert lunch time and interests
        formatted_lunch_time = parse_lunch_time(lunch_time)
        vector = get_embedding(interests)
        vector_blob = struct.pack(f'{len(vector)}f', *vector)

        # Add user to the database
        with conn.cursor() as cursor:
            sql = "INSERT INTO user_profiles (name, email, password, vector, interests, lunch_time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, email, password, vector_blob, interests, formatted_lunch_time, 'active'))
            conn.commit()

        # Save to sample_users.json
        sample_users = load_sample_users()
        new_user = {
            "name": name,
            "email": email,
            "password": password,
            "interests": interests,
            "lunch_time": formatted_lunch_time
        }
        sample_users.append(new_user)
        save_sample_users(sample_users)

        lunch_time = request.form['lunch_time']
        if not lunch_time:
            return "Lunch time is required! <a href='/signup'>Try Again</a>"

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

# --- Login Route ---
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

# --- Dashboard Route ---
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

# --- Matches Route ---
@app.route("/matches")
def display_matches():
    if "user_id" not in session:
        return redirect(url_for('login'))

    import numpy as np

    # Retrieve logged-in user's data
    user_id = session["user_id"]
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, interests, vector, lunch_time FROM user_profiles")
        users = cursor.fetchall()

    user_data = [{"id": u[0], "name": u[1], "interests": u[2].lower().split(", "), "vector": np.frombuffer(u[3], dtype=np.float32).tolist(), "lunch_time": parse_lunch_time(u[4])} for u in users]

    matches = []
    for current_user in user_data:
        if current_user["id"] != user_id:
            continue

        best_match = None
        best_similarity = -1

        for other_user in user_data:
            if current_user["id"] == other_user["id"]:
                continue

            # Check for same lunch time
            if current_user["lunch_time"] != other_user["lunch_time"]:
                continue

            # Compare interests by splitting by commas and ignoring case
            current_interests = set(current_user["interests"])
            other_interests = set(other_user["interests"])
            common_interests = list(current_interests.intersection(other_interests))

            # Skip if no common interests
            if not common_interests:
                continue

            # Compute cosine similarity between vectors
            similarity = np.dot(current_user["vector"], other_user["vector"]) / (
                np.linalg.norm(current_user["vector"]) * np.linalg.norm(other_user["vector"])
            )

            if similarity > best_similarity:
                best_match = {
                    "name": other_user["name"],
                    "common_interests": common_interests,
                    "similarity": similarity
                }
                best_similarity = similarity

        if best_match:
            matches.append({
                "user": current_user["name"],
                "match": best_match["name"],
                "common_interests": best_match["common_interests"],
                "similarity": best_similarity,
                "lunch_time": current_user["lunch_time"]
            })

    return jsonify(matches)

# --- Logout Route ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Run the app
if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
