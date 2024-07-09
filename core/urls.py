from django.urls import path
from .views import VideoListView, VideoDetailView, CustomUserCreateView

urlpatterns = [
    path('users/', CustomUserCreateView.as_view(), name='user-create'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
]
