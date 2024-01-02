from rest_framework.serializers import ModelSerializer
from .models import * 
from .models import Donor
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


# class DonorSerializer(ModelSerializer):
#     class Meta :
#         model = Donor
#         fields = "__all__"

#     def save(self):
#         print(self.validated_data["amount"],self.validated_data["campaign"])
#         donor = Donor(**self.validated_data)
#         amount = self.validated_data["amount"]
#         # campaign = Campaign.objects.get(pk=self.validated_data["campaign"])
#         campaign = self.validated_data["campaign"]
#         required_amount = campaign.goal_amount - campaign.fund_raised
#         if amount > required_amount :
#               return Response({"error" : False,"message" : "You can make donation for this campaign upto "+str(required_amount)+" Rs"},status=status.HTTP_200_OK)     

#         campaign.fund_raised = campaign.fund_raised + amount
#         campaign.save()
#         donor.save()


class DonorSerializer(ModelSerializer):
    class Meta:
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




    # def validate(self, data):
    #     amount = data["amount"]
    #     campaign = data["campaign"]
    #     print(amount)
    #     print(data,campaign.goal_amount,campaign.fund_raised)
    #     required_amount = campaign.goal_amount - campaign.fund_raised
    #     return data

    # def save(self, **kwargs):
    #     amount = self.validated_data["amount"]
    #     campaign = self.validated_data["campaign"]
    #     required_amount = campaign.goal_amount - campaign.fund_raised
    #     print(amount,required_amount)
    #     if amount > required_amount:
    #         raise serializers.ValidationError({"error": True, "message": f"You can make a donation for this campaign up to {required_amount} Rs Only"})
    #     campaign.fund_raised += amount
    #     print(campaign.save())
    #     return super().save(**kwargs)
    