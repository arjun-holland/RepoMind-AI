import os

SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.go', '.cpp', '.c', '.h', '.json', '.yaml', '.yml', '.md'}
IGNORED_DIRS = {'.git', 'node_modules', 'venv', 'env', 'build', 'dist', '__pycache__', '.idea', '.vscode'}

def extract_files(repo_path: str):
    """
    Walks the directory and yields file contents and metadata for supported extensions.
    """
    for root, dirs, files in os.walk(repo_path):
        # Modify dirs in-place to avoid unneeded traversal
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, repo_path)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    yield {
                        "file_name": file,
                        "file_path": relative_path,
                        "extension": ext,
                        "content": content
                    }
                except (UnicodeDecodeError, IOError):
                    continue
