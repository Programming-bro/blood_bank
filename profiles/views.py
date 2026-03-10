
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import DonorProfile, Transaction
from .serializers import DonorProfileSerializer, DonorListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from sslcommerz_lib import SSLCOMMERZ
from django.http import HttpResponseRedirect
from django.conf import settings as main_settings
import uuid
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from urllib import request as urllib_request, parse
from django.contrib.auth import get_user_model

User = get_user_model()



class DonorProfileViewSet(viewsets.ModelViewSet):
    queryset = DonorProfile.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['blood_group']
    search_fields = ['user__username', 'address']

    @swagger_auto_schema(
            operation_summary='Retrive a all the donors short informations'
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a profile of a donor"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrive a specific donors profile'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary='Update a specific donor'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary='Paritally updates a specific donor'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary='Delete a specific request of blood donation'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
    ####
    def get_serializer_class(self):
        if self.action == 'list':
            return DonorListSerializer  
        return DonorProfileSerializer
    
    def get_queryset(self):
        if self.action == 'list':
            return DonorProfile.objects.filter(is_available=True)
        return DonorProfile.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
    
    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    @swagger_auto_schema(
        operation_summary='View, Updates or Partially updates a specific donors profile according to request method'
    )
    def me(self, request):
        profile, created = DonorProfile.objects.get_or_create(user=request.user)

        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)

        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



# ১. পেমেন্ট শুরু করার ফাংশন
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    
    # স্যান্ডবক্স ডিটেইলস
    store_id = 'redhe69af5f627dc67'
    store_pass = 'redhe69af5f627dc67@ssl'
    api_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
    
    # ইউনিক ট্রানজ্যাকশন আইডি (ইউজারের আইডি সহ যাতে পরে চেনা যায়)
    tran_id = f"USER_{user.id}_{uuid.uuid4().hex[:6].upper()}"
    
    post_body = {
        'store_id': store_id,
        'store_passwd': store_pass,
        'total_amount': "100.00",
        'currency': "BDT",
        'tran_id': tran_id,
        'success_url': f"{main_settings.BACKEND_URL}/api/v1/payment/success/",
        'fail_url': f"{main_settings.BACKEND_URL}/api/v1/payment/fail/",
        'cancel_url': f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/",
        'cus_name': str(user.username),
        'cus_email': str(user.email),
        'cus_add1': "Dhaka",
        'cus_city': "Dhaka",
        'cus_postcode': "1200",
        'cus_country': "Bangladesh",
        'cus_phone': "01711111111",
        'shipping_method': "NO",
        'num_of_item': "1",
        'product_name': "Pro Plan",
        'product_category': "Service",
        'product_profile': "general",
    }

    try:
        encoded_data = parse.urlencode(post_body).encode('utf-8')
        req = urllib_request.Request(api_url, data=encoded_data, method='POST')
        with urllib_request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))

        if res_data.get('status') == 'SUCCESS':
            return Response({'payment_url': res_data['GatewayPageURL']})
        return Response({'error': 'Failed to create session'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)





# ২. পেমেন্ট সফল হওয়ার ফাংশন
@csrf_exempt
@api_view(['POST'])
def payment_success(request):
    data = request.POST
    tran_id = data.get('tran_id') # যেমন: USER_5_A1B2C3
    
    # ১. ট্রানজ্যাকশন আইডি থেকে ইউজার আইডি আলাদা করা
    try:
        user_id = tran_id.split('_')[1] # '5' বের করে আনবে
        user = User.objects.get(id=user_id)
        
        # ২. ইউজারের প্রোফাইল আপডেট করা
        # (যদি UserProfile মডেলে is_premium ফিল্ড থাকে)
        profile, created = DonorProfile.objects.get_or_create(user=user)
        profile.is_premium = True
        profile.save()
        
        print(f"Success! {user.email} is now a Premium User.")
        
        # ৩. ইউজারকে ফ্রন্টএন্ডের প্রোফাইল পেজে রিডাইরেক্ট করা
        return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/profile?payment=success")
        
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/profile?payment=failed")
@api_view(['POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/profile")


@api_view(['POST'])
def payment_fail(request):
    print("Inside fail")
    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/profile")