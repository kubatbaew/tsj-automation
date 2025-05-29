# urls.py
from django.urls import path
from .views import SimpleUploadView

urlpatterns = [
    path('upload/', SimpleUploadView.as_view(), name='simple-upload'),
]
