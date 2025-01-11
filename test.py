import json
import numpy as np

# Load sample data
with open("sample_users.json", "r") as file:
    users = json.load(file)

# Function to calculate cosine similarity
def cosine_similarity(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Mock embedding function (for testing purposes)
def mock_embedding(interests):
    return [len(word) for word in interests.split(", ")]

# Pad vectors to the same length
def pad_vector(vector, length):
    return vector + [0] * (length - len(vector))

# Generate embeddings and pad
max_length = 0
for user in users:
    user["vector"] = mock_embedding(user["interests"])
    max_length = max(max_length, len(user["vector"]))

for user in users:
    user["vector"] = pad_vector(user["vector"], max_length)

# Perform matches
matches = []
for current_user in users:
    best_match = None
    best_similarity = -1
    current_vector = current_user["vector"]

    for other_user in users:
        if current_user["email"] != other_user["email"]:
            similarity = cosine_similarity(current_vector, other_user["vector"])
            if similarity > best_similarity:
                # Find common interests
                current_interests = set(current_user["interests"].split(", "))
                other_interests = set(other_user["interests"].split(", "))
                common_interests = list(current_interests.intersection(other_interests))

                best_match = {
                    "name": other_user["name"],
                    "common_interests": common_interests,
                    "similarity": similarity
                }
                best_similarity = similarity

    matches.append({
        "user": current_user["name"],
        "match": best_match["name"] if best_match else "No match",
        "common_interests": best_match["common_interests"] if best_match else [],
        "similarity": best_similarity if best_match else 0.0
    })

# Save matches to a file
with open("matches.json", "w") as file:
    json.dump(matches, file, indent=4)

print("Matches saved to matches.json")
