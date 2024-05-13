from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from accounts.models import *
from accounts.serializers import *
from campaigns.models import * 

# def search():

print("azaht")
model_name = User
search_param = "azhar"
print("in search")
model_class = globals()[model_name]
fields = [field.name for field in model_class._meta.get_fields()]
print("azhar")
for item in fields:
    print(fields)
q_objects = Q()
for field in fields:
    q_objects |= Q(**{f"{field}__icontains": search_param})
    
queryset = model_class.objects.filter(q_objects)
record_count = queryset.count()
serializer = UserAdminSerializer(queryset, many=True)
print(serializer.data)


# search()
# class SearchFilterAPI(APIView):
#     def get(self, request):
#         model_name = request.GET.get('model')
#         search_param = request.GET.get('search')

#         # Dynamically get the model class
#         model_class = globals()[model_name]

#         # Get all fields of the model
#         fields = [field.name for field in model_class._meta.get_fields()]

#         q_objects = Q()
#         for field in fields:
#             q_objects |= Q(**{f"{field}__icontains": search_param})

#         # Filter the queryset based on search_param and fields
#         queryset = model_class.objects.filter(q_objects)
#         record_count = queryset.count()
#         serializer = ArtistAdminSerializer(queryset, many=True)

#         # Return the response
#         return JsonResponse({
#             'record_count': record_count,
#             "data": serializer.data,
#         })
