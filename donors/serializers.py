from rest_framework.serializers import ModelSerializer
from .models import * 
from .models import Donor,Campaign
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


class DonorSerializer(ModelSerializer):
    class Meta :
        model = Donor
        fields = "__all__"

    def save(self):
        print(self.validated_data["amount"],self.validated_data["campaign"])
        donor = Donor(**self.validated_data)
        amount = self.validated_data["amount"]
        # campaign = Campaign.objects.get(pk=self.validated_data["campaign"])
        campaign = self.validated_data["campaign"]
        required_amount = campaign.goal_amount - campaign.fund_raised
        if amount > required_amount :
              return Response({"error" : False,"message" : "You can make donation for this campaign upto "+str(required_amount)+" Rs"},status=status.HTTP_200_OK)     
        
        campaign.fund_raised = campaign.fund_raised + amount
        campaign.save()

        print("------------------")
        donor.save()

class DonorSerializer(ModelSerializer):
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

class BankTransactionSerializer(ModelSerializer):
    class Meta :
        model = BankTransaction
        fields = "__all__"

class UpiSerializers(ModelSerializer):
    class Meta :
        model = UpiTransaction
        fields = "__all__"

class DonorSerializer2(ModelSerializer):
    class Meta:
        model = Donor
        exclude = ['created_on','updated_on','mobile','pancard','comment','is_anonymous','is_approved']

