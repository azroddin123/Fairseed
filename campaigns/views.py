from django.shortcuts import render
from django.db.models import Sum
from donors.models import Donor
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
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

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
    create_serializer_class = CampaignSerializer
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
# class CampaignBycategoryApi(APIView):  
#     def get(self, request, pk, *args, **kwargs):
#             try:
#                 data = Campaigncategory.objects.get(id=pk)
#                 serializer = CampaignBycategorySerializer(data)
#                 return Response({"error": False, "data": serializer.data}, status=status.HTTP_200_OK)
#             except Campaigncategory.DoesNotExist:
#                 return Response({"error": "Campaigncategory not found"}, status=status.HTTP_404_NOT_FOUND)
#             except Exception as e:
#                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReportedCauseApi(APIView):
    def get(self,request,*args, **kwargs) :
        try :
            data = Campaign.objects.filter(is_reported=True)
            serializer = CampaignSerializer1(data,many=True)
            return Response({"error": False, "data" : serializer.data },status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e) },status=status.HTTP_400_BAD_REQUEST)

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
                "count": paginator.count,
                "error": False,
                "data": serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CampaignDetailsApi(APIView):
    def get(self,request,pk,*args, **kwargs): 
        try :       
            data = Campaign.objects.get(pk=pk)
            serializer = CampaignDetailSerializer(data)
            return Response({"error": False, "data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Get Campaign Details if its individual and if all campaigns
# class CampaignDetailsApi(GenericMethodsMixin,APIView):
#     model = Campaign
#     serializer_class = CampaignSerializer
#     lookup_field  = "id"
   
#     def get(self,request,pk=None,*args, **kwargs):
#             if pk is None or pk == str(0) :
#                 try : 
#                     limit = request.GET.get('limit')
#                     data = Campaign.objects.all()
#                     page_number = request.GET.get('page')
#                     print(page_number,limit,type(limit),type(page_number))
#                     if page_number == None or limit == None:
#                         serializer = CampaignAdminSerializer(data,many=True)
#                         return Response({"error": False,"data": serializer.data}, status=status.HTTP_200_OK)
#                     pages = int(math.ceil(len(data)/int(limit)))
#                     paginator = Paginator(data, limit)
#                     data = paginator.get_page(page_number)
#                     serializer = CampaignAdminSerializer(data, many=True)
#                     return Response({"error": False, "pages_count": pages, "total_records" : paginator.count,"data": serializer.data}, status=status.HTTP_200_OK)
#                 except Campaign.DoesNotExist:
#                     return Response({"error" : "Record not found or exists"},status=status.HTTP_400_BAD_REQUEST)
#             else :
#                 data = Campaign.objects.get(pk=pk)
#                 serializer = CampaignDetailSerializer(data)
#                 return Response({"error": False, "data" : serializer.data},status=status.HTTP_200_OK)


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
            return Response({"error" : False,"data" : serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : str(e)},status=status.HTTP_400_BAD_REQUEST)
        




























   
 
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