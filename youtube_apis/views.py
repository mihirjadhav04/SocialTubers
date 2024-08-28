from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import YouTubeChannel
from .serializers import YouTubeChannelSerializer
from .youtube_stats import YTstats
from django.conf import settings

class YouTubeChannelStatsView(APIView):
    def get(self, request, channel_id):
        # Check if data is already in the database
        try:
            channel = YouTubeChannel.objects.get(channel_id=channel_id)
            serializer = YouTubeChannelSerializer(channel)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except YouTubeChannel.DoesNotExist:
            pass  # Channel not found, so we fetch from YouTube API

        # Fetch data from YouTube API
        api_key = settings.YOUTUBE_API_KEY
        yt = YTstats(api_key, channel_id)
        channel_stats = yt.get_channel_statistics()

        if not channel_stats:
            return Response({"error": "Channel not found or API limit reached"}, status=status.HTTP_404_NOT_FOUND)

        # Save channel statistics in the database
        channel = YouTubeChannel.objects.create(
            channel_id=channel_id,
            view_count=channel_stats.get('viewCount'),
            subscriber_count=channel_stats.get('subscriberCount'),
            video_count=channel_stats.get('videoCount')
        )

        serializer = YouTubeChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# class YouTubeChannelVideosView(APIView):
#     def get(self, request, channel_id):
#         # Check if videos are already in the database
#         try:
#             channel = YouTubeChannel.objects.get(channel_id=channel_id)
#             serializer = YouTubeChannelSerializer(channel)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except YouTubeChannel.DoesNotExist:
#             # return Response({"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)

#             # Fetch video data from YouTube API
#             api_key = settings.YOUTUBE_API_KEY
#             yt = YTstats(api_key, channel_id)
#             video_data = yt.get_channel_video_data()

#             if not video_data:
#                 return Response({"error": "No videos found or API limit reached"}, status=status.HTTP_404_NOT_FOUND)

#             # Save videos to the database
#             for video_id, video_info in video_data.items():
#                 YouTubeVideo.objects.create(
#                     video_id=video_id,
#                     channel=channel,
#                     title=video_info.get('snippet', {}).get('title'),
#                     description=video_info.get('snippet', {}).get('description'),
#                     view_count=video_info.get('statistics', {}).get('viewCount'),
#                     like_count=video_info.get('statistics', {}).get('likeCount'),
#                     comment_count=video_info.get('statistics', {}).get('commentCount')
#                 )

#             # Re-fetch the channel with video data
#             channel = YouTubeChannel.objects.get(channel_id=channel_id)
#             serializer = YouTubeChannelSerializer(channel)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# class FetchYouTubeChannelStatsView(APIView):
#     def get(self, request, channel_id):
#         api_key = settings.YOUTUBE_API_KEY
#         yt = YTstats(api_key, channel_id)
#         channel_stats = yt.get_channel_statistics()

#         if not channel_stats:
#             return Response({"error": "Channel not found or API limit reached"}, status=status.HTTP_404_NOT_FOUND)

#         return Response(channel_stats, status=status.HTTP_200_OK)
