from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.serializers import UserAdminSerializer
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
        exclude = ["is_successful","status","is_featured","is_reported"]


class CKBSerializer(ModelSerializer):
    class meta :
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
    user_data      = UserAdminSerializer(read_only=True)
    class Meta :
        model  = Campaign
        fields = ('id','title','goal_amount','fund_raised','start_date','end_date','status','category',"user_data","user")

    
class DocumentSerializer(ModelSerializer):
    class Meta :
        model  = Documents
        fields = "__all__"


class CampaignDetailSerializer(ModelSerializer):
    donor = DonorSerializer1(source="donors",many=True)
    class Meta :
        model   = Campaign
        fields  = ('id','title','goal_amount','fund_raised','start_date','end_date','status','user','donor')
