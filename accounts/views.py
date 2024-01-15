import random

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from portals.GM1 import GenericMethodsMixin
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from .models import *
from .serializers import *


class UserApi(GenericMethodsMixin, APIView):
    model = User
    serializer_class = UserSerializer1
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer1(user)
        return Response(serializer.data)

class RegisterUserApi(APIView):
    def post(self,request,*args, **kwargs):
        try : 
            serializer = UserSerializer(data=request.data)
            if  serializer.is_valid():
                serializer.save()
                return Response({"message" : "User Created Succefully" , "data" : serializer.data},status=status.HTTP_201_CREATED)
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

##################################################################################################################
from django.conf import settings
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime
from .email import send_otp_via_email

class RegisterOTPApi(APIView):
    def post(self, request):
        try:
            data= request.data
            serializer = UserOTPSerializer(data= data)
            if serializer.is_valid():
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': 'Registration successfully done..',
                    'data': serializer.data,
                })
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'data': str(e),
            })

class VerifyOTPApi(APIView):
    def post(self, request):
        try:
            user = User.objects.filter(email=request.data["email"]).first()
            print(type(user.otp))
            print(type(request.data['otp']))
            if user == None:
                return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': 'invalid email'
            })
            print(request.data["otp"])
            if user.otp != int(request.data["otp"]):
                return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': 'wrong otp'
            })
            user.is_verified = True
            user.save()
            return Response({
                'status': 200,
                'message': 'Email Verification is done successfully...',
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 500,
                'message': 'Internal Server Error',
                'data': str(e),
            })

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = User.objects.filter(username=username, password=password).first()
        if user:
            return Response({
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class EmailSMTP(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmailSMTPSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            # recipient = serializer.validated_data['recipient']
            recipients = list(User.objects.values_list('email', flat=True))
            try:
                for recipient_email in recipients:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [recipient_email],
                        fail_silently=False,
                    )
                return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': f'Error sending email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterApi(APIView):
    
    def get(self, request):
        u1 = User.objects.all()
        serializer = UserSerializer1(u1, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'Registration successful.',
                'data': serializer.data,
            })
        return Response({
            'status': 400,
            'message': 'Registration failed.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # u2 = User.objects.get(pk=pk)
        u2 = User.objects.filter(pk=pk).first()
        serializer = UserSerializer1(u2, data=request.data, partial=True)


        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': 'User information updated successfully.',
                'data': serializer.data,
            })
        return Response({
            'status': 400,
            'message': 'Update failed.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LatestMembers(APIView):
    def get(self, request):
        latest_members = User.objects.order_by('-created_on')[:4]
        serializer = LatestMembersSerializer(latest_members, many=True)
        
        formatted_members = []
        
        for member in serializer.data:
            created_on_str = member['created_on']
            created_on = parse_datetime(created_on_str)

            if created_on:
                member['created_on'] = created_on.strftime('%b %d, %Y')

            if 'user_images' not in member:
                member['user_images'] = []

            formatted_members.append(member)

        return Response(formatted_members)
##################################################################################################################