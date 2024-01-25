from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from django.shortcuts import get_object_or_404
from .models import *
from .models import Campaign, Donor


# class DonorSerializer(ModelSerializer):
#     class Meta :
#         model = Donor
#         fields = "__all__"

    # def save(self):
    #     print(self.validated_data["amount"],self.validated_data["campaign"])
    #     donor = Donor(**self.validated_data)
    #     amount = self.validated_data["amount"]
    #     # campaign = Campaign.objects.get(pk=self.validated_data["campaign"])
    #     campaign = self.validated_data["campaign"]
    #     required_amount = campaign.goal_amount - campaign.fund_raised
    #     if amount > required_amount :
    #           return Response({"error" : False,"message" : "You can make donation for this campaign upto "+str(required_amount)+" Rs"},status=status.HTTP_200_OK) 
        
    #     campaign.fund_raised = campaign.fund_raised + amount
    #     campaign.save()

    #     print("------------------")
    #     donor.save()


class DonorSerializer1(ModelSerializer):
    class Meta:
        model = Donor
        fields = "__all__"

    def validate(self, data):
        amount = data["amount"]
        print("ampount",amount)
        campaign = data["campaign"]
        print(data,campaign.goal_amount,campaign.fund_raised)
        required_amount = campaign.goal_amount - campaign.fund_raised

        if amount > required_amount:
            return Response({"error" : False,"message" : "You can make donation for this campaign upto "+str(required_amount)+" Rs"},status=status.HTTP_200_OK)  
        return data

    def save(self, **kwargs):
        print("------------------------")
        amount = self.validated_data["amount"]
        campaign = self.validated_data["campaign"]
        campaign.fund_raised += amount
        print("------------------------")
        print(campaign.save())
        return super().save(**kwargs)
    
     
class DonorSerializer1(ModelSerializer):
    class Meta :
        model = Donor
        fields = ('is_anonymous','full_name','amount')

# class BankTransactionSerializer(ModelSerializer):
#     class Meta :
#         model = BankTransaction
#         fields = "__all__"

class UpiSerializers(ModelSerializer):
    class Meta :
        model = UpiTransaction
        fields = "__all__"

#################################################################################################################################################
class DonateToCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'

#*******************************************************************#
class BankTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankTransaction
        fields = '__all__'

#*******************************************************************#

from django.db import transaction

class DonorSerializer(serializers.ModelSerializer):
    bank_transactions = BankTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Donor
        fields = '__all__'

    def create(self, validated_data):
        bank_transactions_data = validated_data.pop('bank_transactions', None)

        with transaction.atomic():
            donor = Donor.objects.create(**validated_data)

            if bank_transactions_data:
                for transaction_data in bank_transactions_data:
                    BankTransaction.objects.create(donor=donor, **transaction_data)

        return donor

class DonorSerializer2(ModelSerializer):
    class Meta:
        model = Donor
        exclude = ['created_on','updated_on','mobile','pancard','comment','is_anonymous','is_approved']
#################################################################################################################################################
