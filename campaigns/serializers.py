from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.serializers import UserAdminSerializer
from donors.models import Donor
from donors.serializers import DonorSerializer1
from .models import * 

class CampaignCatagorySerializer(ModelSerializer):
    class Meta:
        model  = CampaignCatagory
        fields = "__all__"

class CampaignSerializer(ModelSerializer):
    class Meta :
        model  = Campaign
        fields = "__all__"

class CampaignSerializer1(ModelSerializer):
    class Meta :
        model   = Campaign
        exclude = ["is_successfull","status","is_featured","is_reported","is_scholarship","course"]


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


class CampaignByCatagorySerializer(ModelSerializer):
    campaign    = CampaignSerializer1(source="campaign_set",many=True)
    class Meta :
        model   = CampaignCatagory
        fields  = "__all__"

class CampaignAdminSerializer(ModelSerializer):
    user       = UserAdminSerializer()
    class Meta :
        model  = Campaign
        fields = ('id','title','goal_amount','fund_raised','start_date','end_date','status','user')

class DocumentSerializer(ModelSerializer):
    class Meta :
        model  = Documents
        fields = "__all__"


class CampaignDetailSerializer(ModelSerializer):
    donor = DonorSerializer1(source="donors",many=True)
    class Meta :
        model   = Campaign
        fields  = ('id','title','goal_amount','fund_raised','start_date','end_date','status','user','donor')
