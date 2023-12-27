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
from portals.GM1 import GenericMethodsMixin
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
    lookup_field  = "id"


class DocumentApi(GenericMethodsMixin,APIView):
    model = Documents
    serializer_class = DocumentSerializer
    lookup_field = "id"


class DashboardApi(APIView):
    def get(self,request,*args, **kwargs) :
        data = {
        "total_campaign" : Campaign.objects.count(),
        "total_donation" : 0,
        "donor_count" : Donor.objects.count(),
        "successfull_campaign" : Campaign.objects.filter(is_successfull=True).count(),
        "student_benifited" : Campaign.objects.filter(is_successfull=True).count()
        }
        print(data)
        serializer = DashboardSerializer(data=data)
        if serializer.is_valid():
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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

class CampaignByCategoryApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field  = "id"
    
    def get(self,request,pk=None,*args, **kwargs):
            if pk == None or pk == str(0) :
                try : 
                    cat_id = request.GET.get('catagory')
                    limit = request.GET.get('limit')
                    data = Campaign.objects.filter(category=cat_id)
                    page_number = request.GET.get('page')
                    print(page_number,limit,type(limit),type(page_number))
                    if page_number == None or limit == None:
                        serializer = CampaignAdminSerializer(data,many=True)
                        return Response({"error": False,"data": serializer.data}, status=status.HTTP_200_OK)
                    pages = int(math.ceil(len(data)/int(limit)))
                    paginator = Paginator(data, limit)
                    if int(request.GET.get('page')) > pages or request.GET.get('page') == str(0):
                        return Response({"error": False, "pages_count": pages ,"total_records" : len(data), "data": [], "msg": "data fetched Succefully"}, status=status.HTTP_200_OK)
                    # serializer = CampaignAdminSerializer(data,many=True)
                    else:
                        data = paginator.get_page(page_number)
                        serializer = CampaignAdminSerializer(data, many=True)
                        return Response({"error": False, "pages_count": pages, "total_records" : len(data),"data": serializer.data}, status=status.HTTP_200_OK)
                except Campaign.DoesNotExist:
                    return Response({"error" : "Record not found or exists"},status=status.HTTP_400_BAD_REQUEST)
            
            else :
                data = Campaign.objects.get(pk=pk)
                serializer = CampaignDetailSerializer(data)
                return Response({"error": False, "data" : serializer.data},status=status.HTTP_200_OK)
            
    
class CampaignDetailsApi(GenericMethodsMixin,APIView):
    model = Campaign
    serializer_class = CampaignSerializer
    lookup_field  = "id"
    
    def get(self,request,pk=None,*args, **kwargs):
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
                    # if int(request.GET.get('page')) > pages or request.GET.get('page') == str(0):
                    #     return Response({"error": False, "pages_count": pages ,"total_records" : len(data), "data": [], "msg": "data fetched Succefully"}, status=status.HTTP_200_OK)
                    # # serializer = CampaignAdminSerializer(data,many=True)
                    # else:
                    data = paginator.get_page(page_number)
                    serializer = CampaignAdminSerializer(data, many=True)
                    return Response({"error": False, "pages_count": pages, "total_records" : len(data),"data": serializer.data}, status=status.HTTP_200_OK)
                except Campaign.DoesNotExist:
                    return Response({"error" : "Record not found or exists"},status=status.HTTP_400_BAD_REQUEST)
            
            else :
                data = Campaign.objects.get(pk=pk)
                serializer = CampaignDetailSerializer(data)
                return Response({"error": False, "data" : serializer.data},status=status.HTTP_200_OK)
            
    



