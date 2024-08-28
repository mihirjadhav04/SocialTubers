from django.urls import path
from .views import YouTubeChannelStatsView

urlpatterns = [
    path('channel-stats/<str:channel_id>/', YouTubeChannelStatsView.as_view(), name='channel-stats'),
    # path('channel-videos/<str:channel_id>/', YouTubeChannelVideosView.as_view(), name='channel-videos'),
]
