from django.urls import path
from .views import IngestRepositoryView, QueryCodebaseView, RepositoryStatusView

urlpatterns = [
    path('repository/ingest', IngestRepositoryView.as_view(), name='ingest'),
    path('codebase/query', QueryCodebaseView.as_view(), name='query'),
    path('repository/status', RepositoryStatusView.as_view(), name='status'),
]
