
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import DonorProfile
from .serializers import DonorProfileSerializer, DonorListSerializer
# from .filters import BloodGroupFilter
# from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

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