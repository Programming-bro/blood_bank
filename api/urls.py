from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import DonorProfileViewSet, initiate_payment, payment_success, payment_fail, payment_cancel
from requests.views import BloodRequestViewSet
from donations.views import DonationResponseViewSet

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

router = DefaultRouter()
router.register('donors', DonorProfileViewSet, basename='donor')
router.register('requests', BloodRequestViewSet, basename='request')
router.register('donations', DonationResponseViewSet, basename='donation')

urlpatterns = [

    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("payment/initiate/", initiate_payment, name="initiate-payment"),
    path("payment/success/", payment_success, name="payment-success"),
    path("payment/fail/", payment_fail, name="payment-fail"),
    path("payment/cancel/", payment_cancel, name="payment-cancel"),
]