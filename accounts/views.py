from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from fairseed.GM import GenericMethodsMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404

class UserApi(GenericMethodsMixin,APIView):
    model = User
    serializer_class = UserSerializer1
    lookup_field = "id"

class RegisterUserApi(APIView):
    def post(self,request,*args, **kwargs):
        try : 
            serializer = UserSerializer(data=request.data)
            if  serializer.is_valid():
                serializer.save()
                return Response({"message" : "User Created Succefully"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            raise ValidationError({
                "status_code" : status.HTTP_400_BAD_REQUEST,
                "message" :  e
            })

class ChangePasswordApi(APIView):
    def post(self,request,*args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data,context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Password updated successfully"},status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassIdApi(APIView):
    def get(self,request,id1,id2,id3):
        print(id1,id2,id3)
        
        id_data = {
            "id1" : id1,
            "id2" : id2,
            "id3" : id3
        }

        serializers = IDSerializer(data=id_data)
        if serializers.is_valid() :
            return Response(data=serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    

################### MY CODE ########################
    

class RegisterUserListAPI(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer1(user, many=True)
        return Response(serializer.data)

class RegisterUserAPI(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User,pk=pk)
        serializer = UserSerializer1(user)
        return Response(serializer.data)
    
class RegisterPostAPI(APIView):
    def post(self, request):
        serializer = UserSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serializer = UserSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

class RegisterDeleteApi(APIView):
    def get(self, request, pk):
        u1 = get_object_or_404(User, pk=pk)
        serializer = UserSerializer1(u1)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"message": "User deleted successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"})

        
    
    
    
