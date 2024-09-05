from django.urls import path
from .views import YouTubeChannelStatsView, YouTubeCategoryListView, YouTubeChannelDetailsView

urlpatterns = [
    path('channel-stats/<str:channel_id>/', YouTubeChannelStatsView.as_view(), name='channel-stats'),
    path('category-list/', YouTubeCategoryListView.as_view(), name='youtube-category-list'),
    path('channel-details/<str:channel_id>/', YouTubeChannelDetailsView.as_view(), name='youtube-channel-details'),
    # path('channel-videos/<str:channel_id>/', YouTubeChannelVideosView.as_view(), name='channel-videos'),
]
