from django.db import models

class YouTubeChannel(models.Model):
    channel_id = models.CharField(max_length=100, unique=True)
    view_count = models.BigIntegerField()
    subscriber_count = models.BigIntegerField()
    video_count = models.IntegerField()

    def __str__(self):
        return self.channel_id

class YouTubeVideo(models.Model):
    video_id = models.CharField(max_length=100, unique=True)
    channel = models.ForeignKey(YouTubeChannel, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    view_count = models.BigIntegerField()
    like_count = models.BigIntegerField()
    comment_count = models.BigIntegerField()

    def __str__(self):
        return self.title
