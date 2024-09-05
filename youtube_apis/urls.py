from django.urls import path
from .views import YouTubeCategoryListView, YouTubeChannelDetailsView

urlpatterns = [
    path('category-list/', YouTubeCategoryListView.as_view(), name='youtube-category-list'),
    path('channel-details/<str:channel_id>/', YouTubeChannelDetailsView.as_view(), name='youtube-channel-details'),
]
