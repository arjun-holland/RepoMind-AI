import os
import ast
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from typing import List, Dict, Any

LANGUAGE_MAP = {
    '.py': Language.PYTHON,
    '.js': Language.JS,
    '.ts': Language.TS,
    '.java': Language.JAVA,
    '.go': Language.GO,
    '.cpp': Language.CPP,
    '.c': Language.CPP,
    '.h': Language.CPP,
    '.md': Language.MARKDOWN,
}

def get_text_splitter_for_extension(ext: str):
    language = LANGUAGE_MAP.get(ext)
    if language:
        return RecursiveCharacterTextSplitter.from_language(
            language=language, chunk_size=1000, chunk_overlap=200
        )
    return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def extract_python_ast_metadata(content: str) -> Dict[str, List[str]]:
    """
    Parses Python code and extracts class and function names using AST.
    """
    metadata = {"classes": [], "functions": []}
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                metadata["classes"].append(node.name)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                metadata["functions"].append(node.name)
    except SyntaxError:
        pass
    return metadata

def parse_code_into_chunks(files_data: List[Dict[str, str]], repo_id: str) -> List[Dict[str, Any]]:
    """
    Parses a list of file dictionaries into chunks and attaches semantic metadata.
    """
    chunks = []
    
    for file_data in files_data:
        ext = file_data['extension']
        content = file_data['content']
        splitter = get_text_splitter_for_extension(ext)
        
        ast_metadata = {"classes": [], "functions": []}
        if ext == '.py':
            ast_metadata = extract_python_ast_metadata(content)
            
        split_texts = splitter.split_text(content)
        
        for i, text in enumerate(split_texts):
            chunk = {
                "page_content": text,
                "metadata": {
                    "file_name": file_data['file_name'],
                    "file_path": file_data['file_path'],
                    "extension": ext,
                    "repo_id": repo_id,
                    "chunk_index": i,
                    # ChromaDB metadata must be strings, ints, or floats.
                    "classes": ", ".join(ast_metadata["classes"]) if ast_metadata["classes"] else "",
                    "functions": ", ".join(ast_metadata["functions"]) if ast_metadata["functions"] else ""
                }
            }
            chunks.append(chunk)
            
    return chunks
