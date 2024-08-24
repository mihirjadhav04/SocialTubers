# models.py
from django.db import models

class YouTubeCategory(models.Model):
    category_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)
