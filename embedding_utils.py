from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Pre-trained model

def get_embedding(text):
    """
    Convert text interests into vector embedding.
    Returns a list of float numbers representing the vector.
    """
    return model.encode(text).tolist()
