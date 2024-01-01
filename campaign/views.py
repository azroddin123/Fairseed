from django.core.paginator import Paginator
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

# class CardAPIView(APIView):
#     def get(self, request):
#         campaigns = Campaign.objects.annotate(cause_fund_raised=F('fund_raised'))

#         total_donor_amount = Donor.objects.annotate(total_amt=Sum('amount'))
#         total_amt = total_donor_amount.aggregate(sum_donor=Sum('total_amt'))['sum_donor']

#         total_donor_per_campaign = Donor.objects.all().count()

#         today_date = timezone.now().date()

#         all_campaigns_data = []

#         for c1 in campaigns:
#             if c1.end_date:
#                 days_remaining = (c1.end_date - today_date).days
#                 if days_remaining >= 0:
#                     days_left_message = f'{days_remaining} days left'
#                 else:
#                     days_left_message = 'Campaign ended'
#             else:
#                 days_left_message = 'No end date'

#             api_data = {
#                 'id': c1.id,
#                 'title': c1.title,
#                 'description': c1.description,
#                 'fund_raised': c1.fund_raised,
#                 'days_left': days_left_message,
#                 'sum_of_donor': total_amt,
#                 'num_donors': total_donor_per_campaign
#             }

#             all_campaigns_data.append(api_data)

#         return Response(all_campaigns_data, status=status.HTTP_200_OK)
    
class CardAPIViewPagination(APIView):
    
    def get(self, request):
        page_size = 8
        page_number = int(request.GET.get("page",1))

        campaigns = Campaign.objects.annotate(cause_fund_raised=F('fund_raised'))

        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        paginated_campaigns = campaigns[start_index:end_index]

        all_campaigns_data = []
        print("test")
        
        for c1 in paginated_campaigns:
            print("test1")
            print(c1)
            # to calculate the number of donors and total amount
            donors_per_campaign = Donor.objects.filter(campaign=c1)
            # Campaign.objects.get(id = 1)
            # donors:Donor = Donor.objects.filter(campaign=1)
            # print(donors_per_campaign)
            num_donors = donors_per_campaign.count()
            sum_amt = donors_per_campaign.aggregate(sum_amt=Sum('amount'))['sum_amt'] if donors_per_campaign.exists() else 0
            
            today_date = timezone.now().date()

            if c1.end_date:
                days_remaining = (c1.end_date - today_date).days
                if days_remaining >= 0:
                    days_left_message = f'{days_remaining} days left'
                else:
                    days_left_message = 'Campaign ended'
            else:
                days_left_message = 'No end date'
            
            api_data = {
                'id': c1.id,
                'title': c1.title,
                'description': c1.description,
                'fund_raised': c1.fund_raised,
                'days_left': days_left_message,
                'sum_of_donor': sum_amt,
                'num_donors': donors_per_campaign,
            }


            all_campaigns_data.append(api_data)

        return Response(all_campaigns_data, status=status.HTTP_200_OK)
    
# class Ongoing_Campaign_Api_built_in(APIView):
#     def get(self, request):
#         oc1=Campaign.objects.all()
#         p=Paginator(oc1,8)
#         page_number=request.GET.get("page")
#         page_object = p.get_page(page_number)
#         serializer=CampaignSerializer(page_object, many=True)
#         return Response(serializer.data)
    
# class Ongoing_Campaign_Api(APIView):
#     def get(self,request):
#         oc1=Campaign.objects.all()
#         page_size=8
#         page_number=int(request.GET.get("page",1))
#         start_index=(page_number-1)*page_size
#         end_index=start_index+page_size
#         page_object=oc1[start_index:end_index]
#         serializer=CampaignSerializer(page_object, many=True)
#         return Response(serializer.data)
    
class CausesbyCategoryAPI(APIView):
    def get(self,request):
        causes_by_category = Campaign.objects.all()
        titles = [campaigns.title for campaigns in causes_by_category]
        return Response(titles, status=status.HTTP_200_OK)
        
# class CausesbyCategoryAPI(APIView):
#     def get(self,request):
#         names_of_category=get_object_or_404(CampaignCatagories)
#         cause_name=CampaignCatagories.objects.filter(name=names_of_category)
#         return Response(cause_name, status=status.HTTP_200_OK)

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


