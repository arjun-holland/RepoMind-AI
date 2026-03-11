import os
from datetime import datetime
from pymongo import MongoClient
from django.conf import settings

# Wait for MONGO_URI in settings
MONGO_URI = getattr(settings, 'MONGO_URI', os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
client = MongoClient(MONGO_URI)
db = client['ai_codebase_assistant']

repositories_collection = db['repositories']
queries_collection = db['queries']

def create_repository_record(repo_url: str) -> str:
    from django.utils.timezone import now
    record = {
        "repo_url": repo_url,
        "status": "pending",
        "created_at": now(),
        "updated_at": now()
    }
    result = repositories_collection.insert_one(record)
    return str(result.inserted_id)

def update_repository_status(record_id: str, status: str, repo_id: str = None, error: str = None):
    from bson.objectid import ObjectId
    from django.utils.timezone import now
    
    update_data = {
        "status": status,
        "updated_at": now()
    }
    if repo_id:
        update_data["repo_id"] = repo_id
    if error:
        update_data["error"] = error
        
    repositories_collection.update_one(
        {"_id": ObjectId(record_id)},
        {"$set": update_data}
    )

def get_repository_status(record_id: str) -> dict:
    from bson.objectid import ObjectId
    record = repositories_collection.find_one({"_id": ObjectId(record_id)})
    if record:
        record['_id'] = str(record['_id'])
    return record

def get_repository_by_url(repo_url: str) -> dict:
    record = repositories_collection.find_one({"repo_url": repo_url, "status": "ready"})
    if record:
        record['_id'] = str(record['_id'])
    return record

def log_query(query: str, repo_id: str, answer: str, references: list):
    from django.utils.timezone import now
    record = {
        "query": query,
        "repo_id": repo_id,
        "answer": answer,
        "references": references,
        "timestamp": now()
    }
    queries_collection.insert_one(record)
