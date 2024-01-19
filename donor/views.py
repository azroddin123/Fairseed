from django.shortcuts import get_object_or_404, render

# Create your views here.
from .serializers import * 
from .models import (
    Donor,
    BankTransfer,
    UpiTransaction
)
from rest_framework.views import APIView
from fairseed.GM import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status


class DonorApi(GenericMethodsMixin,APIView):
    model = Donor
    serializer_class = DonorSerializer
    lookup_field = "id"

class BankTransferApi(GenericMethodsMixin,APIView):
    model = BankTransfer
    serializer_class =BankTansferSerializer
    lookup_field = "id"

class UpiTransactionApi(GenericMethodsMixin,APIView):
    model = UpiTransaction
    serializer_class = UpiSerializers
    lookup_field = "id"


class FundedForUserApi(APIView):
    def get(self, request):
        funds = Donor.objects.filter('amount')
        


############# MY CODE ##############
        
class DonorDetailApi(APIView):
    def get(self, request, pk):
        # donor = Donor.objects.all()
        donor = get_object_or_404(Donor, pk=pk)
        serializer = DonorSerializer(donor)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DonorDonationApi:
    def get(self, request):
        donor = Donor.objects.all()
        



