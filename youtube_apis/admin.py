from django.contrib import admin

from .models import YouTubeChannel, YouTubeCategory, YouTubeVideo

# Register your models here.
admin.site.register(YouTubeChannel)
admin.site.register(YouTubeVideo)
admin.site.register(YouTubeCategory)
