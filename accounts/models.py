from django.db import models
from datetime import datetime

# Create your models here.
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    first_name = None
    last_name = None
    name = models.CharField(max_length=100)
    email = models.EmailField(_("email address"), unique=True)
    # is_influencer = models.BooleanField(default=False)
    # is_brand = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

# CATAGORIES = (
#     ("Autos & Vehicles","Autos & Vehicles"),
#     ("Comedy","Comedy"),
#     ("Education","Education"),
#     ("Entertainment","Entertainment"),
#     ("Film & Animation","Film & Animation"),
#     ("Gaming","Gaming"),
#     ("Howto & Style","Howto & Style"),
#     ("Music","Music"),
#     ("News & Politics","News & Politics"),
#     ("Nonprofits & Activisms","Nonprofits & Activisms"),
#     ("People & Blogs","People & Blogs"),
#     ("Pets & Animals","Pets & Animals"),
#     ("Science & Technology","Science & Technology"),
#     ("Travel & Events","Travel & Events"),
#     ("Sports","Sports"),
# )
class Influencer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    channel_name = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100, unique=True)
    instagram_id = models.CharField(max_length=100, null=True, blank=True)
    subscriber_count = models.CharField(max_length=50, null=True, blank=True)
    view_count = models.CharField(max_length=50, null=True, blank=True)
    video_count = models.CharField(max_length=50, null=True, blank=True)
    top_video = models.CharField(max_length=100, null=True, blank=True)
    average_views = models.IntegerField(null=True, blank=True)
    average_likes = models.IntegerField(null=True, blank=True)
    recent_three_videos = models.JSONField(null=True, blank=True)  # To store recent three video IDs
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.channel_name

# class Brand(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     # category_type = models.CharField(max_length=100, choices=CATAGORIES)
#     brand_name = models.CharField(max_length=100)
#     full_name = models.CharField(max_length=100)
#     # established_date = models.DateField()
#     instagram_id = models.CharField(max_length=100)
#     # is_featured = models.BooleanField(default=False)
#     short_description = models.CharField(max_length=255)
#     profile_photo = models.ImageField(upload_to="brand_images/%Y/%m/")
#     created_date = models.DateTimeField(default=datetime.now, blank=True)

#     def __str__(self):
#         return self.brand_name
