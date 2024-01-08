from django.forms import IntegerField
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, F, Case, When,IntegerField
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
from django.core.paginator import Paginator

# Create your views here.

##############################################################################################################################################
class TotalCountAPI(APIView):
    def get(self,request):
        # getting all Campaign values
        c_r = Campaign.objects.all().count()
        serializer = CampaignSerializer(c_r,many=True)
        
        # Total funds raised
        funds_raised_total = Campaign.objects.annotate(total_fund_raised=Sum("fund_raised"))
        total_fund_raised = funds_raised_total.aggregate(sum_fund=Sum('total_fund_raised'))['sum_fund']
        
        # total donors
        total_donors = Donor.objects.all().count()

        # Successful campaigns
        # successful_campaigns_total = Campaign.objects.filter(is_successful=True).aggregate(successful_campaigns=Count("id"))
        # total_successful_campaigns = Campaign.objects.aggregate(successful_campaigns=Sum("is_successful", output_field=IntegerField()))['successful_campaigns']
        
#         successful_campaigns_total = Campaign.objects.aggregate(successful_campaigns=Sum(
#         Case(
#             When(is_successful=True, then=1),
#             default=0,
#             output_field=IntegerField()
#         )
#     )
# )

        # total_successful_campaigns = successful_campaigns_total.get('successful_campaigns', 0)

        serializer_data = {
            'Causes Raised' : c_r,
            'Funds Raised': total_fund_raised,
            'Total donors' :total_donors,
            # 'Successful campaigns' :total_successful_campaigns,
        }
        return Response(serializer_data)
    
    ###################
    # def get(self,request):
        
    # number_of_causes = Campaign.objects.all().count()






# class PracticeAPI(APIView):
#     def get(self, request):
#         c1 = Campaign.objects.all()
#         serializers = CampaignSerializer(c1, many =True)
#         goal = [{'Goal amount' : c2['goal_amount'],
#                 'Title' : c2['title']} for c2 in serializers.data]
#         return Response(goal)
########################################################################################################################

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
    
###############################################################################################################################################


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