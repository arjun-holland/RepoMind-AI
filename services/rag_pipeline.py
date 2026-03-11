import os
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from .vector_store import retrieve_context

def get_llm():
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    # Using 'gemini-2.5-flash' which is universally available on the free tier API
    return ChatGoogleGenerativeAI(google_api_key=gemini_api_key, model="gemini-2.5-flash", temperature=0)

RAG_SYSTEM_PROMPT = """
You are a senior codebase AI assistant. 
You are given code snippets from a repository. Answer questions using only the provided context. If you cannot find the answer, say "I could not find the answer in the indexed code."
Always reference file names or paths when discussing code.

REPOSITORY CODE CONTEXT:
{context}

USER QUESTION:
"""

def generate_answer(query: str, repo_id: str) -> Dict[str, Any]:
    """
    Generates an answer to the query based on the specific repository.
    """
    # 1. Retrieve context
    context_docs = retrieve_context(query, repo_id, k=6)
    
    formatted_context = ""
    file_references = set()
    
    for doc in context_docs:
        meta = doc.metadata
        file_path = meta.get('file_path', 'Unknown file')
        file_references.add(file_path)
        
        # Pull out our AST metadata!
        classes = meta.get("classes", "")
        functions = meta.get("functions", "")
        
        ast_info = ""
        if classes or functions:
             ast_info = f"[Found Classes: {classes} | Found Functions: {functions}]\n"
        
        formatted_context += f"--- FILE: {file_path} ---\n{ast_info}{doc.page_content}\n\n"
        
    # 2. Setup LLM and Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_PROMPT),
        ("human", "{question}")
    ])
    
    llm = get_llm()
    chain = prompt | llm
    
    # 3. Generate response
    response = chain.invoke({
        "context": formatted_context,
        "question": query
    })
    
    return {
        "answer": response.content,
        "references": list(file_references)
    }
