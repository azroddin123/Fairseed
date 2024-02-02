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

#################################################

class PGSerializer1(ModelSerializer):
    class Meta :
        model = PGSetting
        fields = ['currency_code','currency_symbol','fee_for_donation','currency_position','decimal_format']

class PayPalSerializer1(ModelSerializer):
    class Meta:
        model = PayPal
        fields = ['percentage_fee','fee_cents','paypal_account','paypal_sandbox','is_enabled']

class StripeSerializer1(ModelSerializer):
    class Meta:
        model = Stripe
        fields = ['fee_percent', 'fee_cents', 'stripe_public_key', 'stripe_secret_key', 'is_enabled']

class RazorPaySerializer1(ModelSerializer):
    class Meta:
        model = RazorPay
        fields = ['razorpay_key', 'razorpay_secret', 'is_enabled', 'fee_percent', 'fee_cents']

class QRTransferSerializer1(ModelSerializer):
    class Meta:
        model = QRTransfer
        fields = ['fee_percent', 'qr_path', 'is_enabled']

class PhonePaySerializer1(ModelSerializer):
    class Meta:
        model = PhonePay
        fields = ['id', 'phonepay_key', 'phonepay_secret', 'fee_percent', 'fee_cents', 'is_enabled']


class BankTransferSerializer1(ModelSerializer):
    class Meta:
        model = BankTransfer
        fields = ['fee_percent', 'bank_details', 'is_enabled']