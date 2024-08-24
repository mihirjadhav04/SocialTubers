# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.discovery import build
from django.conf import settings
from .models import YouTubeCategory
from .serializers import YouTubeCategorySerializer

class YouTubeCategoryListView(APIView):
    def get(self, request):
        # Check if categories are already in the database
        categories = YouTubeCategory.objects.all()
        
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
