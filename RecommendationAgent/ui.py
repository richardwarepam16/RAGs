# ui.py
import streamlit as st
from recommender.agent import RecommendationAgent
from recommender.formatter import display_recommendations

# --- Page Setup ---
st.set_page_config(page_title="🛍️ Product Recommender", layout="wide")
st.title("🛒 AI-Powered Product Recommender")

# --- Initialize Agent ---
@st.cache_resource
def load_agent():
    try:
        return RecommendationAgent()
    except Exception as e:
        st.error(f"❌ Failed to initialize agent: {e}")
        return None

agent = load_agent()

# --- Sidebar ---
st.sidebar.header("💡 Try These Queries")
st.sidebar.markdown("""
- `mens casual t-shirt`  
- `jewelry for a gift under $200`  
- `backpack for hiking`  
- `stylish women's dress under $60`  
- `electronics for home office`  
""")
st.sidebar.info("Dataset: Fake Store API (20 demo products)")

# --- Main UI ---
if agent:
    user_query = st.text_input(
        "🔍 What are you shopping for?",
        placeholder="e.g. stylish women's dress under $60"
    )
    recommend_btn = st.button("✨ Recommend Products")

    if recommend_btn and user_query:
        with st.spinner("🔎 Finding the best matches..."):
            recommendations = agent.recommend(user_query)

        if not recommendations:
            st.warning("⚠️ No recommendations found. Try a broader query.")
        else:
            st.subheader(f"🎯 Top {len(recommendations)} Recommendations for **'{user_query}'**")

            # Grid layout
            cols = st.columns(2, gap="large")
            for i, product in enumerate(recommendations):
                with cols[i % 2]:
                    with st.container(border=True):
                        st.image(product.get("image", ""), width=220, caption=product.get("title", "N/A"))
                        st.markdown(f"**💵 Price:** ${product.get('price', 0):.2f}")
                        st.markdown(f"**📂 Category:** {product.get('category', 'N/A')}")
                        if "rating" in product:
                            rate = product["rating"].get("rate", "N/A")
                            count = product["rating"].get("count", "0")
                            st.markdown(f"**⭐ Rating:** {rate}/5 ({count} reviews)")
                        st.caption(product.get("description", "N/A")[:250] + "...")
