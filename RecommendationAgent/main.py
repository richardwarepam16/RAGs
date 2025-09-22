from indexer.config import FAKE_STORE_API_URL, FAISS_INDEX_PATH
from indexer.fetch import fetch_products
from indexer.index import create_faiss_index
from indexer.storage import save_faiss_index, load_faiss_index

if __name__ == "__main__":
    # Step 1: Fetch products
    products = fetch_products(FAKE_STORE_API_URL)

    if products:
        # Step 2: Create FAISS index
        db = create_faiss_index(products)


        if db:
            # Step 3: Save index
            save_faiss_index(db, FAISS_INDEX_PATH)

            print("\nFAISS indexing complete!")
            print(f"Index saved at '{FAISS_INDEX_PATH}'.")

            # Step 4: Test loading + search
            loaded_db = load_faiss_index(FAISS_INDEX_PATH)
            if loaded_db:
                query = "men's casual t-shirt"
                print(f"\nSearching for: {query}")
                results = loaded_db.similarity_search_with_score(query, k=3)

                for doc, score in results:
                    print(f"Score: {score:.4f}")
                    print(f"Title: {doc.metadata.get('title')}")
                    print(f"Price: ${doc.metadata.get('price'):.2f}")
                    print(f"Category: {doc.metadata.get('category')}")
                    print(f"Description: {doc.metadata.get('description', '')[:100]}...")
                    print("-" * 20)
