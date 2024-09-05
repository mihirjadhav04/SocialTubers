# urls.py
from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, 
    InfluencerListView, LogoutView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('influencers/', InfluencerListView.as_view(), name='influencers-list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('brands/', BrandListView.as_view(), name='brands-list'),
]
