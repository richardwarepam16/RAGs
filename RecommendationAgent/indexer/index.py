import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

load_dotenv()

def create_faiss_index(products):
    """Creates a FAISS index from product data using OpenAI embeddings."""
    if not products:
        print("No products to index. Exiting.")
        return None

    if os.getenv("OPENAI_API_KEY") is None:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return None

    print("Initializing OpenAI Embeddings...")
    embeddings = OpenAIEmbeddings()

    texts, metadatas = [], []
    for product in products:
        combined_text = (
            f"Title: {product.get('title', '')}. "
            f"Description: {product.get('description', '')}. "
            f"Category: {product.get('category', '')}. "
            f"Price: ${product.get('price', 0):.2f}"
        )
        texts.append(combined_text)
        metadatas.append(product)

    print(f"Generating embeddings for {len(texts)} products...")
    docs = [Document(page_content=t, metadata=m) for t, m in zip(texts, metadatas)]
    db = FAISS.from_documents(docs, embeddings)
    print("FAISS index created successfully.")
    return db
