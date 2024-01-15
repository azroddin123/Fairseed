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


#####################################################################################################
class LandingPageAPI(APIView):
    def get(self, request):
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

class GeneralSettingApi1(APIView):
    def get(self,request):
        general = GeneralSetting.objects.all()
        serializer = GSSerializer(general, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = GSSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KeywordsApi1(APIView):
    def post(self, request):
        serializer = KeywordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        keywords = Keyword.objects.all()
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)

class LimitApi1(APIView):
    #No need to restrict the data through backend, you have to change this code for now leave this api
    VALID_NUM_CAMPAIGNS_OPTIONS = [4, 8, 12, 24, 36, 48, 60]
    VALID_MAX_FILE_SIZE_OPTIONS = ['1 MB', '2 MB', '3 MB', '4 MB', '5 MB', '10 MB']

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'num_campaigns' in data and data['num_campaigns'] not in self.VALID_NUM_CAMPAIGNS_OPTIONS:
            return Response({'num_campaigns': ['Invalid value']}, status=status.HTTP_400_BAD_REQUEST)

        if 'max_file_size' in data and data['max_file_size'] not in self.VALID_MAX_FILE_SIZE_OPTIONS:
            return Response({'max_file_size': ['Invalid value']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LimitSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        keywords = Limit.objects.all()
        serializer = LimitSerializer(keywords, many=True)
        return Response(serializer.data)
    
############################################################################################################
