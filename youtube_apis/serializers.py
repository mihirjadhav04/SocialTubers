from rest_framework import serializers
from .models import YouTubeChannel, YouTubeVideo

# class YouTubeVideoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = YouTubeVideo
#         fields = '__all__'

class YouTubeChannelSerializer(serializers.ModelSerializer):
    # videos = YouTubeVideoSerializer(many=True, read_only=True)

    class Meta:
        model = YouTubeChannel
        fields = '__all__'
