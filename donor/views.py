from django.shortcuts import render
from django.db.models import Sum

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
from rest_framework.decorators import action

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



