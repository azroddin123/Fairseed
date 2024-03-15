from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from portals.services import generate_token,my_mail
from django.contrib.auth.hashers import check_password
from random import randint
from django.core.mail import send_mail


class UserRolesAPi(GenericMethodsMixin,APIView):
    model = UserRole
    serializer_class = UserRoleSerializer
    lookup_field = "id"


class UserApi(GenericMethodsMixin,APIView):
    model = User
    serializer_class = UserSerializer1
    lookup_field = "id"
    
class RegisterUserApi(APIView):
    def post(self,request,*args, **kwargs):
        try : 
            serializer = UserSerializer(data=request.data)
            
            if  serializer.is_valid():
                user = serializer.save()
                print(user.id)
                token = generate_token(user.email)
                return Response({"message" : "User Created Succefully" , "data" : UserSerializer1(user).data , "token" : token},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(APIView):
    def post(self,request,*args, **kwargs):
        
        try : 
            email       = request.data.get('email')
            password    = request.data.get('password')
            # Generate Token
            user = User.objects.filter(email=email).first()
            if user is None : 
             return Response({"error" : False,"data" : "User Not Exists"},status=status.HTTP_404_NOT_FOUND)
            token = generate_token(user.email)
            # password_match = check_password(password,user.password)
            password_match = check_password(password,user.password)
            print("password match",password_match)
            serializer = UserSerializer1(user)
            data = {"error" : False, "message": "User logged in successfully","user_info": serializer.data,"token" : token}
            if password == user.password  or password_match:
                print("password matched")
                return Response(data,status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error" : True, "message" : "Something Went Wrong"},status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordApi(APIView):
    def post(self,request,*args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data,context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Password updated successfully"},status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPI(APIView):
    def post(self,request,*args, **kwargs):
        try :
            mail = request.data.get('email')
            print("in user",mail)
            user = User.objects.get(email=mail)
            print(user)
            otp = randint(1000,9999)
            res = my_mail(mail,otp)
            if (res ==1):
                return Response(data={'Success':'Otp Mail sent succesfully to '+ mail,'OTP':str(otp)},status=status.HTTP_200_OK)
            else:
                return Response(data = 'Error sending mail',status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": True,"message" : "User Email Does not exists"},status=status.HTTP_400_BAD_REQUEST )

class UpdateUserAPI(APIView):
    def put(self,request,*args, **kwargs):
        try :
            user = User.objects.get(id=request.thisUser)
            serializer = UserSerializer1(user, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"error" : False, "message": "User updated successfully",},status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


    
class ResetPasswordAPI(APIView):
    def post(self,request,*args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return Response(data={'Success':'Password for Email ' +str(user) +' reset succesfull'},status=status.HTTP_200_OK)
        return Response(data = {'Error':'Email does not exists'})


class PageNotFoundAPI(APIView):
    def get(self,request,*args, **kwargs):
        return Response({"error" : True, "message" : "This API Does not exists in this Application"},status=status.HTTP_404_NOT_FOUND)


# Email Sending Scenarios 
    
# 1.Forget Password
# 2.After Donation
# Assuming you have already imported the User model
# users = User.objects.values('country')
# print(users)


# adhar pan , pan card image ,adhar card image
# for item in users :
#     print(item)
    
# # Query to get country-wise user count
# country_user_count = User.objects.values('country').annotate(user_count=Count('id'))

# # Print the results
# for item in country_user_count:
#     print("Country:", item['country'], "User Count:", item['user_count'])