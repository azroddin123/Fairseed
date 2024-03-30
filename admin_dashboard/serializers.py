from .models import * 
from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers

from donors.models import Withdrawal
from campaigns.models import * 
from campaigns.serializers import * 

class CampSerializer(ModelSerializer):
    class Meta :
        model = Campaign
        fields = ('id','title','rasing_for')

class CampBankKycSerializer(ModelSerializer):
    campaign = CampSerializer(read_only=True)
    class Meta :
        model = BankKYC
        fields = "__all__"


class ReportedCampaignSerializer(ModelSerializer):
    campaign = CampSerializer(read_only=True)
    class Meta :
        model = ReportedCampaign
        fields = "__all__"

class KS(ModelSerializer):
    class Meta :
        model = Keyword
        fields = ("name",)
        
        
class GSSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSetting
        fields = ('id','namesite','welcome_text','welcome_subtitle','description','email_admin','tandc_url','privacy_policy_url','email_no_reply','new_registration_enabled','auto_approve_enabled','email_verification_enabled','facebook_login_enabled','google_login_enabled','captcha_enabled','date_format','keywords')
    
class KeywordSerializer(ModelSerializer):
    class Meta :
        model = Keyword
        fields = "__all__"

class LimitSerializer(ModelSerializer):
    class Meta :
        model = Limit
        fields = "__all__"

class SocialProfileSerializer(ModelSerializer):
    class Meta :
        model = SocialProfile
        fields = "__all__"
    
class LandingPageSerializer(ModelSerializer):
    class Meta :
        model = LandingPage
        fields = "__all__"

class PageSerializer(ModelSerializer):
    class Meta :
        model = Pages
        fields = "__all__"
        
class UserAdminSerializer1(ModelSerializer):
    user_role = serializers.SerializerMethodField(read_only=True)
    campaign_count = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model  = User
        fields = ('id','username','email','mobile_number','created_on','user_type','user_role','password','is_active','country','password','campaign_count')

    def get_user_role (self,obj):
        return obj.user_role.role_name if obj.user_role else None
    
    def get_campaign_count(self,obj):
        return obj.campaigns.count()
    
# class UserSerializer(ModelSerializer):
#     class Meta :
#         model = User 
#         fields = "__all__"

class WithdrawalSerializer1(ModelSerializer):
    
    class Meta :
        model = Withdrawal
        fields = "__all__"


class UserSerializer2(ModelSerializer):
    class Meta :
        model = User
        exclude = ("last_login","created_on","updated_on","is_admin","password")


class CauseEditSerializer1(ModelSerializer):
    campaign = CampaignDocumentSerializer(read_only=True)
    class Meta :
        model = CauseEdit
        fields= ('id','campaign','campaign_data','doc1','doc2','doc3')