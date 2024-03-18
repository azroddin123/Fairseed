from campaigns.models import * 
from campaigns.serializers import * 
from rest_framework.serializers import ModelSerializer

class UserCampaignSerializer(ModelSerializer):
    class Meta :
        model = Campaign
        fields = ('id','title','campaign_image','story','summary','zakat_eligible','goal_amount','location','fund_raised','end_date','days_left','status',"is_reported","is_successful","is_featured")