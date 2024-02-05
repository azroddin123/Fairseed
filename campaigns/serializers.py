from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers
from accounts.serializers import UserAdminSerializer, UserSerializer
from donors.models import Donor
from donors.serializers import DonorSerializer1
from .models import * 

class CampaigncategorySerializer(ModelSerializer):
    class Meta:
        model  = Campaigncategory
        fields = "__all__"

class CampaignSerializer(ModelSerializer):
    class Meta :
        model  = Campaign
        fields = "__all__"

    
    # def save(self):
    #     pass


class CampaignSerializer1(ModelSerializer):
    class Meta :
        model   = Campaign
        exclude = ["is_successful","status","is_featured","is_reported","is_withdrawal"]


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
    user       = UserAdminSerializer()
    class Meta :
        model  = Campaign
        fields = ('id','title','goal_amount','fund_raised','start_date','end_date','status','user','category')

class DocumentSerializer(ModelSerializer):
    class Meta :
        model  = Documents
        fields = "__all__"


class CampaignDetailSerializer(ModelSerializer):
    donor = DonorSerializer1(source="donors",many=True)
    class Meta :
        model   = Campaign
        fields  = ('id','title','goal_amount','fund_raised','start_date','end_date','status','user','donor')

#############################################################################
        
class RecentDonorSerializer(ModelSerializer):
    class Meta:
        model = Donor
        fields = ['full_name', 'amount', 'created_on']


class CampaignCauseSerializer(ModelSerializer):
    class Meta:
        model = CampaignCause
        fields = "__all__"

class CampaigncategorySerializer1(ModelSerializer):
    class Meta:
        model  = Campaigncategory
        exclude = ['created_on', 'updated_on'] 


class CampaigncategorySerializer2(ModelSerializer):
    class Meta:
        model  = Campaigncategory
        fields = ['id','name','is_active']


class CampaignSerializer2(ModelSerializer):
    user_info = UserAdminSerializer(source='user', read_only=True)
    class Meta:
        model = Campaign
        fields = ('id','title','goal_amount','fund_raised','start_date','end_date','status','user','user_info')

class CampaignSearchSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    username = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=False)
    goal_amount = serializers.CharField(required=False)
    fund_raised = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    # sort_by = serializers.CharField(allow_blank=True, required=False)
    # sort_order = serializers.ChoiceField(choices=[('asc', 'Ascending'), ('desc','Descending')], allow_blank=True, required=False)

