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
    campaign_title = serializers.SerializerMethodField()
    c_id=serializers.SerializerMethodField()
    class Meta:
        model = Donor
        fields = "__all__"
        
    def get_campaign_title(self, obj):
        return obj.campaign.title
        # return obj.campaign.campaign_name if obj.campaign else None

    def get_c_id(self,obj):
        return obj.campaign.c_id if obj.campaign else None

class DonorSerializer1(ModelSerializer):
    date = serializers.SerializerMethodField()
    class Meta :
        model = Donor
        fields = ('status','is_anonymous','full_name','amount',"date")
    
    def get_date(self, obj):
        # Format the date here
        return obj.date.strftime('%d-%b-%Y') if obj.date else None

class User1(ModelSerializer):
    class Meta :
        model = User
        fields = ('id','username','email','mobile_number')


class Camapign1(ModelSerializer):
    user = User1(read_only=True)
    class Meta :
        model = Campaign
        fields = ('id','title','goal_amount','fund_raised','user','c_id','notes')


class WithDrawalSerializer(ModelSerializer):
    campaign   = Camapign1(read_only=True)
    class Meta :
        model = Withdrawal
        fields = "__all__"  

class WithDrawalSerializer1(ModelSerializer):
    class Meta :
        model = Withdrawal
        fields = "__all__"  
