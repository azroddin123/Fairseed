from django.db import models 
from rest_framework.serializers import ModelSerializer
from .models import * 


class PGSerializer(ModelSerializer):
    class Meta :
        model = PGSetting
        fields = "__all__"


class BankTransferSerializer(ModelSerializer):
    class Meta :
        model = BankTransfer
        fields = "__all__"

class PhonePaySerializer(ModelSerializer):
    class Meta :
        model =PhonePay
        fields = "__all__"


        