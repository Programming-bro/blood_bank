from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import DonationResponse
from .serializers import DonationResponseSerializer
from requests.models import BloodRequest
from drf_yasg.utils import swagger_auto_schema


class DonationResponseViewSet(viewsets.ModelViewSet):
    serializer_class = DonationResponseSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            operation_summary='Retrive a all the own donation record of logged user'
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a profile of a donor"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrive a specific donation record'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary='Update a specific blood donation record'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary='Paritally updates a specific blood donation record'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    @swagger_auto_schema(
        operation_summary='Delete a specific request of blood donation record'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    ####
    def get_queryset(self):
        return DonationResponse.objects.filter(donor=self.request.user)

    def create(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')

        try:
            blood_request = BloodRequest.objects.get(id=request_id)
        except BloodRequest.DoesNotExist:
            return Response(
                {"error": "Request not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        donation = DonationResponse.objects.create(
            donor=request.user,
            request=blood_request
        )

        serializer = self.get_serializer(donation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # @action(detail=False, methods=['get'])
    # def history(self, request):
    #     donations = DonationResponse.objects.filter(donor=request.user)
    #     serializer = self.get_serializer(donations, many=True)
    #     return Response(serializer.data)