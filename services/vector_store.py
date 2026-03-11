import os
from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain_core.documents import Document
from .embedding_service import get_embedding_model
from django.conf import settings

# Initialize Chroma directory in django root
CHROMA_PERSIST_DIR = os.path.join(settings.BASE_DIR, 'chroma_db')

def get_vector_store():
    """
    Returns the persistent ChromaDB vector store instance.
    """
    embeddings = get_embedding_model()
    return Chroma(
        collection_name="codebase_collection",
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR
    )

def store_chunks(chunks: List[Dict[str, Any]]):
    """
    Takes a list of chunks and stores them into ChromaDB.
    """
    vector_store = get_vector_store()
    
    documents = []
    for chunk in chunks:
        doc = Document(
            page_content=chunk['page_content'],
            metadata=chunk['metadata']
        )
        documents.append(doc)
        
    if documents:
        vector_store.add_documents(documents)

def retrieve_context(query: str, repo_id: str, k: int = 5) -> List[Document]:
    """
    Retrieves the most semantically similar code chunks for a given query and repo_id.
    """
    vector_store = get_vector_store()
    
    # Filter by repo_id in metadata
    filter_dict = {"repo_id": repo_id}
    
    results = vector_store.similarity_search(query, k=k, filter=filter_dict)
    return results
