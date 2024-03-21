
from campaigns.models import Campaign
from donors.models import Donor
from portals.choices import CampaignChoices
from django.db import models


def update_campaign_fund():
   campaigns = Campaign.objects.filter(status=CampaignChoices.PENDING)
   for campaign in campaigns:
        total_donation = Donor.objects.filter(campaign=campaign).aggregate(total_amount=models.Sum('amount'))['total_amount']
        campaign.fund_raised = total_donation if total_donation else 0
        campaign.save()