class ReportedCampaignSerilaizer(ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('id','user', 'start_date','title')

class CamapaignDetailSerializer(ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('user','campaign_image','title','goal_amount','location','category','zakat_eligible','end_date')

class CampaignDocSerializer(ModelSerializer):
    class Meta:
        model = Documents
        fields = ['doc_file']

class CampaignStorySerializer(ModelSerializer):
    doc = CampaignDocSerializer(source='documents', read_only=True)
    class Meta :
        model = Campaign
        fields = ('description','summary','goal_amount','category_id','doc')
        extra_kwargs = {
        'category_id': {'required': False}  
    }

class CampaignAccSerailaizer(ModelSerializer):
    class Meta :
        model = Campaign
        fields = ['rasing_for']

class CamapaignAccountSerializer(ModelSerializer):
    # user_info = CampaignAccSerailaizer(source='user1')
    class Meta:
        model = CampaignKycBenificiary
        fields = ['account_holder_name','account_number','bank_name','branch_name','ifsc_code','passbook_image']

class CampaignDetailStorySerializer(ModelSerializer):
    doc = CampaignDocSerializer(source='campaign', read_only=True)
    class Meta:
        model = Campaign
        fields = ('user','campaign_image','title','goal_amount','location','category','zakat_eligible','end_date','description','summary','doc')
    
class CamapaignKYCSerializer(ModelSerializer):
    class Meta:
        model  = CampaignKycBenificiary
        fields = ('adhar_card','adhar_card_image', 'pan_card','pan_card_image')

class CamapaignCreateSerializer(serializers.ModelSerializer):
    doc = CampaignDocSerializer(source='documents', read_only=True)
    acc_detail = CamapaignAccountSerializer(source='bank_details',read_only=True)
    kyc_detail = CamapaignKYCSerializer(source='bank_details',read_only=True)
    class Meta:
        model = Campaign
        fields = ('user','campaign_image','title','goal_amount','location','category','zakat_eligible','end_date','description','summary','goal_amount','doc','rasing_for','acc_detail','kyc_detail')

    
class DocumentSerializer3(ModelSerializer):
    models = Documents
    fields = ['doc_file']

class CampaignAdminSerializer3(ModelSerializer):
    documents = DocumentSerializer3(many=True)
    class Meta :
        model  = Campaign
        fields = ['title', 'category', 'goal_amount', 'location', 'zakat_eligible', 'end_date', 'description', 'status', 'summary', 'documents','is_featured']

class CampaignAdminPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['category', 'title', 'goal_amount', 'location', 'zakat_eligible', 'status', 'end_date', 'description', 'summary', 'is_featured', 'campaign_image' ]

class CampaignModificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Campaign
        fields = ['updated_on', 'user_name']

class CampaignAdminSerializer1(ModelSerializer):
    # id = SequentialIntegerField()
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_mobile_number = serializers.CharField(source='user.mobile_number', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'title','user_username', 'user_email','user_mobile_number','goal_amount', 'fund_raised', 'status', 'start_date', 'end_date']

class CampaignViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignView
        fields = ['id', 'campaign', 'timestamp', 'user']

class DashboradCampaignSerailaizer(ModelSerializer):
    class Meta:
        model = Campaign
        fields  = ['id', 'title','user','goal_amount', 'fund_raised', 'status', 'start_date', 'end_date']

# class DCampaignSerializer(ModelSerializer):
#     class Meta :
#         model  = Campaign
#         fields = ('title','goal_amount','fund_raised','start_date','end_date','status','category','campaign_image','location','zakat_eligible','')


class DashboardDonorSerializer1(serializers.ModelSerializer):
    campaign_title = serializers.SerializerMethodField()
    class Meta:
        model = Donor
        fields = ['id','full_name','pancard','campaign','amount','payment_type','comment','created_on','is_anonymous','campaign_title']

    def get_campaign_title(self, obj):
        # Access the campaign associated with the donor and get its title
            if obj.campaign:
                return obj.campaign.title
            else:
                return None 
            
class CamapaignKYCAPSerializer(ModelSerializer):
    campaign_id = SerializerMethodField()
    campaign_title = SerializerMethodField()
    class Meta:
        model = CampaignKycBenificiary
        fields = ['campaign_title','id','account_holder_name','account_number','campaign_id','bank_name','ifsc_code','is_verified']

    def get_campaign_id(self, obj):
        if obj.campaign:
            return obj.campaign.id
        else:
            return None
    def get_campaign_title(self, obj):
        if obj.campaign:
            return obj.campaign.title
        else:
            return None
        
class CamapaignKYCViewSerializer(ModelSerializer):
    campaign_raising_for = SerializerMethodField()
    campaign_title = SerializerMethodField()
    class Meta:
        model = CampaignKycBenificiary
        fields = ['campaign_id','campaign', 'account_holder_name', 'account_number', 'bank_name', 'branch_name', 'ifsc_code', 'passbook_image', 'pan_card', 'pan_card_image', 'adhar_card', 'adhar_card_image', 'other_details', 'is_verified','campaign_raising_for','campaign_title']

    def get_campaign_raising_for(self, obj):
        if obj.campaign:
            return obj.campaign.rasing_for
        else:
            return None
        
    def get_campaign_id(self, obj):
        if obj.campaign:
            return obj.campaign.id
        else:
            return None

    def get_campaign_title(self, obj):
        if obj.campaign:
            return obj.campaign.title
        else:
            return None
        
class CamapaignViewKYCViewSerializer(ModelSerializer):
    campaign_raising_for = SerializerMethodField()
    updated_on = serializers.SerializerMethodField()

    class Meta:
        model = CampaignKycBenificiary
        fields = ['campaign_id', 'account_holder_name', 'account_number', 'bank_name', 'branch_name', 'ifsc_code', 'passbook_image', 'pan_card', 'pan_card_image', 'adhar_card', 'adhar_card_image', 'other_details', 'is_verified','updated_on','campaign_raising_for']

    def get_campaign_raising_for(self, obj):
        if obj.campaign:
            return obj.campaign.rasing_for
        else:
            return None
            
    def get_updated_on(self, obj):
        if obj.updated_on:
            return obj.updated_on.strftime('%d-%m-%Y')  # Format the datetime as 'dd-mm-yyyy'
        else:
            return None
        
class CamapaignAdminPKYCSerializer(ModelSerializer):
    campaign_raising_for = SerializerMethodField()
    campaign_title = SerializerMethodField()
    class Meta:
        model = CampaignKycBenificiary
        fields = ['account_holder_name', 'account_number', 'bank_name', 'branch_name', 'ifsc_code', 'passbook_image', 'pan_card', 'pan_card_image', 'adhar_card', 'adhar_card_image', 'other_details', 'is_verified','campaign_raising_for','campaign_title']

    def get_campaign_raising_for(self, obj):
        if obj.campaign:
            return obj.campaign.rasing_for
        else:
            return None

    def get_campaign_title(self, obj):
        if obj.campaign:
            return obj.campaign.title
        else:
            return None       
    # def get_campaign_id(self, obj):
    #     if obj.campaign:
    #         return obj.campaign.id
    #     else:
    #         return None