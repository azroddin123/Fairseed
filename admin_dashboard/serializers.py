from .models import * 
from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers

from campaigns.models import * 
from campaigns.serializers import * 

class CampSerializer(ModelSerializer):
    class Meta :
        model = Campaign
        fields = ('id','title')

class CampBankKycSerializer(ModelSerializer):
    campaign = CampSerializer(read_only=True)
    class Meta :
        model = BankKYC
        fields = "__all__"

# class GSSerializer(ModelSerializer):
#     keywords = serializers.ListField(child=serializers.CharField(),write_only=True)
#     class Meta :
#         model = GeneralSetting
#         exclude = ("new_registration_enabled","auto_approve_enabled","email_verification_enabled","facebook_login_enabled","google_login_enabled")

#     def save(self, *args, **kwargs):
#         gs = super().save(*args, **kwargs)
#         keywords_list = self.validated_data.get("keywords")
#         print(keywords_list)
#         print("----------------------",gs)
#         for item in keywords_list : 
#             print(Keyword.objects.create(gs=gs,name=item))
#         # Your additional actions or data update logic here
#         pass
    
    
class KS(ModelSerializer):
    class Meta :
        model = Keyword
        fields = ("name",)
        
        
class GSSerializer(serializers.ModelSerializer):
    keywords = serializers.ListField(child=serializers.CharField(), write_only=True,required=False,allow_null=True,allow_empty=True)
    keywords_data = KS(source="keyword_set",many=True,read_only=True)
    class Meta:
        model = GeneralSetting
        fields = ('id','namesite','welcome_text','description','email_admin','tandc_url','privacy_policy_url','email_no_reply','new_registration_enabled','auto_approve_enabled','email_verification_enabled','facebook_login_enabled','google_login_enabled','keywords','keywords_data')
    
    def create(self, validated_data):
        keywords_data = validated_data.pop('keywords', [])
        gs = GeneralSetting.objects.create(**validated_data)
        for item in keywords_data:
            Keyword.objects.create(gs=gs, name=item)
        return gs
    
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
    
    def save(self,*args, **kwargs):
        data = SocialProfile.objects.all()
        print("data",data)
        data.delete()
        return super().save(*args, **kwargs)

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
    campaign_count  = serializers.SerializerMethodField(read_only=True)
    class Meta :
        model  = User
        fields = ('id','username','email','mobile_number','created_on','user_type','user_role','password','is_active','country','password','campaign_count')

    def get_user_role (self,obj):
        return obj.user_role.role_name if obj.user_role else None
    
    def get_campaign_count(self,obj):
        return obj.campaigns.count()
    
class UserSerializer(ModelSerializer):
    class Meta :
        model = User 
        fields = "__all__"
    # def get_campaign_count(self, obj):
    #       return obj.campaigns.count()
