from django.db.models import Sum
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from portals.GM2 import GenericMethodsMixin

from .models import *
from .serializers import *


class PagesAPi(APIView):
    model = Pages
    serializer_class = PageSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser]


class GeneralSettingApi(GenericMethodsMixin,APIView):
    model = GeneralSetting
    serializer_class = GSSerializer
    lookup_field = "id"


class KeywordSApi(GenericMethodsMixin,APIView):
    model = Keyword
    serializer_class = KeywordSerializer
    lookup_field = "id"


class LimitApi(GenericMethodsMixin,APIView):
    model = Limit
    serializer_class = LimitSerializer
    lookup_field = "id"


class SocialProfileApi(GenericMethodsMixin,APIView):
    model = SocialProfile
    serializer_class = SocialProfileSerializer
    lookup_field = "id"


class LandingPageSettingApi(GenericMethodsMixin,APIView):
    model = LandingPage
    serializer_class = LandingPageSerializer
    lookup_field = "id"


####################################################################################################################################################################################
    
from django.shortcuts import get_object_or_404

#***************************************************************************************************************************************************************#

#Admin Panel --> Landing PAge

class LandingPageAPI(APIView):
    def get(self, request):
        print("v")
        landing_pages = LandingPage.objects.all()

        if not landing_pages:
            return Response({"error": "No data"}, status=status.HTTP_404_NOT_FOUND)

        image_data_list = []
        for landing_page in landing_pages:
            image_data = {
                'logo': request.build_absolute_uri(landing_page.logo.url) if landing_page.logo else None,
                'logo_footer': request.build_absolute_uri(landing_page.logo_footer.url) if landing_page.logo_footer else None,
                'favicon': request.build_absolute_uri(landing_page.favicon.url) if landing_page.favicon else None,
                'image_header': request.build_absolute_uri(landing_page.image_header.url) if landing_page.image_header else None,
                'image_bottom': request.build_absolute_uri(landing_page.image_bottom.url) if landing_page.image_bottom else None,
                'avtar': request.build_absolute_uri(landing_page.avtar.url) if landing_page.avtar else None,
                'image_category': request.build_absolute_uri(landing_page.image_category.url) if landing_page.image_category else None,
            }
            image_data_list.append(image_data)
        return Response(image_data_list, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = LandingPageSerializer1(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#***************************************************************************************************************************************************************#
    
#Admin Panel --> General Settings
    
class GeneralSettingApi1(APIView):
    def get(self, request):
        general = GeneralSetting.objects.all()
        serializer = GSSerializer(general, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = GSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        general = get_object_or_404(GeneralSetting, id=pk)
        serializer = GSSerializer(general, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Admin Panel -- > Keyword(FK) --> General setting
class KeywordsApi1(APIView):
    def post(self, request):
        serializer = KeywordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        keywords = Keyword.objects.all()
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        keyword = get_object_or_404(Keyword, id=pk)
        keyword.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#***************************************************************************************************************************************************************#

#Admin Panel --> General Settings --> Limit
    
class LimitApi1(APIView):
    def get(self, request):
        limits = Limit.objects.all()
        serializer = LimitSerializer1(limits, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = LimitSerializer1(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        limit = get_object_or_404(Limit, id=pk)
        serializer = LimitSerializer1(limit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#***************************************************************************************************************************************************************#

#Admin Panel --> General Settings --> Social Profiles
    
class SocialProfile1(APIView):
    def get(self, request):
        social_profile = SocialProfile.objects.all().delete()
        serializer = SocialProfileSerializer(social_profile, many = True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = SocialProfileSerializer(data=request.data)

        if serializer.is_valid():
            SocialProfile.objects.all().delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def put(self, request, pk):
        sp = get_object_or_404(SocialProfile, id=pk)
        serializer = SocialProfileSerializer(sp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
######################################################################################################################################################################################
