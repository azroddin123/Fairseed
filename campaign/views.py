from django.shortcuts import render
from .serializers import * 
from .models import (
    Campaign,
    CampaignCatagories,
    BenificiaryBankDetails,
    KycDetails
)
from rest_framework.views import APIView

from fairseed.GM import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CampaignApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field = "id"

class  CampaignCatagoryApi(GenericMethodsMixin,APIView):
    model = CampaignCatagories
    serializer_class = CampaignCatagorySerializer
    lookup_field = "id"

class BBDApi(GenericMethodsMixin,APIView):
    model = BenificiaryBankDetails
    serializer_class = BenificiaryBankDetails
    lookup_field = "id"

class KycApi(GenericMethodsMixin,APIView):
    model = KycDetails
    serializer_class = KycDetailSerializer
    lookup_field = "id"


