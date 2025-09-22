from recommender.agent import RecommendationAgent
from recommender.formatter import display_recommendations

if __name__ == "__main__":
    try:
        agent = RecommendationAgent()
        print("Recommendation Agent Ready! Type 'exit' to quit.")
        while True:
            query = input("\nYour query: ")
            if query.lower() == "exit":
                break
            results = agent.recommend(query)
            display_recommendations(results, query)
    except Exception as e:
        print(f"Error: {e}")
