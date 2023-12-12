from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import * 

class CampaignCatagorySerializer(ModelSerializer):
    class Meta:
        model = CampaignCatagories
        fields = "__all__"

class CampaignSerializer(ModelSerializer):
    class Meta :
        model = Campaign
        fields = "__all__"

class CampaignSerializer1(ModelSerializer):
    class Meta :
        model = Campaign
        exclude = ["is_successfull","status","is_featured","is_reported","is_scholarship","course"]

class BBDetailSerailizer(ModelSerializer):
    class Meta :
        model = BenificiaryBankDetails
        fields = "__all__"
    

class KycDetailSerializer(ModelSerializer):
    class Meta :
        model = KycDetails
        fields = "__all__"


class DashboardSerializer(serializers.Serializer):
    total_campaign = serializers.IntegerField()
    total_donation = serializers.IntegerField()
    donor_count    = serializers.IntegerField()
    successfull_campaign = serializers.IntegerField()
    student_benifited  = serializers.IntegerField()
