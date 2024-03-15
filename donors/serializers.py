from rest_framework.serializers import ModelSerializer
from .models import * 
from .models import Donor
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from accounts.models import User
from campaigns.models import Campaign,BankKYC




class DonorSerializer2(ModelSerializer):
    class Meta:
        model = Donor
        fields = "__all__"

class DonorSerializer(ModelSerializer):
    campaign = serializers.SerializerMethodField()
    class Meta:
        model = Donor
        fields = "__all__"
        
    def get_campaign(self, obj):
        return obj.campaign.title
        # return obj.campaign.campaign_name if obj.campaign else None

class DonorSerializer1(ModelSerializer):
    date = serializers.SerializerMethodField()
    class Meta :
        model = Donor
        fields = ('is_anonymous','full_name','amount',"date")
    
    def get_date(self, obj):
        # Format the date here
        return obj.created_on.strftime('%d-%b-%Y')

class BankTransactionSerializer(ModelSerializer):
    class Meta :
        model = BankTransaction
        fields = "__all__"

class UpiSerializers(ModelSerializer):
    class Meta :
        model = UpiTransaction
        fields = "__all__"


class User1(ModelSerializer):
    class Meta :
        model = User
        fields = ('id','username','email','mobile_number')


class Camapign1(ModelSerializer):
    class Meta :
        model = Campaign
        fields = ('id','title','goal_amount','fund_raised')


class WithDrawalSerializer(ModelSerializer):
    class Meta :
        model = Withdrawal

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
    