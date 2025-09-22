import requests

def fetch_products(api_url):
    """Fetches all products from the given API URL."""
    print(f"Fetching products from: {api_url}...")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        products = response.json()
        print(f"Successfully fetched {len(products)} products.")
        return products
    except requests.exceptions.RequestException as e:
        print(f"Error fetching products: {e}")
        return None
