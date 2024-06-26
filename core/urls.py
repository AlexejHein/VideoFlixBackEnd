# core/urls.py
from django.urls import path
from .views import UserCreateView, VideoListView, VideoDetailView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
]
