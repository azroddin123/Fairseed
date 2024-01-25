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

################################################################
    
class PG_General(APIView):
    def get(self, request):
        page = PGSetting.objects.all()
        serializer = PGSerializer1(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PGSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PayPalApi(APIView):
    def get(self, request):
        paypal = PayPal.objects.all()
        serializer = PayPalSerializer1(paypal, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PayPalSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            instance = PayPal.objects.get(id=request.data.get('id'))
        except PhonePay.DoesNotExist:
            return Response({"error": "PayPal not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PayPalSerializer1(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StripeApi(APIView):
    def get(self, request):
        stripe = Stripe.objects.all()
        serializer = StripeSerializer1(stripe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StripeSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            instance = Stripe.objects.get(id=request.data.get('id'))
        except PhonePay.DoesNotExist:
            return Response({"error": "Stripe not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StripeSerializer1(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RazorPayApi(APIView):
    def get(self, request):
        stripe = RazorPay.objects.all()
        serializer = RazorPaySerializer1(stripe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = RazorPaySerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            instance = RazorPay.objects.get(id=request.data.get('id'))
        except PhonePay.DoesNotExist:
            return Response({"error": "RazorPay not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RazorPaySerializer1(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QRTransferApi(APIView):
    def get(self, request):
        stripe = QRTransfer.objects.all()
        serializer = QRTransferSerializer1(stripe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = QRTransferSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            instance = QRTransfer.objects.get(id=request.data.get('id'))
        except QRTransfer.DoesNotExist:
            return Response({"error": "QRTransfer not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = QRTransferSerializer1(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PhonePayApi(APIView):
    def get(self, request):
        stripe = PhonePay.objects.all()
        serializer = PhonePaySerializer1(stripe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = PhonePaySerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            instance = PhonePay.objects.get(id=request.data.get('id'))
        except PhonePay.DoesNotExist:
            return Response({"error": "PhonePay not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PhonePaySerializer1(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)