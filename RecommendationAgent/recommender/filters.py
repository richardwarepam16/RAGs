import re

def parse_query_filters(query: str):
    """
    Parses a user query to extract filters (e.g., max_price).
    Returns filters + cleaned query.
    """
    filters = {}
    cleaned_query = query.lower()

    price_match = re.search(
        r'(under|max|less than|cheaper than|below)\s*\$?(\d+(\.\d{1,2})?)',
        cleaned_query
    )
    if price_match:
        try:
            price_limit = float(price_match.group(2))
            filters['max_price'] = price_limit
            cleaned_query = re.sub(
                r'(under|max|less than|cheaper than|below)\s*\$?(\d+(\.\d{1,2})?)',
                '',
                cleaned_query
            ).strip()
        except ValueError:
            pass

    return filters, cleaned_query.strip()
