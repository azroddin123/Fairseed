from django.shortcuts import render

# Create your views here.
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from portals.GM import GenericMethodsMixin

class PGApi(GenericMethodsMixin,APIView):
    model = PGSetting
    serializer_class = PGSerializer
    lookup_field = "id"

class BankTransferApi(GenericMethodsMixin,APIView):
    model = BankTransfer
    serializer_class = BankTransferSerializer
    lookup_field = "id"

class PhonepayApi(GenericMethodsMixin,APIView):
    model = PhonePay
    serializer_class = PhonePaySerializer
    lookup_field = "id"


    