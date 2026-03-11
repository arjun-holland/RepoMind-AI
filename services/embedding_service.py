from langchain_huggingface import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Returns the configured embedding model for Langchain.
    We are using a local, 100% free HuggingFace model so you don't run into API limits!
    """
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
