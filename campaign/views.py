from django.shortcuts import render
from .serializers import * 
from .models import (
    Campaign,
    CampaignCatagories,
    BenificiaryBankDetails,
    KycDetails
)
from rest_framework.views import APIView
from donor.models import Donor

from fairseed.GM import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from .serializers import CampaignSerializer
from django.db.models import Count, Sum
from django.db.models import F

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


###################### MY CODE ############################


class CampaignGetApi(APIView):
    def get(self,request):
        ongoing_campaign = Campaign.objects.all()
        serializer = CampaignSerializer(ongoing_campaign, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
class CampaignCatagoriesGetApi(APIView):
    def get(self, request):
        CampaignCategory = CampaignCatagories.objects.all()
        serializer = CampaignCatagorySerializer(CampaignCategory, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CampaignRaisedUserApi(APIView):
    def get(self, request):
        campaign_raised = Campaign.objects.annotate(user_count=Count('user'))
        total_user_count = campaign_raised.aggregate(causes_raised=Count('user'))['causes_raised']
        return Response({'causes_raised': total_user_count}, status=status.HTTP_200_OK)
    

class SuccessfulCampaignCount(APIView):
    def get(self, request):
        successful_campaigns = Campaign.objects.filter(fund_raised__gte=F('donor__amount'))
        total_successful_campaigns = successful_campaigns.count()

        return Response({'total_successful_campaigns': total_successful_campaigns}, status=status.HTTP_200_OK)
        

class CampaignDetailApi(APIView):
    def get(self, request):
        campaign_raised = Campaign.objects.annotate(user_count=Count('user'))
        total_user_count = campaign_raised.aggregate(causes_raised=Count('user'))['causes_raised']

        campaign_fund_raised = Campaign.objects.annotate(total_fund_raised=Sum('fund_raised'))
        total_fund_raised = campaign_fund_raised.aggregate(sum_fund=Sum('total_fund_raised'))['sum_fund']

        total_donor = Donor.objects.count()

        total_donor_amount = Donor.objects.annotate(total_f=Sum('amount'))
        total_f = total_donor_amount.aggregate(sum_f=Sum('total_f'))['sum_f']
        print(total_f)

        # Successful campaign count
        cam_model:Campaign = Campaign.objects.all()
        successful_cam = 0
        for camp in cam_model:
            print(type(camp.fund_raised))
            print(type(camp.goal_amount))
            print(camp.fund_raised)
            print(camp.goal_amount)
            # print(camp.fund_raised == )
            if camp.fund_raised == camp.goal_amount:
                successful_cam += 1
        print(camp.goal_amount)

        #Successful Student Count 
        # cam_cat:CampaignCatagories = CampaignCatagories.objects.all()
        # suc_std = 0
        # cam_cat = CampaignCatagories.objects.filter(name='Education')
        # for c in cam_cat:
        #     if c.fund_raised >= c.goal_amount:
        #         suc_std += 1

        return Response({
            'causes_raised': total_user_count,
            'fund_raised': total_fund_raised,
            'donor_total': total_donor,
            'sum123': total_f,
            # 'successful_campaign': camp_status,
            'success_cam': successful_cam,
            # 'std_student': suc_std
        },
            status=status.HTTP_200_OK)
    
class success_cam(APIView):
        def get(self, request):
            success_count = Campaign.objects.filter(is_successful=True).count()
            return Response({'Succcessful_campaign_count':success_count}, status=status.HTTP_200_OK)
        



    


