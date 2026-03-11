# import os
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# def get_embedding_model():
#     """
#     Returns the configured embedding model for Langchain.
#     We are using the Gemini API for embeddings because running local HuggingFace 
#     models via PyTorch exceeds the 512MB RAM limit on Render's free tier.
#     """
#     gemini_api_key = os.getenv('GEMINI_API_KEY')
#     return GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001", 
#         google_api_key=gemini_api_key
#     )

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embedding_model():
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    return GoogleGenerativeAIEmbeddings(
        model="embedding-001",
        google_api_key=gemini_api_key
    )
