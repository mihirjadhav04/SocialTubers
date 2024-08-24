# urls.py
from django.urls import path
from .views import YouTubeCategoryListView

urlpatterns = [
    path('list/', YouTubeCategoryListView.as_view(), name='youtube-category-list'),
]
