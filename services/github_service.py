import os
import uuid
import tempfile
import shutil
import stat
from git import Repo

def clone_repository(repo_url: str) -> dict:
    """
    Clones a GitHub repository to a temporary directory.
    Returns the repository ID (UUID) and the path to the cloned directory.
    """
    repo_id = str(uuid.uuid4())
    
    clones_dir = os.path.join(tempfile.gettempdir(), 'ai_codebase_clones')
    os.makedirs(clones_dir, exist_ok=True)
    
    repo_path = os.path.join(clones_dir, repo_id)
    
    try:
        Repo.clone_from(repo_url, repo_path)
    except Exception as e:
        if os.path.exists(repo_path):
            delete_repository(repo_path)
        raise e
        
    return {
        "repo_id": repo_id,
        "repo_path": repo_path
    }

def delete_repository(repo_path: str):
    """
    Deletes the cloned repository to free up space.
    """
    if os.path.exists(repo_path):
        def on_rm_error(func, path, exc_info):
            os.chmod(path, stat.S_IWRITE)
            func(path)
            
        shutil.rmtree(repo_path, onerror=on_rm_error)
