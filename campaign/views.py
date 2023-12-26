from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from donor.models import Donor
from fairseed.GM import GenericMethodsMixin

from .models import (BenificiaryBankDetails, Campaign, CampaignCatagories,
                     KycDetails)
from .serializers import *

# Create your views here.

##########################################################################

class CardAPIView(APIView):
    def get(self, request):
        c1=Campaign.objects.all()
        
        # c1= get_object_or_404(Campaign, pk=pk)
        
        campaigns = Campaign.objects.annotate(cause_fund_raised=F('fund_raised'))
        
        #Calculating how much fund has been generated out of fund raised for this specific campaign
        total_donor_amount = Donor.objects.annotate(total_amt=Sum('amount'))
        total_amt = total_donor_amount.aggregate(sum_donor=Sum('total_amt'))['sum_donor']
        
        #Calculating number of donors who have contributed for this specific campaign
        total_donor_per_campaign = Donor.objects.all().count()

        serializers = CampaignSerializer(c1, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

class SuccessAPI(APIView):
        def get(self, request):
            success_count = Campaign.objects.filter(is_successful=True).count()
            return Response({'Succcessful_campaign_count':success_count}, status=status.HTTP_200_OK)
        
class CCAPI(APIView):
    def get(self, request, id):
        c1 = CampaignCatagories.objects.filter(pk=id).exists()
        c2 = CampaignCatagories.name
        if c1:
            c2 = CampaignCatagories.objects.get(pk=id).name
            CampaignCatagories.objects.filter(status=False).update(status=False)
            return Response({f"Category {c2} is inactive"})
        else:
            return Response({f"Category does not exists"})
        
class DashboardAPI(APIView):
    def get(self, request):
        pk = request.GET.get('pk')

        #Total Donations
        total_donations = Donor.objects.all().count()

        #Total Funds Raised
        total_fund_raised_all_campaigns = Campaign.objects.aggregate(total_fund_raised = Sum('fund_raised'))['total_fund_raised'] or 0

        #Total causes raised/Campaign caused raised
        number_of_causes = Campaign.objects.all().count()

        #Members or users who have sign up 
        number_of_members = User.objects.all().count()
        
        serialized_data = {
            'Total Donation': total_donations,
            'Fund Raised' : total_fund_raised_all_campaigns,
            'Causes' : number_of_causes,
            'Members' : number_of_members,
        }

        return Response(serialized_data, status=status.HTTP_200_OK)

class CausesbyCategoryAPI(APIView):
    def get(self,request):
        causes_by_category = CampaignCatagories.objects.all()
        titles = [category.name for category in causes_by_category]
        return Response(titles, status=status.HTTP_200_OK)
##########################################################################
    
class CampaignCatagoriesView(APIView):
    def get(self, request):
        campaigns_categories = CampaignCatagories.objects.all()
        serializer = CampaignCatagorySerializer(campaigns_categories, many=True)
        return Response(serializer.data)

class CampaignView(APIView):
    def get(self, request):
        campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)


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


