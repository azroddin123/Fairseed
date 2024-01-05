from django.shortcuts import render

# Create your views here.
from .serializers import * 
from .models import (
    Donor,
    BankTransaction,
    UpiTransaction
)
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework import status
from rest_framework.response import Response


# class DonorApi(GenericMethodsMixin,APIView):
#     model = Donor
#     serializer_class = DonorSerializer
#     lookup_field = "id"

#     def post(self,request,pk=None,*args, **kwargs):
#         if pk == str(0) or pk is None :
#             print("in api")
#             # amount = request.data["amount"]
#             # obj = Campaign.objects.get(pk=request.data["campaign"])
#             # required_amount = obj.goal_amount - obj.fund_raised
#             # if amount > required_amount :
#             #     return Response({"error" : False,"message" : "You can make donation for this campaign upto "+str(required_amount)+" Rs"},status=status.HTTP_200_OK)     
#             # # obj.fund_raised 
#             serializer = DonorSerializer(data=request.data)
#             if serializer.is_valid():
#                 # obj.fund_raised = obj.fund_raised + request.data["amount"]
#                 # obj.save()
#                 serializer.save()
#                 return Response({ "error" : False,"data" : serializer.data}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"error" : True , "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class DonorApi(GenericMethodsMixin,APIView):
    model = Donor
    serializer_class = DonorSerializer
    lookup_field = "id"

    def post(self,request,pk=None,*args, **kwargs):
        if pk == str(0) or pk is None :
            
            serializer = DonorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BankTransactionApi(GenericMethodsMixin,APIView):
    model = BankTransaction
    serializer_class =BankTransactionSerializer
    lookup_field = "id"

class UpiTransactionApi(GenericMethodsMixin,APIView):
    model = UpiTransaction
    serializer_class = UpiSerializers
    lookup_field = "id"


# Remove Cause
    