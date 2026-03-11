import threading
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models.repository_model import (
    create_repository_record, 
    update_repository_status, 
    get_repository_status,
    get_repository_by_url,
    log_query
)
from services.github_service import clone_repository, delete_repository
from utils.file_loader import extract_files
from services.code_parser import parse_code_into_chunks
from services.vector_store import store_chunks
from services.rag_pipeline import generate_answer

def ingest_repository_background(record_id: str, repo_url: str):
    """
    Background task to clone, parse, and index the repository.
    """
    repo_path = None
    try:
        update_repository_status(record_id, status="cloning")
        clone_data = clone_repository(repo_url)
        repo_id = clone_data['repo_id']
        repo_path = clone_data['repo_path']
        
        update_repository_status(record_id, status="parsing", repo_id=repo_id)
        files_data = list(extract_files(repo_path))
        
        chunks = parse_code_into_chunks(files_data, repo_id=repo_id)
        
        update_repository_status(record_id, status="indexing", repo_id=repo_id)
        store_chunks(chunks)
        
        update_repository_status(record_id, status="ready", repo_id=repo_id)
        
    except Exception as e:
        update_repository_status(record_id, status="failed", error=str(e))
    finally:
        if repo_path:
            delete_repository(repo_path)


class IngestRepositoryView(APIView):
    def post(self, request):
        repo_url = request.data.get('repo_url')
        if not repo_url:
            return Response({"error": "repo_url is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        existing = get_repository_by_url(repo_url)
        if existing:
            return Response({
                "message": "Repository already indexed",
                "record_id": existing['_id'],
                "repo_id": existing['repo_id']
            }, status=status.HTTP_200_OK)
            
        record_id = create_repository_record(repo_url)
        
        thread = threading.Thread(target=ingest_repository_background, args=(record_id, repo_url))
        thread.start()
        
        return Response({
            "message": "Repository indexing started",
            "record_id": record_id
        }, status=status.HTTP_202_ACCEPTED)

class RepositoryStatusView(APIView):
    def get(self, request):
        record_id = request.query_params.get('record_id')
        if not record_id:
            return Response({"error": "record_id query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        record = get_repository_status(record_id)
        if not record:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(record, status=status.HTTP_200_OK)

class QueryCodebaseView(APIView):
    def post(self, request):
        query = request.data.get('query')
        repo_url = request.data.get('repo_url')
        repo_id = request.data.get('repo_id')
        
        if not query:
            return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not repo_id and not repo_url:
            return Response({"error": "Either repo_id or repo_url is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not repo_id:
            repo_record = get_repository_by_url(repo_url)
            if not repo_record:
                return Response({"error": "Repository not found or not fully indexed yet"}, status=status.HTTP_404_NOT_FOUND)
            repo_id = repo_record['repo_id']
            
        try:
            result = generate_answer(query, repo_id)
            log_query(query, repo_id, result['answer'], result['references'])
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
