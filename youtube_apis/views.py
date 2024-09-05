from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import YouTubeChannel, YouTubeCategory, YouTubeVideo
from .serializers import YouTubeChannelSerializer, YouTubeCategorySerializer
from socialtubers.youtube_stats import YTstats
from django.conf import settings
from googleapiclient.discovery import build
from rest_framework.permissions import AllowAny


class YouTubeChannelDetailsView(APIView):
    authentication_classes = []  # Override any global authentication
    permission_classes = [AllowAny]
    def get(self, request, channel_id):
        
        try:
            # Check if channel data is already in the database
            channel = YouTubeChannel.objects.get(channel_id=channel_id)
            serializer = YouTubeChannelSerializer(channel)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except YouTubeChannel.DoesNotExist:
            pass  # Channel not found, so we fetch from YouTube API

        # Fetch data from YouTube API
        api_key = settings.YOUTUBE_API_KEY
        yt = YTstats(api_key, channel_id)
        
        # Fetch channel statistics
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

        print("CHANNEL STATS COMPLETED!")

        # Fetch video data from YouTube API
        video_data = yt.get_channel_video_data()
        print(video_data)
        print("LENGTH OF VIDEO DATA : ", len(video_data))
        if not video_data:
            return Response({"error": "No videos found or API limit reached"}, status=status.HTTP_404_NOT_FOUND)

        # Save videos to the database
        for video_id, video_info in video_data.items():
            print("VIDEO INFO : ", video_info)
            YouTubeVideo.objects.create(
                video_id=video_id,
                channel=channel,
                title=video_info.get('snippet').get('title'),
                description=video_info.get('snippet').get('description'),
                view_count=video_info.get('statistics').get('viewCount', 0),
                like_count=video_info.get('statistics').get('likeCount', 0),
                comment_count=video_info.get('statistics').get('commentCount', 0)
            )

        # Serialize the complete channel data including videos
        serializer = YouTubeChannelSerializer(channel)
        return Response({
            "success": True,
            "message": "Youtube data of the influencer fetched successfully!",
            "status_code": status.HTTP_201_CREATED,
            "data": {
                    "channel-statistics": serializer.data
                },
        }, status=status.HTTP_201_CREATED)





class YouTubeCategoryListView(APIView):
    def get(self, request):
       
        # Check if categories are already in the database
        categories = YouTubeCategory.objects.all()
        authentication_classes = []  # Override any global authentication
        permission_classes = [AllowAny]

        if categories.exists():
            print("DATA ACCESSED FROM DB.")
            serializer = YouTubeCategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If not, fetch from YouTube API
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        
        try:
            print("DATA ACCESSED FROM API.")

            response = youtube.videoCategories().list(
                part="snippet",
                regionCode="IN"  # Change to your preferred region
            ).execute()
            
            categories_data = []
            for item in response.get('items', []):
                category_id = item['id']
                title = item['snippet']['title']
                
                # Save each category to the database
                category, created = YouTubeCategory.objects.get_or_create(
                    category_id=category_id,
                    defaults={'title': title}
                )
                
                categories_data.append({
                    "category_id": category_id,
                    "title": title
                })
            
            return Response(categories_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class YouTubeChannelStatsView(APIView):
    pass
#     def get(self, request, channel_id):
#         # Check if data is already in the database
#         try:
#             channel = YouTubeChannel.objects.get(channel_id=channel_id)
#             serializer = YouTubeChannelSerializer(channel)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except YouTubeChannel.DoesNotExist:
#             pass  # Channel not found, so we fetch from YouTube API

#         # Fetch data from YouTube API
#         api_key = settings.YOUTUBE_API_KEY
#         yt = YTstats(api_key, channel_id)
#         channel_stats = yt.get_channel_statistics()

#         if not channel_stats:
#             return Response({"error": "Channel not found or API limit reached"}, status=status.HTTP_404_NOT_FOUND)

#         # Save channel statistics in the database
#         channel = YouTubeChannel.objects.create(
#             channel_id=channel_id,
#             view_count=channel_stats.get('viewCount'),
#             subscriber_count=channel_stats.get('subscriberCount'),
#             video_count=channel_stats.get('videoCount')
#         )

#         serializer = YouTubeChannelSerializer(channel)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)



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
