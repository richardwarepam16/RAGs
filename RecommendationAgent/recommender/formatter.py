def format_products_for_llm(products):
    formatted_str = ""
    for product in products:
        formatted_str += (
            f"Product ID: {product.get('id', 'N/A')}\n"
            f"Title: {product.get('title', 'N/A')}\n"
            f"Price: ${product.get('price', 0):.2f}\n"
            f"Category: {product.get('category', 'N/A')}\n"
            f"Description: {product.get('description', 'N/A')[:200]}...\n"
            f"---\n"
        )
    return formatted_str

def display_recommendations(products, original_query):
    print(f"\n--- Recommendations for '{original_query}' ---")
    if not products:
        print("No recommendations found.")
        return

    for i, product in enumerate(products, 1):
        print(f"#{i}:")
        print(f"  Title: {product.get('title', 'N/A')}")
        print(f"  Price: ${product.get('price', 0):.2f}")
        print(f"  Category: {product.get('category', 'N/A')}")
        print(f"  Description: {product.get('description', 'N/A')[:150]}...")
        print(f"  Link: {product.get('image', 'N/A')}")
        print("-" * 30)
