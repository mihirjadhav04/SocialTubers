from django.db import models

class YouTubeChannel(models.Model):
    channel_id = models.CharField(max_length=255, unique=True)
    # title = models.CharField(max_length=255, null=True, blank=True)
    # description = models.TextField(null=True, blank=True)
    view_count = models.BigIntegerField(default=0)
    subscriber_count = models.BigIntegerField(default=0)
    video_count = models.IntegerField(default=0)

    def __str__(self):
        return self.channel_id

class YouTubeVideo(models.Model):
    video_id = models.CharField(max_length=255, unique=True)
    channel = models.ForeignKey(YouTubeChannel, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    comment_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title or self.video_id



class YouTubeCategory(models.Model):
    category_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)


# class YouTubeChannel(models.Model):
#     channel_id = models.CharField(max_length=100, unique=True)
#     view_count = models.BigIntegerField()
#     subscriber_count = models.BigIntegerField()
#     video_count = models.IntegerField()

#     def __str__(self):
#         return self.channel_id

# class YouTubeVideo(models.Model):
#     video_id = models.CharField(max_length=100, unique=True)
#     channel = models.ForeignKey(YouTubeChannel, related_name='videos', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     view_count = models.BigIntegerField()
#     like_count = models.BigIntegerField()
#     comment_count = models.BigIntegerField()

#     def __str__(self):
#         return self.title
