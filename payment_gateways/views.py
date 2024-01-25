from django.shortcuts import render

# Create your views here.

from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status

from portals.GM import GenericMethodsMixin

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

########################################################################################################################
class BankTransferView(APIView):

    def get(self, request):
        account_details = BankTransfer.objects.all()
        serializer = BankTransferSerializer1(account_details, many=True)
        serialized_data = serializer.data
        return Response(serialized_data)
    
    def post(self, request):
        serializer = BankTransferSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

########################################################################################################################