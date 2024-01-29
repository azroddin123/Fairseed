from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.serializers import UserAdminSerializer
from donors.models import Donor
from donors.serializers import DonorSerializer1
from payment_gateways.models import BankTransfer
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
        fields = ("id","name","is_active","image")

class UserSerializerCampaign(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'mobile_number']

class CampaignAdminSerializer1(ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_mobile_number = serializers.CharField(source='user.mobile_number', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'title','user_username', 'user_email','user_mobile_number','goal_amount', 'fund_raised', 'status', 'start_date', 'end_date']

# class DocumentSerializer1(ModelSerializer):
#     model = Documents
#     fields = ['doc_file']

class CampaignAdminSerializer2(ModelSerializer):

    # documents = DocumentSerializer1(many=True)

    class Meta:
        model = Campaign
        fields = ['title', 'category', 'goal_amount', 'location', 'zakat_eligible', 'end_date', 'description', 'status', 'summary', 'is_featured']

class CampaignModificationSerializer(serializers.ModelSerializer):
    modification_history = serializers.SerializerMethodField()

    class Meta:
        model = CampaignModification
        fields = ['campaign_id', 'modification_history']

class CampaignEditSerializer(ModelSerializer):

    class Meta :
        model  = Campaign
        fields = ['title', 'category', 'goal_amount', 'location', 'zakat_eligible', 'end_date', 'description', 'summary']

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = ('payment_type',)

class UserWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile_number')

class CampaignWithdrawalSerializer(serializers.ModelSerializer):
    user = UserWithdrawalSerializer()
    # donor_payments = DonorSerializer(many=True, read_only=True, source='donors')

    class Meta:
        model = Campaign
        fields = ('id', 'title', 'fund_raised', 'status', 'end_date', 'user')

# class WithdrawalInsideSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = BankTransfer
#         fields = ('id', 'title', 'bank_details', 'fund_raised', 'payment_gateway', 'end_date', 'status')

# class CampaignKycSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CampaignKycBenificiary
#         fields = ('account_holder_name', 'account_number', 'bank_name', 'ifsc_code', 'other_details')

# class WithdrawalDetailsSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     # campaign = CampaignWithdrawalSerializer()
#     bank_details = CampaignKycSerializer(source='campaign.bank_details')
#     amount = serializers.DecimalField(max_digits=10, decimal_places=2, source='campaign.fund_raised')
#     payment_gateway = serializers.CharField(source='campaign.rasing_for')  # Change this based on your actual field
#     date = serializers.DateField(source='campaign.end_date')
#     status = serializers.CharField(source='campaign.status')
        
class CampaignCKB(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [
            'title', 'rasing_for', 'adhar_card', 'bank_details',
            'goal_amount', 'fund_raised', 'location', 'zakat_eligible',
            'status', 'start_date', 'end_date', 'description', 'summary'
        ]

class CampaignKycSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignKycBenificiary
        fields = [
            'account_holder_name', 'account_number', 'bank_name',
            'branch_name', 'ifsc_code', 'passbook_image',
            'pan_card', 'pan_card_image', 'adhar_card',
            'adhar_card_image', 'other_details', 'is_verified'
        ]

class CombinedSerializer(serializers.ModelSerializer):
    campaign_id = serializers.UUIDField(source='campaign.id')
    campaign_title = serializers.CharField(source='campaign.title')
    campaign_status = serializers.CharField(source='campaign.status')

    class Meta:
        model = CampaignKycBenificiary
        fields = [
            'id', 'account_holder_name', 'account_number', 'ifsc_code', 'bank_name',
            'campaign_id', 'campaign_title', 'campaign_status'
        ]

class CKBViewSerializer(serializers.Serializer):
    campaign_details = CampaignCKB(source='campaign', read_only=True)
    kyc_details = CampaignKycSerializer(source='campaign.bank_details', read_only=True)

    class Meta:
        model = CampaignKycBenificiary
        fields = ['campaign_details', 'kyc_details']
#############################################################################################################################################################
