# urls.py
from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, 
    InfluencerListView, LogoutView, InfluencerDetailsAPI
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('influencers/', InfluencerListView.as_view(), name='influencers-list'),
    path('influencer/<str:channel_id>/', InfluencerDetailsAPI.as_view(), name='influencer-details-api'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('brands/', BrandListView.as_view(), name='brands-list'),
]
