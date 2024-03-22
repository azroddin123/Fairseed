from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.serializers import UserAdminSerializer
from donors.models import Donor
from donors.serializers import DonorSerializer1
from .models import * 
from datetime import datetime

class CampaignCategorySerializer(ModelSerializer):
    class Meta:
        model  = Campaigncategory
        fields = ("name","image","slug","is_active","id")

class CampaignSerializer(ModelSerializer):
    class Meta :
        model  = Campaign
        fields = "__all__"

class CampaignSerializer2(ModelSerializer):
    user        = UserAdminSerializer(read_only=True)
    donor_count = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model  = Campaign
        fields = "__all__"

    def get_donor_count(self, obj):
        return obj.donors.count()
   
class CampaignSerializer1(ModelSerializer):
    class Meta :
        model   = Campaign
        exclude = ["is_successful","status","is_featured","is_reported"]

        
class DocumentSerializer1(ModelSerializer):
    class Meta :
        model   = Documents
        fields  = ('id','doc_file','campaign')
        
class DocumentSerializer(ModelSerializer):
    class Meta :
        model   = Documents
        fields  = "__all__"

class DashboardSerializer(serializers.Serializer):
    total_campaign       = serializers.IntegerField()
    total_donation       = serializers.IntegerField()
    donor_count          = serializers.IntegerField()
    successful_campaign = serializers.IntegerField()
    student_benefited    = serializers.IntegerField()

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
        fields = ('id','title','campaign_image','story','summary','goal_amount','zakat_eligible','location','fund_raised','end_date','days_left','status',"is_reported","is_successful","is_featured","user","category",'donor_count','rasing_for','approval_status','campaign_data')

    def get_donor_count(self, obj):
          return obj.donors.count()
    
    
class RHSerializer(ModelSerializer):
    class Meta:
        model = RevisionHistory
        fields =  "__all__"
        
class CampaignDocumentSerializer(ModelSerializer):
    user        = UserAdminSerializer(read_only=True)
    documents   = DocumentSerializer1(many=True, read_only=True)
    donor_count = serializers.SerializerMethodField(read_only=True)
    category    = CampaignCategorySerializer(read_only=True)
    revision_history = RHSerializer(many=True, read_only=True)
    class Meta :
        model  = Campaign
        fields = ('id','title','campaign_image','story','summary','goal_amount','campaign_data','zakat_eligible','location','fund_raised','end_date','days_left','status',"is_successful","is_featured","user","documents",'category','revision_history','donor_count','approval_status','campaign_data')

    def get_donor_count(self, obj):
        return obj.donors.count()
    
class CampaignDetailSerializer(ModelSerializer):
    user        = serializers.SerializerMethodField(read_only=True)
    category    = serializers.SerializerMethodField(read_only=True)
    donor       = DonorSerializer1(source="donors",many=True,read_only=True)
    
    donor_count = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model   = Campaign
        fields  = ('id','title','campaign_image','story','summary','goal_amount','fund_raised','end_date','location','days_left','status','zakat_eligible','user','category','donor','donor_count')
    
    def get_user(self,obj):
        return obj.user.username
    
    def get_category(self,obj):
        return obj.category.name
    
    def get_donor_count(self, obj):
        return obj.donors.count()
    
    
class BankKYCSerializer(ModelSerializer):
    class Meta :
        model = BankKYC
        fields = "__all__"


class BankKYCEditSerializer(ModelSerializer):
    class Meta :
        model = BankKYCEdit
        fields = "__all__"

