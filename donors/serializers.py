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

class User1(ModelSerializer):
    class Meta :
        model = User
        fields = ('id','username','email','mobile_number')


class Camapign1(ModelSerializer):
    user = User1(read_only=True)
    class Meta :
        model = Campaign
        fields = ('id','title','goal_amount','fund_raised','user')


class WithDrawalSerializer(ModelSerializer):
    campaign   = Camapign1(read_only=True)
    class Meta :
        model = Withdrawal
        fields = "__all__"  

