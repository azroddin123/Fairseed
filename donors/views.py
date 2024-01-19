from django.shortcuts import render

# Create your views here.
from .serializers import * 
from .models import (
    Donor,
    BankTransaction,
    UpiTransaction
)
from rest_framework.views import APIView
from portals.GM1 import GenericMethodsMixin
from rest_framework import status
from rest_framework.response import Response

###################################################################################
class DonorRecord(APIView):
    def get(self, request):
        donors_record = Donor.objects.all()
        serializers = DonorSerializer1(donors_record, many = True)
        return Response(serializers.data, status=status.HTTP_200_OK)
###################################################################################

class DonorApi(GenericMethodsMixin,APIView):
    model = Donor
    serializer_class = DonorSerializer
    lookup_field = "id"

    def post(self,request,pk=None,*args, **kwargs):
        if pk == str(0) or pk == None :
            print("in api")
            amount = request.data["amount"]
            obj = Campaign.objects.get(pk=request.data["campaign"])
            required_amount = obj.goal_amount - obj.fund_raised
            if amount > required_amount :
                return Response({"error" : False,"message" : "You can make donation for this campaign upto "+str(required_amount)+" Rs"},status=status.HTTP_200_OK)     
            # obj.fund_raised 
            serializer = DonorSerializer(data=request.data)
            # here i have to update the campaign model also 
            if serializer.is_valid():
                obj.fund_raised = obj.fund_raised + request.data["amount"]
                obj.save()
                serializer.save()
                return Response({ "error" : False,"data" : serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error" : True , "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#**************************************************************************************************************************************************************************#
class DonorApi(GenericMethodsMixin,APIView):
    model = Donor
    serializer_class = DonorSerializer
    lookup_field = "id"

    def post(self,request,pk=None,*args, **kwargs):
        if pk == str(0) or pk == None :
            
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

#################################################################################################################################################    
from payment_gateways.serializers import BankTransferSerializer1
from payment_gateways.models import BankTransfer

#**********************************************************************************************************************************************#
class DonateToCampaign(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DonateToCampaignSerializer(data=request.data)
        if serializer.is_valid():
            campaign_id = serializer.validated_data['campaign'].id
            amount = serializer.validated_data['amount']
            campaign = Campaign.objects.get(id=campaign_id)
            if amount > campaign.goal_amount:
                error_message = f"Donation amount cannot exceed more than {campaign.goal_amount}"
                raise serializers.ValidationError(error_message)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#**********************************************************************************************************************************************#
class DonateToBankTransfer(APIView):
    def get(self, request, *args, **kwargs):
        bank_transfers = BankTransfer.objects.all()
        serializer = BankTransferSerializer1(bank_transfers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#**********************************************************************************************************************************************#
class BankTransaction1(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DonorBankTransactionSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            serialized_data = DonorBankTransactionSerializer(instance).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################################################################################################################################################
