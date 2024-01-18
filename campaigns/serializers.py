from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.serializers import UserAdminSerializer
from donors.models import Donor
from donors.serializers import DonorSerializer1
from .models import * 

class CampaignCategorySerializer(ModelSerializer):
    class Meta:
        model  = Campaigncategory
        fields = ("name","image","is_active","id")

class CampaignSerializer(ModelSerializer):
    category = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model  = Campaign
        fields = "__all__"

    def get_category(self,obj):
       return obj.category.name
   
class CampaignSerializer1(ModelSerializer):
    class Meta :
        model   = Campaign
        exclude = ["is_successful","status","is_featured","is_reported"]

class AccountDSerializer(ModelSerializer):
    class Meta :
        model  = AccountDetail
        fields = "__all__"
        
class KycSerializer(ModelSerializer):
    class Meta :
        model = Kyc
        fields = "__all__"

class DocumentSerializer(ModelSerializer):
    class Meta :
        model   = Documents
        fields  = "__all__"

class DashboardSerializer(serializers.Serializer):
    total_campaign       = serializers.IntegerField()
    total_donation       = serializers.IntegerField()
    donor_count          = serializers.IntegerField()
    successfull_campaign = serializers.IntegerField()
    student_benifited    = serializers.IntegerField()

class CampaignBycategorySerializer(ModelSerializer):
    campaign    = CampaignSerializer1(source="campaign_set",many=True)
    class Meta :
        model   = Campaigncategory
        fields  = "__all__"

class CampaignAdminSerializer(ModelSerializer):
    user        = UserAdminSerializer(read_only=True)
    category    = CampaignCategorySerializer(read_only=True)
    donor_count = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model  = Campaign
        fields = ('id','title','campaign_image','story','summary','goal_amount','location','fund_raised','end_date','days_left','status',"is_reported","is_successful","is_featured","user","category",'donor_count')

    def get_donor_count(self, obj):
          return obj.donors.count()

class CampaignDetailSerializer(ModelSerializer):
    user        = serializers.SerializerMethodField(read_only=True)
    category    = serializers.SerializerMethodField(read_only=True)
    donor       = DonorSerializer1(source="donors",many=True,read_only=True)
    donor_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta :
        model   = Campaign
        fields  = ('id','title','campaign_image','story','summary','goal_amount','fund_raised','end_date','status','user','category','donor','donor_count')
    
    def get_user(self,obj):
        return obj.user.username
    
    def get_category(self,obj):
        return obj.category.name
    
    def get_donor_count(self, obj):
        return obj.donors.count()
    


# class BankKYCSerializer(ModelSerializer):
#     class Meta :
#         model = BankKYC
#         fields = "__all__"
        