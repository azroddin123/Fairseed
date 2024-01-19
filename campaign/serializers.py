from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import * 

class CampaignCatagorySerializer(ModelSerializer):
    class Meta:
        model = CampaignCatagories
        fields = "__all__"

    
class CampaignSerializer(ModelSerializer):
    image = serializers.ImageField(source='image.url', required=False)

    class Meta :
        model = Campaign
        fields = "__all__"


class BBDetailSerailizer(ModelSerializer):
    class Meta :
        model = BenificiaryBankDetails
        fields = "__all__"
    

class KycDetailSerializer(ModelSerializer):
    class Meta :
        model = KycDetails
        fields = "__all__"

##############################################################

class CampaignCatagories1(ModelSerializer):
    class Meta:
        model = Campaign
        exclude = ['is_std_benefited']

class CampaignCauseSerializer(ModelSerializer):
    class Meta:
        model = CampaignCause
        fields = "__all__"

