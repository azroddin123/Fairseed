from django.shortcuts import render, get_object_or_404,get_list_or_404
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
from django.core.paginator import Paginator, EmptyPage

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
        

class CampaignCatagoriesListAPI(APIView):
    def get(self, request):
        list = CampaignCatagories.objects.all()
        serializer = CampaignCatagorySerializer(list, many=True)
        name_list = [item['name'] for item in serializer.data]
        return Response(name_list, status=status.HTTP_200_OK)
    
class StdBenefitedCountAPI(APIView):
    def get(self, request):
        b_std= Campaign.objects.filter(is_std_benenfited=True).count()
        return Response({'std_benefited': b_std})
    
class SuccessCount(APIView):
#     def get(self, request):
#         s_c = Campaign.objects.filter(is_successful=True).count()
#         return Response({'Success_count': s_c})
    
# class MethodStdBen(APIView):
    def get(self, request):
        camp = Campaign.objects.filter(catagory__name='Education', fund_raised=F('goal_amount'))
            
        for campaign in camp:
            print(f"Setting is_std_benefited to True for campaign {campaign.pk}")
            campaign.is_std_benenfited = True
            campaign.is_std_benenfited += 1
            campaign.save()
        
        return Response({'message': 'View logic executed successfully'})
    
class CampaignCategoryCausesAPI(APIView):
    def get(self, request, pk):
        camp= get_object_or_404(Campaign, pk=pk)
        s1={
            "title":camp.title,
            # "image":camp.image,
        }
        return Response(s1, status=status.HTTP_200_OK)
    # def get(self,request,pk):
        # camp = get_object_or_404(Campaign, pk=pk)
        # title = camp.title
        # return Response({"Title": title}, status=status.HTTP_200_OK)
    
class CapmPaginationApi(APIView):
    def get(self, request):
        camp = Campaign.objects.all()
        all_titles = Campaign.objects.values_list('title', flat=True)
        page_size = 3
        page_number = int(request.GET.get("page", 1))
        try:
            start_index = (page_number - 1) * page_size
            end_index = start_index + page_size

            paginated_titles = all_titles[start_index:end_index]
            response_data = {
                "Title": list(paginated_titles),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except EmptyPage:
            return Response({"Title": None}, status=status.HTTP_200_OK)

    # def get(self, request, pk):
    #     # Assuming you have a queryset for campaigns
    #     queryset = Campaign.objects.all()

    #     # Get the total number of items
    #     total_items = queryset.count()

    #     # Set the desired number of items per page
    #     items_per_page = 1

    #     # Get the page number from the request
    #     page_number = int(request.GET.get("page", 1))

    #     # Calculate the start and end indices for the current page
    #     start_index = (page_number - 1) * items_per_page
    #     end_index = start_index + items_per_page

    #     # Slice the queryset for the current page
    #     paginated_queryset = queryset[start_index:end_index]

    #     # Serialize the paginated queryset
    #     serializer = CampaignSerializer(paginated_queryset, many=True)

    #     # Construct the response data
    #     response_data = {
    #         "title": serializer.data[0]['title'],  # Assuming there is only one item per page
    #         # Add other fields as needed
    #     }

    #     return Response(response_data, status=status.HTTP_200_OK)


class CampaignCause(APIView):
    def post(self, request):
        serializer = CampaignCauseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        camp_cause = CampaignCause.objects.all()


        




    


