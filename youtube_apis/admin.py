from django.contrib import admin

from .models import YouTubeChannel, YouTubeCategory

# Register your models here.
admin.site.register(YouTubeChannel)
admin.site.register(YouTubeCategory)
