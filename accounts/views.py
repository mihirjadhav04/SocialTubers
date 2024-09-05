# views.py
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Influencer
from .serializers import (
    UserSerializer, InfluencerSerializer, 
    UserRegistrationSerializer
)
from rest_framework.permissions import AllowAny

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = []  # Override any global authentication
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user')
        influencer_data = request.data.get('influencer')
        print(user_data)
        print(influencer_data)
        user_serializer = self.get_serializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Save Influencer data
        influencer_serializer = InfluencerSerializer(data=influencer_data)
        if influencer_serializer.is_valid(raise_exception=True):
            influencer_serializer.save(user=user)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "success": True,
            "message": "User registered successfully!",
            "data": {
                "user": UserSerializer(user).data,
                "influencer": influencer_serializer.data,
                "token": token.key
            },
            "status_code": status.HTTP_201_CREATED
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "success": True,
                "message": "Logged In Successfully!",
                "data": {
                    "token": token.key,
                    "user": UserSerializer(user).data
                },
                "status_code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Invalid credentials. Please check your email and password.",
            "errors": {
                "email": ["Ensure this field is correct."],
                "password": ["Ensure this field is correct."]
            },
            "status_code": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # # Get the user's token
        # token = Token.objects.get(user=request.user)
        # # Delete the token to logout the user
        # token.delete()
        
        return Response({
            "success": True,
            "message": "Logged out successfully!",
            "status_code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class InfluencerListView(generics.ListAPIView):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from .models import Influencer
# from .serializers import InfluencerSerializer
# from socialtubers.youtube_stats import YTstats

class InfluencerDetailsAPI(APIView):
    pass
#     def get(self, request, channel_id):
#         try:
#             # Check if influencer data is already in the database
#             tuber = Influencer.objects.get(youtube_id=channel_id)
#             return Response(InfluencerSerializer(tuber).data, status=status.HTTP_200_OK)
        
#         except Influencer.DoesNotExist:
#             # If not, fetch from YouTube API and save it to the database
#             yt = YTstats(settings.YOUTUBE_API_KEY, channel_id)
#             channel_stats = yt.get_channel_statistics()

#             subCount = channel_stats.get("subscriberCount", 0)
#             viewCount = channel_stats.get("viewCount", 0)
#             videoCount = channel_stats.get("videoCount", 0)

#             base_price = convert_count(round((int(viewCount) / int(videoCount)) / 2))

#             subCount = convert_count(subCount)
#             viewCount = convert_count(viewCount)
#             videoCount = convert_count(videoCount)

#             video_stats = yt.get_channel_video_data()
#             sorted_videos = sorted(
#                 video_stats.items(), key=lambda item: int(item[1]["viewCount"]), reverse=True
#             )
#             converted_list = list(video_stats.items())
#             sliced_converted_list = converted_list[:2]

#             sliced_converted_list_recent_three_videoid = [
#                 upload[0] for upload in sliced_converted_list
#             ]

#             stats = [
#                 {
#                     "video_id": vid[0],
#                     "title": vid[1]["title"],
#                     "views": int(vid[1]["viewCount"]),
#                     "likes": int(vid[1]["likeCount"]),
#                     "comments": vid[1]["commentCount"],
#                     "thumbnail": vid[1]["thumbnails"]["default"]["url"],
#                 }
#                 for vid in sorted_videos
#             ]

#             top_video = stats[0]["video_id"] if stats else None

#             avg_views = sum(st["views"] for st in stats) / len(stats) if stats else 0
#             avg_likes = sum(st["likes"] for st in stats) / len(stats) if stats else 0

#             # Store the retrieved data into the database
#             tuber = Influencer.objects.create(
#                 channel_name=yt.get_channel_name(),
#                 youtube_id=channel_id,
#                 subscriber_count=subCount,
#                 view_count=viewCount,
#                 video_count=videoCount,
#                 top_video=top_video,
#                 average_views=round(avg_views),
#                 average_likes=round(avg_likes),
#                 recent_three_videos=sliced_converted_list_recent_three_videoid,
#                 user=request.user
#             )

#             return Response(InfluencerSerializer(tuber).data, status=status.HTTP_201_CREATED)

# def convert_count(num):
#     num_len = len(str(num))
#     num_in_int = int(num)
#     str_num = 0
#     if num_len < 4:
#         str_num = num
#     elif num_len < 7:
#         temp = format(num_in_int / 1000, ".1f") if num_in_int % 1000 != 0 else int(num_in_int / 1000)
#         str_num = str(temp) + "K"
#     elif num_len <= 10:
#         temp = format(num_in_int / (10 ** 6), ".1f") if num_in_int % (10 ** 6) != 0 else int(num_in_int / (10 ** 6))
#         str_num = str(temp) + "M"
#     return str_num





# # class BrandListView(generics.ListAPIView):
# #     queryset = Brand.objects.all()
# #     serializer_class = BrandSerializer
