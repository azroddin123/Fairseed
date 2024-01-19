from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.serializers import UserAdminSerializer
from donors.models import Donor
from donors.serializers import DonorSerializer1
from .models import *

class CampaigncategorySerializer(ModelSerializer):
    class Meta:
        model  = Campaigncategory
        fields = ("id","name","image","is_active")

    def create(self, validated_data):
        # Override the create method to handle image field
        image = validated_data.pop('image', None)
        instance = super().create(validated_data)
       
        if image:
            instance.image = image
            instance.save()
       
        return instance
   
class CampaignSerializer(ModelSerializer):
   
    class Meta :
        model  = Campaign
        fields = "__all__"

class CampaignSerializer1(ModelSerializer):
    class Meta :
        model   = Campaign
        exclude = ["is_successful","status","is_featured","is_reported"]

class CKBSerializer(ModelSerializer):
    class Meta :
        model  = CampaignKycBenificiary
        fields = "__all__"

# class BBDetailSerailizer(ModelSerializer):
#     class Meta :
#         model = BenificiaryBankDetails
#         fields = "__all__"

# class KycDetailSerializer(ModelSerializer):
#     class Meta :
#         model = KycDetails
#         fields = "__all__"

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
    user       = UserAdminSerializer(read_only=True)
    category   = CampaigncategorySerializer(read_only=True)
    class Meta :
        model  = Campaign
        fields = ('id','title','campaign_image','goal_amount','fund_raised','start_date','end_date','status',"is_reported","is_successful","is_featured","user","category")

class DocumentSerializer(ModelSerializer):
    class Meta :
        model   = Documents
        fields  = "__all__"

class CampaignDetailSerializer(ModelSerializer):
    user        = serializers.SerializerMethodField(read_only=True)
    category    = serializers.SerializerMethodField(read_only=True)
    donor       = DonorSerializer1(source="donors",many=True,read_only=True)
   
    class Meta :
        model   = Campaign
        fields  = ('id','title','goal_amount','fund_raised','start_date','end_date','status','user','category','donor',)
   
    def get_user(self,obj):
        return obj.user.username
   
    def get_category(self,obj):
        return obj.category.name
   
########################################################################################################
# Convert UUID to integer
    
class SequentialIntegerField(serializers.Field):
    def to_representation(self, value):
        return self.context['counter']
        
class DonorRecentSerializer(ModelSerializer):
    class Meta:
        model = Donor
        fields =["full_name", "amount"]

class CampaignCategorySerializer1(ModelSerializer):
    class Meta:
        model  = Campaigncategory
        fields = ("id","name","is_active")

class UserSerializerCampaign(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'mobile_number']

class CampaignAdminSerializer1(ModelSerializer):
    id = SequentialIntegerField()
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_mobile_number = serializers.CharField(source='user.mobile_number', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'title','user_username', 'user_email','user_mobile_number','goal_amount', 'fund_raised', 'status', 'start_date', 'end_date']

class DocumentSerializer1():
    models = Documents
    fields = ['doc_file']

class CampaignAdminSerializer2(ModelSerializer):
   
    doc_file = DocumentSerializer(source='documents')

    class Meta :
        model  = Campaign
        fields = ['title', 'category', 'goal_amount', 'location', 'zakat_eligible', 'end_date', 'description', 'status', 'summary', 'doc_file','is_featured']

class CampaignEditSerializer(ModelSerializer):

    class Meta :
        model  = Campaign
        fields = ['title', 'category', 'goal_amount', 'location', 'zakat_eligible', 'end_date', 'description', 'summary']
#############################################################################################################################################################
