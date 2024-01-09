from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from portals.GM2 import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from portals.services import generate_token
from django.contrib.auth.hashers import check_password


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
                return Response({"message" : "User Created Succefully" , "data" : serializer.data , "token" : token},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({"error" : True , "message" : str(e)},status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self,request,*args, **kwargs):
            email       = request.data.get('email')
            password    = request.data.get('password')
            # Generate Token
            user = User.objects.filter(email=email).first()
            print
            if user is None : 
             return Response({"error" : False,"data" : "User Not Exists"},status=status.HTTP_404_NOT_FOUND)
            token = generate_token(user.email)
            print(token)
            print(password,user.password)
            print(type(password),type(user.password))
            # password_match = check_password(password,user.password)
            password_match = check_password(password,user.password)
            print("password match",password_match)
            serializer = UserSerializer(user)
            data = {"error" : True, "message": "User logged in successfully","user_info": serializer.data,"token" : token}
            if password == user.password  or password_match:
                return Response(data,status=status.HTTP_200_OK)
            else :
               return Response({"error" : True, "message" : "Something Went Wrong"},status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordApi(APIView):
    def post(self,request,*args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data,context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Password updated successfully"},status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


