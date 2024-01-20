from django.shortcuts import render, get_object_or_404,get_list_or_404
from django.db.models import Sum, F, Count
from donors.models import Donor
from django.utils import timezone
from .serializers import * 
from .models import (
    Campaign,
    Campaigncategory,
    CampaignKycBenificiary,
)
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.views import APIView
import uuid
import math
from portals.GM1 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage

# Create your views here.
# limit = 10 

class CampaignApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field = "id"

class  CampaigncategoryApi(GenericMethodsMixin,APIView):
    model = Campaigncategory
    serializer_class = CampaigncategorySerializer
    lookup_field = "id"

class CKBApi(GenericMethodsMixin,APIView):
    model = CampaignKycBenificiary
    serializer_class = CKBSerializer
    lookup_field = "id"

# class KycApi(GenericMethodsMixin,APIView):
#     model = KycDetails
#     serializer_class = KycDetailSerializer
#     lookup_field = "id"

class CampaignAdminApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignAdminSerializer
    lookup_field  = "id"


class DocumentApi(GenericMethodsMixin,APIView):
    model = Documents
    serializer_class = DocumentSerializer
    lookup_field = "id"



class CampaignFilterApi(APIView):
    def get(self,request,*args, **kwargs):
        try : 
            category = request.GET.get('name')
            campain_id=Campaigncategory.objects.get(name=category)
            campaing_data = Campaign.objects.filter(category=campain_id)
            serializer = CampaignSerializer1(campaing_data,many=True)
            return Response({"error": False, "data" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

# getting some issues in this api
class CampaignBycategoryApi(APIView):  
    def get(self, request, pk, *args, **kwargs):
            try:
                data = Campaigncategory.objects.get(id=pk)
                serializer = CampaignBycategorySerializer(data)
                return Response({"error": False, "data": serializer.data}, status=status.HTTP_200_OK)
            except Campaigncategory.DoesNotExist:
                return Response({"error": "Campaigncategory not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:

                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# Camapaign By Catagory 
# class CampaignBycategoryApi(APIView):  
#     def get(self, request, pk, *args, **kwargs):
#             try:
#                 data = Campaigncategory.objects.get(id=pk)
#                 serializer = CampaignBycategorySerializer(data)
#                 return Response({"error": False, "data": serializer.data}, status=status.HTTP_200_OK)
#             except Campaigncategory.DoesNotExist:
#                 return Response({"error": "Campaigncategory not found"}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class CampaignBycategoryApi(APIView):
#     def get(self,pk,request,*args, **kwargs):
#         # try :
#             print(pk,request.data)
#             data = Campaigncategory.objects.get(id="4faedac9-c908-41db-8d15-a5577f97fecd")
#             serializer = CampaignBycategorySerializer(data)
#             return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
#         # except Exception as e :
#             return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

class ReportedCauseApi(APIView):
    def get(self,request,*args, **kwargs) :
        try :
            data = Campaign.objects.filter(is_reported=True)
            serializer = CampaignSerializer1(data,many=True)
            return Response({"error": False, "data" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

# class CampaignByCategoryApi(APIView):
#     def get(self,request,*args, **kwargs):
#         try : 
#             cat_id = request.GET.get('category')
#             limit = request.GET.get('limit')
#             data = Campaign.objects.filter(category=cat_id)
#             print(data)
#             page_number = request.GET.get('page')
#             if page_number == None or limit == None:
#                 serializer = CampaignAdminSerializer(data,many=True)
#                 return Response({"error": False,"data": serializer.data}, status=status.HTTP_200_OK)
#             pages = int(math.ceil(len(data)/int(limit)))
#             paginator = Paginator(data, limit)
#             data = paginator.get_page(page_number)
#             serializer = CampaignAdminSerializer(data, many=True)
#             return Response({"error": False, "pages_count": pages, "total_records" : len(data),"data": serializer.data}, status=status.HTTP_200_OK)
#         except Exception as e :
#             return Response({"error" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class CampaignByCategoryApi(APIView):
    def get(self, request, *args, **kwargs):
        try:
            cat_id = request.GET.get('category')
            limit = int(request.GET.get('limit', 0))
            page_number = int(request.GET.get('page', 0))

            data = Campaign.objects.filter(category=cat_id)
            
            paginator = Paginator(data, limit)
            current_page_data = paginator.get_page(page_number)
            
            serializer = CampaignAdminSerializer(current_page_data, many=True)
            
            return Response({
                "pages_count": paginator.num_pages,
                "total_records": paginator.count,
                "error": False,
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CampaignDetailsApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field  = "id"
    
    def get(self,request,pk=None,*args, **kwargs):
            print("In Campaign Details API")
            if pk == None or pk == str(0) :
                try : 
                    limit = request.GET.get('limit')
                    data = Campaign.objects.all()
                    page_number = request.GET.get('page')
                    print(page_number,limit,type(limit),type(page_number))
                    if page_number == None or limit == None:
                        serializer = CampaignAdminSerializer(data,many=True)
                        return Response({"error": False,"data": serializer.data}, status=status.HTTP_200_OK)
                    pages = int(math.ceil(len(data)/int(limit)))
                    paginator = Paginator(data, limit)
                    data = paginator.get_page(page_number)
                    serializer = CampaignAdminSerializer(data, many=True)
                    return Response({"error": False, "pages_count": pages, "total_records" : len(data),"data": serializer.data}, status=status.HTTP_200_OK)
                except Campaign.DoesNotExist:
                    return Response({"error" : "Record not found or exists"},status=status.HTTP_400_BAD_REQUEST)
            else :
                data = Campaign.objects.get(pk=pk)
                serializer = CampaignDetailSerializer(data)
                return Response({"error": False, "data" : serializer.data},status=status.HTTP_200_OK)

# Landing page api
class LandingPageApi(APIView):
    def get(self,request,*args, **kwargs) :
        try : 
            data = {
            "total_campaign" : Campaign.objects.count(),
            "total_donation" : Donor.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
            "donor_count" : Donor.objects.count(),
            "successfull_campaign" : Campaign.objects.filter(is_successful=True).count(),
            # this should be done when the amoint is credited to student account.
            "student_benifited" : Campaign.objects.filter(is_withdrawal=True).count()
            }
            serializer = DashboardSerializer(data)
            return Response({"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"data" : serializer.data},status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

##########################################################################################
    
class CampaignGetApi(APIView):
    def get(self,request):
        ongoing_campaign = Campaign.objects.all()
        serializer = CampaignSerializer(ongoing_campaign, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    
class CampaignPostApi(APIView):
    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CampaignDeletePutApi(APIView):
    def put(self, request, pk):
        try:
            camp = Campaign.objects.get(pk=pk)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CampaignSerializer(camp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            campaign = Campaign.objects.get(pk=pk)
            campaign.delete()
            return Response({"message": "Campaign deleted successfully"})
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign does not exist"})
        
        
class CampaignCatagoriesGetApi(APIView):  # camapign get API (Admin Panel)
    def get(self, request):
        CampaignCategory = Campaigncategory.objects.all()
        serializer = CampaigncategorySerializer1(CampaignCategory, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CampaigncategorySerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CamapaignActionApi(APIView):        # campaign Action API(Admin Panel)
    def put(self, request,id):
        try:
            camp = Campaigncategory.objects.get(id=id)
        except Campaigncategory.DoesNotExist:
            return Response({"error": "Campaign Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CampaigncategorySerializer1(camp, data=request.data, )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        try:
            camp = Campaigncategory.objects.get(id=id)
            camp.delete()
            return Response({"message": "Campaign Category deleted successfully"})
        except Campaigncategory.DoesNotExist:
            return Response({"error": "Campaign Category does not exist"})


class CampaignCatagoriesGetApi1(APIView):  # camapign get API (Admin Panel)
    def get(self, request):
        CampaignCategory = Campaigncategory.objects.all()
        serializer = CampaigncategorySerializer(CampaignCategory, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = CampaigncategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
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

        successful_cam = Campaign.objects.filter(is_successful=True).count()

        # cam_std = Campaign.objects.filter(is_std_benenfited=True).count()
        std_ben = Campaign.objects.filter(title='Education', is_withdrawal=True).count()


        return Response({
            'causes_raised': total_user_count,
            'fund_raised': total_fund_raised,
            'donor_total': total_donor,
            'success_cam': successful_cam,
            'std_benefited': std_ben
        },
            status=status.HTTP_200_OK)
        

class CampaignCatagoriesListAPI(APIView):     # get cmapaign category name list.....
    def get(self, request):
        list = Campaigncategory.objects.all()
        serializer = CampaigncategorySerializer(list, many=True)
        name_list = [item['name'] for item in serializer.data]
        return Response(name_list, status=status.HTTP_200_OK)
    
class StdBenefitedCountAPI(APIView):
    def get(self, request):
        b_std= Campaign.objects.filter(is_std_benenfited=True).count()
        return Response({'std_benefited': b_std})
    
    def get(self, request):
        a = Donor.objects.filter()
    
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
        limit = 2
        pg = int(request.GET.get("page", 1))
        all_titles = Campaign.objects.values_list('title', flat=True)
    
        try:
            start_index = (pg - 1) * limit
            end_index = start_index + pg

            paginated_titles = all_titles[start_index:end_index]
            response_data = {
                "Title": paginated_titles,
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

#### getting error #####
class CampaignCause1(APIView):
    def get(self, request, pk):
        camp_cause = get_object_or_404(CampaignCause, pk=pk)
        serializer = CampaignCauseSerializer(camp_cause, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CamapaignCauseApi(APIView):
    def post(self, request):
        serializer = CampaignCauseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        camp = CampaignCause.objects.all()
        serializer = CampaignCauseSerializer(camp, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

            # if c1.end_date:
            #     days_remaining = (c1.end_date - today_date).days
            #     if days_remaining >= 0:
            #         days_left_message = f'{days_remaining} days left'
            #     else:
            #         days_left_message = 'Campaign ended'
            # else:
            days_left_message = 'No end date'
            
            api_data = {
                'id': c1.id,
                'title': c1.title,
                'description': c1.description,
                'fund_raised': c1.fund_raised,
                'days_left': days_left_message,
                'sum_of_donor': sum_amt,
                'num_donors': num_donors,
            }

            all_campaigns_data.append(api_data)

        return Response(all_campaigns_data, status=status.HTTP_200_OK)
    
class OneCardApi(APIView):
    # working one card api
    def get(self, request):
        camp = Campaign.objects.all()
        data1 = []
        for c in camp:
            camp_data={
                "title" : c.title,
                "fund_raised": c.fund_raised,
                "goal_amount": c.goal_amount,
                'is_zakat_aligible': c.zakat_eligible,
                'created_date': c.created_on.strftime('%b %d, %Y %I:%M %p'),
                # "img": c.
            }
        data1.append(camp_data)
        return Response(data1)
    
    
class RecentDonorApi(APIView):   
    def get(self, request, camp_id):
        campaign = get_object_or_404(Campaign, id=camp_id)
        donors = Donor.objects.filter(campaign=campaign)
        # response_data = []
        # for donor in donors:
        #     donor_data = {
        #         "name": donor.full_name,
        #         "amount": donor.amount
                
        #     }
        #     response_data.append(donor_data)
        serializer = RecentDonorSerializer(donors, many=True)

        return Response(serializer.data, status=200)
        # return Response(response_data, status=status.HTTP_200_OK)
    
class practice(APIView):
    def get(self, request):
        u1 = Campaign.objects.all()
        serializer = CampaignSerializer(u1, many = True)
        goal = [ {'goal amout': i['goal_amount'], 'title': i['title']}for i in serializer.data]
        return Response(goal, status=status.HTTP_200_OK)
    
####### Admin Campaign API's   #############

class CampaignGetApi(APIView):   # Campaign get Api (Admin panel)
    def get(self,request):
        ongoing_campaign = Campaign.objects.all()
        serializer = CampaignSerializer2(ongoing_campaign, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)

# class CampaignSearchApi(APIView):
#     def get(self,request):
#         ongoing_campaign = Campaign.objects.all()
#         serializer = CampaignSerializer2(ongoing_campaign, many = True)
#         return Response(serializer.data , status=status.HTTP_200_OK)

#     def get(self, request, *args, **kwargs):
#         serializer = CamapaignSearchSeraializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)
#         queryset = Campaign.objects.all()

#         start_date = serializer.validated_data.get('start_date')
#         username= serializer.validated_data.get('username')
#         title = serializer.validated_data.get('title')
#         email = serializer.validated_data.get('email')
#         mobile_number= serializer.validated_data.get('mobile_number')
#         start_date = serializer.validated_data.get('start_date')
#         goal_amount = serializer.validated_data.get('goal_amount')
#         fund_raised = serializer.validated_data.get('fund_raised')
#         id = serializer.validated_data.get('id')

#         sort_with = serializer.validated_data.get('sort_with')
#         sort_by = serializer.validated_data.get('sort_by')  # get('sort_by','asc')

#         if username:
#             queryset = queryset.filter(user__username__icontains=username)
#         if title:
#             queryset= queryset.filter(title__icontains=title)
#         if mobile_number:
#             queryset = queryset.filter(user__mobile_number__icontains=mobile_number)
#         if email:
#             queryset = queryset.filter(user__email__icontains=email)
#         if start_date:
#             queryset = queryset.filter(start_date__icontains=start_date)
#         if goal_amount:
#             queryset = queryset.filter(goal_amount__icontains=goal_amount)
#         if fund_raised:
#             queryset = queryset.filter(fund_raised__icontains=fund_raised)
#         if id:
#             queryset = queryset.filter(user__id__icontains=id)

#         if sort_with:
#             order_by_field = sort_with
#             if sort_by =='desc':
#                 order_by_field = '-' + order_by_field
#             queryset = queryset.order_by(order_by_field)

#         print(f'Sorting by {sort_with} in {sort_by} order')
#         # print(f'Final queryset: {queryset.query}')

#         serializer = CampaignSerializer2(queryset, many=True)

#         return Response(serializer.data) 




class CampaignSearchApi(APIView):
    def get(self,request):
        ongoing_campaign = Campaign.objects.all()
        serializer = CampaignSerializer2(ongoing_campaign, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        serializer = CamapaignSearchSeraializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = Campaign.objects.all()

        start_date = serializer.validated_data.get('start_date')
        username= serializer.validated_data.get('username')
        title = serializer.validated_data.get('title')
        email = serializer.validated_data.get('email')
        mobile_number= serializer.validated_data.get('mobile_number')
        start_date = serializer.validated_data.get('start_date')
        goal_amount = serializer.validated_data.get('goal_amount')
        fund_raised = serializer.validated_data.get('fund_raised')
        id = serializer.validated_data.get('id')

        sort_with = serializer.validated_data.get('sort_with')
        print(sort_with)
        sort_by = serializer.validated_data.get('sort_by')  # get('sort_by','asc')
        print(sort_by)

        if username:
            queryset = queryset.filter(user__username__icontains=username)
        if title:
            queryset= queryset.filter(title__icontains=title)
        if mobile_number:
            queryset = queryset.filter(user__mobile_number__icontains=mobile_number)
        if email:
            queryset = queryset.filter(user__email__icontains=email)
        if start_date:
            queryset = queryset.filter(start_date__icontains=start_date)
        if goal_amount:
            queryset = queryset.filter(goal_amount__icontains=goal_amount)
        if fund_raised:
            queryset = queryset.filter(fund_raised__icontains=fund_raised)
        if id:
            queryset = queryset.filter(user__id__icontains=id)

        if sort_with:
            print(sort_with)
            # Map frontend field names to model field names for sorting
            field_mapping = {'User': 'user__username', 'Date': 'start_date'}

            if sort_with in field_mapping:
                ordering_field = field_mapping[sort_with]

                if sort_by == 'desc':
                    ordering_field = '-' + ordering_field
                queryset = queryset.order_by(ordering_field)

            print(f'Sorting by {sort_with} in {sort_by} order')
                # print(f'Final queryset: {queryset.query}')

        serializer = CampaignSerializer2(queryset, many=True)

        return Response(serializer.data)


### Admin Panel > Scholarship 
    
class ScholarshipCampaignApi(APIView):
    def get(self, request):
        camp = Campaign.objects.filter(category__name__icontains='Scholarship')
        print(type(camp))
        print(camp)
        print(f'Number of campaign {camp.count()}')
        serializer = CampaignSerializer2(camp, many=True)
        return Response(serializer.data)
    
# campaign cretae Api's
    
class CampaignDetailPostApi(APIView):
    def post(self, request):
        serializer = CamapaignDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CampaignGetApi1(APIView):
    def get(self,request):
        camp = Campaign.objects.all()
        serializer = CamapaignDetailSerializer(camp, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CamapaignDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CamapaignStoryApi(APIView):  #not working ...asking fo goal_amount
    def get(self,request):
        camp = Campaign.objects.all()
        serializer = CampaignStorySerailaizer(camp,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CampaignStorySerailaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CamapaignAccountDetailApi(APIView):
    def get(self,request):
        camp = CamapaignAccountSerializer.objects.all()
        serializer = CKBSerializer(camp,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CamapaignAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CampaignDetailStoryApi(APIView):
    def get(self, request):
        camp = Campaign.objects.all()
        serializer = CampaignDetailStorySerializer(camp,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CampaignDetailStorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CamapaignKYCApi(APIView):
    def get(self, request):
        camp = CampaignKycBenificiary.objects.all()
        serializer = CamapaignKYCSerializer(camp, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CamapaignKYCSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CampaignCreateApi1(APIView):
    def get(self, request):
        camp = Campaign.objects.all()
        serializer = CamapaignCreateSerializer(camp, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CamapaignCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import Q, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import timedelta

# working
class RelegiousEducationCampApi(APIView):    
    def get(self, request):
        params = request.GET
        page_number = int(params.get("pg", 1))
        page_size = int(params.get("limit", 2))
        offset = (page_number - 1) * page_size
        limit = page_size

        campaigns = Campaign.objects.annotate(cause_fund_raised=F('fund_raised'))

        # Filter by zakat=true
        zakat_filter = params.get("zakat_eligible")
        if zakat_filter and zakat_filter.lower() == 'True':
            campaigns = campaigns.filter(zakat_eligible=True)

        # Filter by user_type=NGO
        user_type_filter = params.get("user_type")
        if user_type_filter and user_type_filter.lower() == 'ngo':
            campaigns = campaigns.filter(user__user_type='NGO')
        
        # #Filter by location
        location_filters = params.get("location")
        # if location_filter:
        #     campaigns = campaigns.filter(Q(location__icontains=location_filter))
            
        if location_filters:
            locations = [location.strip() for location in location_filters.split(',')]
            query = Q()
            for location in locations:
                query |= Q(location__icontains=location)
            
            campaigns = campaigns.filter(query)

        # if expiring_soon:
        #     ten_days_ago = timezone.now() - timedelta(days=10)
        #     queryset = queryset.filter(end_date__gte=ten_days_ago)


        # Add filter for campaigns where 90% goal amount is equal to or greater than fund raised
        queryset = queryset.annotate(
            goal_amount_90_percent=F('goal_amount') * 0.9,
            fund_raised_decimal=ExpressionWrapper(F('fund_raised'), output_field=DecimalField())
        ).filter(fund_raised_decimal__gte=F('goal_amount_90_percent'))


        paginated_campaigns = campaigns[offset:offset + limit]
        all_campaigns_data = []

        for c1 in paginated_campaigns:
            donors_per_campaign = Donor.objects.filter(campaign=c1)
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

            user_images = None
            if c1.user and hasattr(c1.user, 'user_images') and c1.user.user_images:
                user_images = c1.user.user_images.url

            api_data = {
                'id': c1.id,
                'logo':user_images,
                'title': c1.title,
                'description': c1.description,
                'fund_raised': c1.fund_raised,
                'days_left': days_left_message,
                'sum_of_donor': sum_amt,
                'num_donors': num_donors,
                'location': c1.location,
            }

            all_campaigns_data.append(api_data)

        return Response(all_campaigns_data, status=status.HTTP_200_OK)   
    



    


