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
    create_serializer_class = DonorSerializer
    lookup_field = "id"

    # def get(self,request,pk=None,*args, **kwargs):
    #     print(request.data)
    #     if pk == str(0) or pk is None :
    #         amount = request.data.get('amount',50)
    #         mobile_no = "841204546"
            
    #         if request.data["payment_type"] == "UPI" :
    #             pay(request,1200,841204546)
                
            # serializer = DonorSerializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     return Response(status=status.HTTP_200_OK)
            # return Response(status=status.HTTP_400_BAD_REQUEST)

class BankTransactionApi(GenericMethodsMixin,APIView):
    model = BankTransaction
    serializer_class =BankTransactionSerializer
    lookup_field = "id"

class UpiTransactionApi(GenericMethodsMixin,APIView):
    model = UpiTransaction
    serializer_class = UpiSerializers
    lookup_field = "id"


# class DonationApi(APIView):
import jsons
import base64
import requests
import shortuuid
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from cryptography.hazmat.primitives import hashes
from django.views.decorators.csrf import csrf_exempt
from cryptography.hazmat.backends import default_backend
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
########################## HELPER FUNCTION ################################
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def calculate_sha256_string(input_string):
    # Create a hash object using the SHA-256 algorithm
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Update hash with the encoded string
    sha256.update(input_string.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return sha256.finalize().hex()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def base64_encode(input_dict):
    # Convert the dictionary to a JSON string
    json_data = jsons.dumps(input_dict)
    # Encode the JSON string to bytes
    data_bytes = json_data.encode('utf-8')
    # Perform Base64 encoding and return the result as a string
    return base64.b64encode(data_bytes).decode('utf-8')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
########################## Create your views here. ########################
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def index(request):
    return render(request, "index.html", { 'output': "Please Pay & Repond From The Payment Gateway Will Come In This Section", 'main_request': "" })


class PayApi(APIView):
    def get(self,request):
        print(request.data)
        print("in pay method")
        MAINPAYLOAD = {
            "merchantId": "PGTESTPAYUAT",
            "merchantTransactionId": shortuuid.uuid(),
            "merchantUserId": "MUID123",
            "amount":100,
            "redirectUrl": "http://127.0.0.1:8000/phonepay/return-to-me/",
            "redirectMode": "POST",
            "callbackUrl": "http://127.0.0.1:8000/phonepay/return-to-me/",
            "mobileNumber": 9876543210,
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # SETTING
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        INDEX = "1"
        ENDPOINT = "/pg/v1/pay"
        SALTKEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        base64String = base64_encode(MAINPAYLOAD)
        mainString = base64String + ENDPOINT + SALTKEY;
        sha256Val = calculate_sha256_string(mainString)
        checkSum = sha256Val + '###' + INDEX;
        # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # # Payload Send
        # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checkSum,
            'accept': 'application/json',
        }
        json_data = {
            'request': base64String,
        }
        response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
        responseData = response.json();
        return redirect(responseData['data']['instrumentResponse']['redirectInfo']['url'])


@csrf_exempt
def payment_return(request):
    print("in payment return ")
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SETTING
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    INDEX = "1"
    SALTKEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Access form data in a POST request
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_data = request.POST
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Convert form data to a dictionary
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_data_dict = dict(form_data)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    transaction_id = form_data.get('transactionId', None)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 1.In the live please match the amount you get byamount you send also so that hacker can't pass static value.
    # 2.Don't take Marchent ID directly validate it with yoir Marchent ID
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if transaction_id:
        request_url = 'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT/' + transaction_id;
        sha256_Pay_load_String = '/pg/v1/status/PGTESTPAYUAT/' + transaction_id + SALTKEY;
        sha256_val = calculate_sha256_string(sha256_Pay_load_String);
        checksum = sha256_val + '###' + INDEX;
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Payload Send
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
            'X-MERCHANT-ID': transaction_id,
            'accept': 'application/json',
        }
        response = requests.get(request_url, headers=headers)
        print("--------------")
        #page_respond_data=form_data_dict, page_respond_data_varify=response.text
    # return render(request, 'index.html', { 'output': response.text, 'main_request': form_data_dict  })
    return Response({"error" : False, "message" : "Data Uploaded Successfully" , "output" : response.text})