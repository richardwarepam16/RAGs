import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def save_faiss_index(db, path):
    """Saves FAISS index locally."""
    print(f"Saving FAISS index to: {path}...")
    db.save_local(path)
    print("Index saved.")

def load_faiss_index(path):
    """Loads FAISS index if available."""
    if not os.path.exists(path):
        print(f"Error: No FAISS index at {path}.")
        return None

    print(f"Loading FAISS index from: {path}...")
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    print("FAISS index loaded.")
    return db
