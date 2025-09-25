from django.urls import path, include
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

urlpatterns = [
    path('api/', include('optimizer.urls')),
    path('metrics', lambda request: HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)),
]
