from rest_framework.serializers import ModelSerializer
from .models import * 


class DonorSerializer(ModelSerializer):
    class Meta :
        model = Donor
        fields = "__all__"

class DonorSerializer1(ModelSerializer):
    class Meta :
        model = Donor
        fields = ('is_anonymous','full_name','amount')


class BankTransactionSerializer(ModelSerializer):
    class Meta :
        model = BankTransaction
        fields = "__all__"

class UpiSerializers(ModelSerializer):
    class Meta :
        model = UpiTransaction
        fields = "__all__"