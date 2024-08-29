from rest_framework import serializers
from .models import YouTubeChannel, YouTubeCategory

class YouTubeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeCategory
        fields = ['category_id', 'title']


# class YouTubeVideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = YouTubeVideo
#         fields = '__all__'

class YouTubeChannelSerializer(serializers.ModelSerializer):
    # videos = YouTubeVideoSerializer(many=True, read_only=True)

    class Meta:
        model = YouTubeChannel
        fields = '__all__'
