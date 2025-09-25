from django.urls import path
from .views import upload_resume, match, health, ingest, search_match

urlpatterns = [
    path('upload-resume/', upload_resume, name='upload-resume'),
    path('match/', match, name='match'),
    path('health/', health, name='health'),
    path('ingest/', ingest, name='ingest'),
    path('search-match/', search_match, name='search-match'),
]
