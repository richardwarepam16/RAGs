import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from .config import FAISS_INDEX_PATH

def load_faiss_index(path=FAISS_INDEX_PATH):
    """Loads FAISS index from local path."""
    if not os.path.exists(path):
        raise RuntimeError(f"FAISS index not found at {path}. Run indexing first.")

    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
