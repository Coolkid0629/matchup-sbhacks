import singlestoredb as s2
from config import SINGLESTORE_CONFIG
import json
import os
from embedding_utils import get_embedding
import struct

# Connect to SingleStore
conn = s2.connect(host='svc-2d85fc18-3a17-4bcf-800c-160f3fd4e87a-dml.gcp-virginia-1.svc.singlestore.com', port='3306', user='admin',
                  password='eifmxUSGhaKzGkgDcw6s4iyyr3wcS6WW', database='lunchLink')

SAMPLE_USERS_FILE = "sample_users.json"

def create_tables():
    with conn.cursor() as cursor:
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS lunchLink;")
        cursor.execute("USE lunchLink;")
        cursor.execute("DROP TABLE IF EXISTS user_profiles;")
        create_users_table = """
        CREATE ROWSTORE TABLE user_profiles (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            email VARCHAR(200) NOT NULL,
            password VARCHAR(200) NOT NULL,
            vector BLOB,
            interests TEXT,
            lunch_time VARCHAR(50) NULL,
            status VARCHAR(20) DEFAULT 'active',
            profile_picture VARCHAR(255),  -- Column to store the profile picture path
            UNIQUE KEY (id, email)
        );
        """
        
        
        cursor.execute(create_users_table)
        
        conn.commit()

        load_sample_users()

        

        

def load_sample_users():
    if not os.path.exists(SAMPLE_USERS_FILE):
        print(f"{SAMPLE_USERS_FILE} not found!")
        return

    print(f"Loading users from {SAMPLE_USERS_FILE}")
    with open(SAMPLE_USERS_FILE, "r") as f:
        sample_users = json.load(f)

    if not sample_users:
        print("No users found in sample_users.json")
        return

    with conn.cursor() as cursor:
        for user in sample_users:
            print(f"Processing user: {user['email']}")
            cursor.execute("SELECT 1 FROM user_profiles WHERE email = %s", (user["email"],))
            if cursor.fetchone():
                print(f"User {user['email']} already exists. Skipping.")
                continue

            try:
                vector = get_embedding(user["interests"])
                vector_blob = struct.pack(f'{len(vector)}f', *vector)
            except Exception as e:
                print(f"Embedding failed for {user['email']}: {e}")
                vector_blob = struct.pack(f'768f', *[0.0] * 768)

            sql = "INSERT INTO user_profiles (name, email, password, vector, interests, lunch_time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (user["name"], user["email"], user["password"], vector_blob, user["interests"], user["lunch_time"], 'active'))
            conn.commit()

    print("Sample users loaded successfully!")

if __name__ == "__main__":
    create_tables()
    load_sample_users()
