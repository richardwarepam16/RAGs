import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from .config import OPENAI_MODEL_NAME, TOP_K_RETRIEVAL, TOP_K_RERANK
from .filters import parse_query_filters
from .formatter import format_products_for_llm
from .utils import load_faiss_index

load_dotenv()

class RecommendationAgent:
    def __init__(self):
        if os.getenv("OPENAI_API_KEY") is None:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        self.faiss_db = load_faiss_index()
        self.llm = ChatOpenAI(model_name=OPENAI_MODEL_NAME, temperature=0.2)

        self.rerank_prompt = PromptTemplate(
            input_variables=["user_query", "retrieved_products_str", "filter_details"],
            template="""You are an expert e-commerce product recommender.
            The user is looking for: "{user_query}".
            Constraints: {filter_details}
            
            Here are {top_k_retrieval} candidate products:
            {retrieved_products_str}
            
            Re-rank by relevance to the query & constraints.
            Return ONLY the Product IDs, comma-separated.
            
            Top {top_k_rerank} IDs:"""
        ).partial(
            top_k_retrieval=TOP_K_RETRIEVAL,
            top_k_rerank=TOP_K_RERANK
        )

        self.rerank_chain = self.rerank_prompt | self.llm | StrOutputParser()

    def recommend(self, query: str):
        filters, cleaned_query = parse_query_filters(query)
        filter_details_str = f"Max Price: ${filters['max_price']:.2f}" if 'max_price' in filters else "None"

        retrieved_docs = self.faiss_db.similarity_search(cleaned_query, k=TOP_K_RETRIEVAL)
        retrieved_products = [doc.metadata for doc in retrieved_docs]

        if 'max_price' in filters:
            retrieved_products = [
                p for p in retrieved_products if p.get('price', 0) <= filters['max_price']
            ]
            if not retrieved_products:
                return []

        products_for_llm_str = format_products_for_llm(retrieved_products)
        if not products_for_llm_str:
            return []

        reranked_ids_str = self.rerank_chain.invoke({
            "user_query": query,
            "retrieved_products_str": products_for_llm_str,
            "filter_details": filter_details_str
        })

        reranked_ids = [id.strip() for id in reranked_ids_str.split(',') if id.strip()]
        product_id_map = {str(p['id']): p for p in retrieved_products}

        final_recommendations = []
        for prod_id in reranked_ids:
            if prod_id in product_id_map and product_id_map[prod_id] not in final_recommendations:
                final_recommendations.append(product_id_map[prod_id])
            if len(final_recommendations) >= TOP_K_RERANK:
                break

        return final_recommendations
