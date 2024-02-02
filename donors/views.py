from django.shortcuts import render,get_object_or_404
from django.db.models import Sum
from accounts.models import User

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


############# MY CODE ##############
        
class DonorDetailApi(APIView):
    def get(self, request, pk):
        # donor = Donor.objects.all()
        donor = get_object_or_404(Donor, pk=pk)
        serializer = DonorSerializer(donor)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DonorDonationApi:
    def get(self, request):
        donor = Donor.objects.all()
    

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
    
class DonationsAPApi(APIView):
    def get(self,request):
        ongoing_campaign = Donor.objects.all()
        serializer = DonorSerializer2(ongoing_campaign, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        serializer = DonorSerializer2(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = Donor.objects.all()

        full_name = serializer.validated_data.get('full_name')
        amount = serializer.validated_data.get('amount')
        email = serializer.validated_data.get('email')
        city = serializer.validated_data.get('city')
        fund_raised = serializer.validated_data.get('fund_raised')
        id = serializer.validated_data.get('id')
        country = serializer.validated_data.get('country')

        # Explicitly define each filter condition
        if full_name:
            queryset = queryset.filter(full_name__icontains=full_name)
        if amount:
            queryset = queryset.filter(amount__icontains=amount)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if city:
            queryset = queryset.filter(city__icontains=city)
        if fund_raised:
            queryset = queryset.filter(fund_raised__icontains=fund_raised)
        if id:
            queryset = queryset.filter(id__icontains=id)
        if country:
            queryset = queryset.filter(country__icontains=country)


        serializer = DonorSerializer2(queryset, many=True)

        return Response(serializer.data)
    
class DashboardDonationsApi(APIView):
    def get(self,request):
        donor= Donor.objects.all()
        serializer = DashboardDonorSerializer(donor, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DashboardDonorSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardDonationsViewApi(APIView):
    def get(self,request):
        donor= Donor.objects.all()
        serializer = DashboardDonorSerializer1(donor, many = True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
class MyDonationApi(APIView):
    def get(self, request, user_id):
        user_donations = Donor.objects.filter(campaign__user_id=user_id)
        serializer = MyDonationSerializer(user_donations, many=True)
        return Response(serializer.data)
    





    




    