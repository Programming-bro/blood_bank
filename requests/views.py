from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import BloodRequest
from .serializers import BloodRequestSerializer
from donations.models import DonationResponse
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class BloodRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BloodRequestSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_summary='Retrive a all the request of blood donation'
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a request for blood donation"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrive a specific request of blood donation'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary='Update a specific request of blood donation'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary='Paritally updates a specific request of blood donation'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a specific request of blood donation'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    #####
    def permission_denied(self, request, message=None, code=None):
        return super().permission_denied(request, message, code)

    def get_queryset(self):
        if self.action == 'list':
            return BloodRequest.objects.filter(is_active=True).exclude(
                requester=self.request.user
            )
        return BloodRequest.objects.all()

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    @action(detail=True, methods=['post'])
    @swagger_auto_schema(
        operation_summary='Accept a specific request of blood donation'
    )
    def accept(self, request, pk=None):
        blood_request = self.get_object()
        
        if blood_request.requester == request.user:
            return Response(
                {"error": "You cannot accept your own request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent duplicate accept
        if DonationResponse.objects.filter(
            donor=request.user,
            request=blood_request
        ).exists():
            return Response(
                {"error": "You already accepted this request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        DonationResponse.objects.create(
            donor=request.user,
            request=blood_request
        )

        return Response(
            {"message": "Request accepted successfully."},
            status=status.HTTP_201_CREATED
        )