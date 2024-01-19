from django.shortcuts import render

# Create your views here.

from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status

from fairseed.GM import GenericMethodsMixin

class PGApi(GenericMethodsMixin,APIView):
    model = PGSetting
    serializer_class = PGSerializer
    lookup_field = "id"

class PaypalApi(GenericMethodsMixin,APIView):
    model = PayPal
    serializer_class = PayPalSerializer
    lookup_field  = "id"

class StripeApi(GenericMethodsMixin,APIView):
    model = Stripe
    serializer_class = StripeSerializer
    lookup_field = "id"

class BankTransferApi(GenericMethodsMixin,APIView):
    model = BankTransfer
    serializer_class = BankTransferSerializer
    lookup_field = "id"

class RazorpayApi(GenericMethodsMixin,APIView):
    model = RazorPay
    serializer_class = RazorpaySerializer
    lookup_field = "id"

class PhonepayApi(GenericMethodsMixin,APIView):
    model = PhonePay
    serializer_class = PhonePaySerializer
    lookup_field = "id"

class QRTransferApi(GenericMethodsMixin,APIView):
    model = QRTransfer
    serializer_class = QRTransferSerializer
    lookup_field = "id"

    