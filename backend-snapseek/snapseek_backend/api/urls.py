from django.urls import path
from .views import ImageUploadView,  ImageSearchView 

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('search/', ImageSearchView.as_view(), name = "image-search"),
]