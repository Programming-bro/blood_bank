from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import DonorProfileViewSet
from requests.views import BloodRequestViewSet
from donations.views import DonationResponseViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('donors', DonorProfileViewSet, basename='donor')
router.register('requests', BloodRequestViewSet, basename='request')
router.register('donations', DonationResponseViewSet, basename='donation')

urlpatterns = [

    # Auth
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', TokenObtainPairView.as_view(), name='login'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API
    path('', include(router.urls))
]