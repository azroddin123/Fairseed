from django.db import models 
from rest_framework.serializers import ModelSerializer
from .models import * 


class PGSerializer(ModelSerializer):
    class Meta :
        model = PGSetting
        fields = "__all__"

class PayPalSerializer(ModelSerializer):
    class Meta :
        model= PayPal
        fields  = "__all__"

class StripeSerializer(ModelSerializer):
    class Meta :
        model = Stripe
        fields = "__all__"

class BankTransferSerializer(ModelSerializer):
    class Meta :
        model = BankTransfer
        fields = "__all__"

class RazorpaySerializer(ModelSerializer):
    class Meta :
        model = RazorPay
        fields = "__all__"


class PhonePaySerializer(ModelSerializer):
    class Meta :
        model =PhonePay
        fields = "__all__"

class QRTransferSerializer(ModelSerializer):
    class Meta :
        model = QRTransfer
        fields = "__all__"

        