import datetime
import math
import uuid
from datetime import timedelta

from django.core.paginator import Paginator
from django.db.models import F, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.utils.timezone import localtime
from rest_framework import status
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response
from rest_framework.views import APIView

from donors.models import Donor
from portals.GM1 import GenericMethodsMixin

from .models import Campaign, Campaigncategory, CampaignKycBenificiary
from .serializers import *

# Create your views here.

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
    
##############################################################################################################################################
from datetime import datetime

from django.db.models import F, Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework.parsers import FileUploadParser

from accounts.models import User


#******************************************************************************#
class CampaignCategory1(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CampaignCategorySerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        category = Campaigncategory.objects.all()
        serializer = CampaignCategorySerializer1(category, many = True)
        return Response(serializer.data)
    
class CampaignDetailsApi1(APIView):
    def get(self, request):
        campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(campaigns, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
#******************************************************************************#
class CardAPIViewPagination(APIView):
   
    def get(self, request):
       
        params = request.GET
        page_number = int(params.get("pg", 1))
        page_size = int(params.get("limit", 8))
        offset = (page_number - 1) * page_size
        limit = page_size

        campaigns = Campaign.objects.annotate(cause_fund_raised=F('fund_raised'))

        paginated_campaigns = campaigns[offset:offset + limit]

        all_campaigns_data = []

        for c1 in paginated_campaigns:
            donors_per_campaign = Donor.objects.filter(campaign=c1)
            num_donors = donors_per_campaign.count()
            # sum_amt = donors_per_campaign.aggregate(sum_amt=Sum('amount'))['sum_amt'] if donors_per_campaign.exists() else 0
           
            today_date = timezone.now().date()
            if c1.end_date:
                days_remaining = (c1.end_date - today_date).days
                if days_remaining >= 0:
                    days_left_message = f'{days_remaining} days left'
                else:
                    days_left_message = 'Campaign ended'
            else:
                days_left_message = 'No end date'

            user_data = {
                'username': c1.user.username,
            }

            user_images = None
            if c1.user and hasattr(c1.user, 'user_images') and c1.user.user_images:
                user_images = c1.user.user_images.url

            campaign_image_url = c1.campaign_image.url if c1.campaign_image else None

            api_data = {
                'campaign image': campaign_image_url,
                'logo':user_images,
                'user': user_data,
                'title': c1.title,
                'fund_raised': c1.fund_raised,
                "goal_amount": c1.goal_amount,
                'num_donors': num_donors,
                'days_left': days_left_message,
                'location': c1.location,
            }

            all_campaigns_data.append(api_data)

        return Response(all_campaigns_data, status=status.HTTP_200_OK)

#******************************************************************************#
class CardAPIView2(APIView):
    def get(self, request, pk):
        campaign = get_object_or_404(Campaign, id=pk)
        # formatted_date_time = campaign.created_on.strftime('%b %d, %Y %I:%M %p')
        user = campaign.user

        user_data = {
            'username': user.username,
        }

        user_images = None
        if user and hasattr(user, 'user_images') and user.user_images:
            user_images = user.user_images.url

        num_donors = campaign.donors.count()

        today_date = timezone.now().date()
        days_left_message = None

        if campaign.end_date:
            days_remaining = (campaign.end_date - today_date).days
            if days_remaining >= 0:
                days_left_message = f'{days_remaining} days left'
            else:
                days_left_message = 'Campaign ended'
        else:
            days_left_message = 'No end date'
            
        c1 = campaign

        data = {
            'Status': 'Campaign Ongoing' if campaign.end_date and campaign.end_date >= timezone.now().date() else 'Campaign Ended',
            'Fund Raised': campaign.fund_raised,
            'Goal Amount': campaign.goal_amount,
            'Zakah Eligible': campaign.zakat_eligible,
            'logo': user_images,
            'user': user_data,
            'title': campaign.title,
            'num_donors': num_donors,
            'days_left': days_left_message,
            'location': c1.location,
            # 'Date Time': formatted_date_time,
        }

        return Response(data, status=status.HTTP_200_OK)

#******************************************************************************#
class RecentDonors(APIView):
    def get(self, request):
        campaigns = Campaign.objects.all().order_by('-created_on')
        all_donors = Donor.objects.filter(campaign__in=campaigns)
        serializer = DonorRecentSerializer(all_donors, many=True)
        return Response(serializer.data)

#******************************************************************************#
class RecentCampaigns(APIView):
    def get(self, request):
        recent_campaigns = Campaign.objects.all().order_by('-created_on')

        formatted_data = []
        for campaign in recent_campaigns:
            formatted_campaign = {
                'Images': campaign.campaign_image.url if campaign.campaign_image else None,
                'cause_title': campaign.title,
                'username': campaign.user.username,
                'created_on': campaign.created_on.strftime('%b %d, %Y')
            }
            formatted_data.append(formatted_campaign)

        return Response(formatted_data)

#******************************************************************************#
class CausesbyCategoryAPI(APIView):
    def get(self,request):
        causes_by_category = Campaign.objects.all()
        titles = [campaigns.title for campaigns in causes_by_category]
        return Response(titles, status=status.HTTP_200_OK)

#******************************************************************************#
class DashboardAPI(APIView):
    def get(self, request):
        total_donations = Donor.objects.all().count()
        total_fund_raised_all_campaigns = Campaign.objects.aggregate(total_fund_raised = Sum('fund_raised'))['total_fund_raised'] or 0
        number_of_causes = Campaign.objects.all().count()
        number_of_members = User.objects.all().count()
        serialized_data = {
            'Total Donation': total_donations,
            'Fund Raised' : total_fund_raised_all_campaigns,
            'Causes' : number_of_causes,
            'Members' : number_of_members,
        }
        return Response(serialized_data, status=status.HTTP_200_OK)
    
#******************************************************************************#
class CategoryAdminApi(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            category = get_object_or_404(Campaigncategory, id=pk)
            serializer = CampaignCategorySerializer1(category)
            return Response(serializer.data)
        else:
            categories = Campaigncategory.objects.all()
            serializer = CampaignCategorySerializer1(categories, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CampaignCategorySerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        category = get_object_or_404(Campaigncategory, id=pk)
        serializer = CampaignCategorySerializer1(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(Campaigncategory, id=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#******************************************************************************#
    
from django.contrib.auth.models import AnonymousUser

class CampaignAdminApi(APIView):
    def get(self, request, *args, **kwargs):
        search_query = self.request.query_params.get('search', None)
        reset_query = self.request.query_params.get('reset', None)
        sort_with = self.request.query_params.get('sort_with', None)
        sort_by = self.request.query_params.get('sort_by', None)
        campaigns = Campaign.objects.all()

        if reset_query:
            pass
        elif search_query:
            campaigns = campaigns.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(user__username__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(user__mobile_number__icontains=search_query) |
                Q(goal_amount__icontains=search_query) |
                Q(fund_raised__icontains=search_query) |
                Q(status__icontains=search_query) |
                Q(start_date__icontains=search_query) |
                Q(end_date__icontains=search_query)
            )
        if sort_with:
            if sort_with == 'Sort With':
                if sort_by == 'Lower to High':
                    campaigns = campaigns.order_by('id')
                elif sort_by == 'High to Low':
                    campaigns = campaigns.order_by('-id')
                else:
                    campaigns = campaigns.order_by('id')
            elif sort_with == 'Date':
                if sort_by in ['Ascending', 'Lower to High', 'A to Z']:
                    campaigns = campaigns.order_by('start_date')
                elif sort_by in ['Descending', 'High to Low', 'Z to A']:
                    campaigns = campaigns.order_by('-start_date')
            elif sort_with == 'Title':
                if sort_by in ['Ascending', 'Lower to High', 'A to Z']:
                    campaigns = campaigns.order_by('title')
                elif sort_by in ['Descending', 'High to Low', 'Z to A']:
                    campaigns = campaigns.order_by('-title')
            elif sort_with == 'User':
                if sort_by in ['Ascending', 'Lower to High', 'A to Z']:
                    campaigns = campaigns.order_by('user__username')
                elif sort_by in ['Descending', 'High to Low', 'Z to A']:
                    campaigns = campaigns.order_by('-user__username')
            elif sort_with == 'Status':
                if sort_by == 'Active':
                    campaigns = campaigns.filter(status='Active')
                elif sort_by == 'Pending':
                    campaigns = campaigns.filter(status='Pending')
                elif sort_by == 'Rejected':
                    campaigns = campaigns.filter(status='Rejected')
                elif sort_by == 'Completed':
                    campaigns = campaigns.filter(status='Completed')
                if sort_by in ['Ascending', 'Lower to High', 'A to Z']:
                    campaigns = campaigns.order_by('status')
                elif sort_by in ['Descending', 'High to Low', 'Z to A']:
                    campaigns = campaigns.order_by('-status')

        if sort_by == 'Sort By':
            campaigns = Campaign.objects.all()

        serializer = CampaignAdminSerializer1(campaigns, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        campaign = get_object_or_404(Campaign, id=pk)
        serializer = CampaignAdminSerializer2(campaign, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CampaignModificationsApi(APIView):
    def get(self, request, pk):
        campaign = get_object_or_404(Campaign, id=pk)
        modifications = campaign.modifications.all()
        serializer = CampaignModificationSerializer(modifications, many=True)
        return Response(serializer.data)

#******************************************************************************#
class CampaignEditApproval(APIView):
    
    def get(self, request):
        campaign_edit = Campaign.objects.all()

        formatted_data = []
        for campaign in campaign_edit:
            formatted_campaign = {
                'Id': campaign.id,
                'Campaign': campaign.title,
                'Changes Requested At': campaign.updated_on.strftime('%d-%m-%Y %H:%M:%S'),
                'Goal': campaign.goal_amount,
                'Campaign Created At': campaign.created_on.strftime('%d-%m-%Y %H:%M:%S'),
                'Deadline': campaign.end_date.strftime('%d-%m-%Y')
            }
            formatted_data.append(formatted_campaign)
        return Response(formatted_data)
    
    def put(self, request, pk):
        campaign_edit = get_object_or_404(Campaign, id=pk)
        serializer = CampaignEditSerializer(campaign_edit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#******************************************************************************#
class ScholarshipCAmpaigns(APIView):

        def get(self, request, *args, **kwargs):
            search_query = self.request.query_params.get('search', None)
            reset_query = self.request.query_params.get('reset', None)
            sort_with = self.request.query_params.get('sort_with', None)
            sort_by = self.request.query_params.get('sort_by', None)

            campaigns = Campaign.objects.all()

            if reset_query:
                pass

            if search_query:
                campaigns = campaigns.filter(
                    Q(title__icontains=search_query) |
                    Q(description__icontains=search_query) |
                    Q(user__username__icontains=search_query) |
                    Q(user__email__icontains=search_query) |
                    Q(user__mobile_number__icontains=search_query) |
                    Q(goal_amount__icontains=search_query) |
                    Q(fund_raised__icontains=search_query) |
                    Q(status__icontains=search_query) |
                    Q(start_date__icontains=search_query) |
                    Q(end_date__icontains=search_query)
                )

            if sort_with:
                if sort_with == 'Date':
                    campaigns = campaigns.order_by('start_date')
                elif sort_with == 'User':
                    campaigns = campaigns.order_by('user__username')
                elif sort_with == 'Title':
                    campaigns = campaigns.order_by('-title')
                elif sort_with == 'Status':
                    campaigns = campaigns.order_by('status')

            if sort_by:
                if sort_by == 'Lower to High':
                    campaigns = campaigns.order_by('goal_amount')
                elif sort_by == 'High to Low':
                    campaigns = campaigns.order_by('-goal_amount')

            scholarship_campaigns = campaigns.filter(category__name='Scholarship')
            counter = 1
            serializer = CampaignAdminSerializer1(scholarship_campaigns, many=True, context={'counter': counter})
            return Response(serializer.data)

#******************************************************************************#
class ReportedCampaigns(APIView):

    def get(self, request):
            reported_campaigns = Campaign.objects.filter(is_reported=True)
            formatted_data = []
            for index, campaign in enumerate(reported_campaigns, start=1):
                formatted_campaign = {
                    'Id': index,
                    'User': campaign.user.username,
                    'Campaign': campaign.title,
                    'Date': campaign.end_date.strftime('%b %d, %Y')
                }
                formatted_data.append(formatted_campaign)

            return Response(formatted_data)
    
    def put(self, request, pk):
        campaign_edit = get_object_or_404(Campaign, id=pk)
        serializer = CampaignEditSerializer(campaign_edit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        delete_reported_campaign = get_object_or_404(Campaign, id=pk)
        delete_reported_campaign.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#******************************************************************************#
class DonateToCampaignCard(APIView):

    def get(self, request, pk):
        campaign = get_object_or_404(Campaign, id=pk)
        # formatted_date_time = campaign.created_on.strftime('%b %d, %Y %I:%M %p')

        donor_count = campaign.donors.count()

        today_date = timezone.now().date()
        if campaign.end_date:
            days_remaining = (campaign.end_date - today_date).days
            if days_remaining >= 0:
                days_left_message = f'{days_remaining} days left'
            else:
                days_left_message = 'Campaign ended'
        else:
            days_left_message = 'No end date'

        data = {
            'Status': 'Campaign Ongoing' if campaign.end_date and campaign.end_date >= timezone.now().date() else 'Campaign Ended',
            'Fund Raised': campaign.fund_raised,
            'Goal Amount': campaign.goal_amount,
            'Zakah Eligible': campaign.zakat_eligible,
            'Title': campaign.title,
            'Summary': campaign.summary,
            'Total Donors': donor_count,
            'Days left': days_left_message,
            'Location': campaign.location,
        }

        return Response(data, status=status.HTTP_200_OK)
        
#******************************************************************************#
#Tags api remaining
    
class CampaignBycategory(APIView):
    def get(self, request):

        params = request.GET
        page_number = int(params.get("pg", 1))
        page_size = int(params.get("limit", 4))
        offset = (page_number - 1) * page_size
        limit = page_size

        campaigns = Campaign.objects.filter(is_successful=True).annotate(cause_fund_raised=F('fund_raised'))

        paginated_campaigns = campaigns[offset:offset + limit]

        all_campaigns_data = []

        for c1 in paginated_campaigns:
            donors_per_campaign = Donor.objects.filter(campaign=c1)
            num_donors = donors_per_campaign.count()
    
            today_date = timezone.now().date()
            if c1.end_date:
                days_remaining = (c1.end_date - today_date).days
                if days_remaining >= 0:
                    days_left_message = f'{days_remaining} days left'
                else:
                    days_left_message = 'Campaign ended'
            else:
                days_left_message = 'No end date'

            user_data = {
                'username': c1.user.username,
            }

            user_images = None
            if c1.user and hasattr(c1.user, 'user_images') and c1.user.user_images:
                user_images = c1.user.user_images.url

            campaign_image_url = c1.campaign_image.url if c1.campaign_image else None

            api_data = {
                'campaign image': campaign_image_url,
                'logo': user_images,
                'user': user_data,
                'title': c1.title,
                'fund_raised': c1.fund_raised,
                "goal_amount": c1.goal_amount,
                'num_donors': num_donors,
                'days_left': days_left_message,
                'location': c1.location,
            }

            all_campaigns_data.append(api_data)

        return Response(all_campaigns_data, status=status.HTTP_200_OK)
    
#******************************************************************************#
    
#working on this
    
# class WithdrawalCampaignView(APIView):
    # def get(self, request, pk=None):
    #     if pk is not None:
    #         campaign = Campaign.objects.filter(pk=pk).first()
    #         if not campaign:
    #             return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

    #         serializer = WithdrawalCampaignSerializer(campaign)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         campaigns = Campaign.objects.all()
    #         serializer = CampaignWithdrawalSerializer(campaigns, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

class WithdrawalCampaignView(APIView):
    def get(self, request):
        withdrawal_campaign = Campaign.objects.all()
        serializer = CampaignWithdrawalSerializer(withdrawal_campaign, many = True)
        return Response(serializer.data)
    
# class WithdrawalInsideView(APIView):
#     def get(self, request, pk):
#         try:
#             campaign = Campaign.objects.get(id=pk)
#         except Campaign.DoesNotExist:
#             return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = WithdrawalDetailsSerializer(campaign)

#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#******************************************************************************#
#working on this
# class CampaignKycBenificiaryAPI(APIView):
#     parser_classes = [FileUploadParser]

#     def get(self, request):
#         ckb = CampaignKycBenificiary.objects.all()
#         serializer = CombinedSerializer(ckb, many=True)
#         return Response(serializer.data)
    
#     def patch(self, request, *args, **kwargs):
#         u2 = get_object_or_404(CampaignKycBenificiary, id=kwargs.get('pk'))
#         serializer = CKBViewSerializer(u2, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###############################################################################################################################################
