from django.urls import path
from .views import VideoListView, VideoDetailView, CustomUserCreateView, EmailVerificationView

urlpatterns = [
    path('users/', CustomUserCreateView.as_view(), name='user-create'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('auth/registration/account-confirm-email/', EmailVerificationView.as_view(), name='account_confirm_email'),

]
