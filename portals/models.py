from django.db import models
import uuid
# Create your models here.


class BaseModel(models.Model):
    id         = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    created_on = models.DateField(auto_now_add=True,editable=False)
    updated_on = models.DateField(auto_now=True)
 
    class Meta:
        abstract = True
        ordering = ("-created_on",)

from django.db.models import Q

class SearchFilter:

    def filter_queryset(self, queryset, filter_data):
        """
        Filters the queryset based on the provided JSON filter data.

        Args:
            queryset: The queryset to be filtered.
            filter_data: A dictionary containing filter criteria.

        Returns:
            The filtered queryset.
        """
        q = Q()
        for field, filters in filter_data.items():
            for operator, value in filters.items():
                q = q & self.apply_filter(field, operator, value)
        return queryset.filter(q)


    def apply_filter(self, field, operator, value):
        """
        Applies a specific filter based on the operator.

        Args:
            field: The field name to filter on.
            operator: The comparison operator (e.g., "eq", "lt", "gt").
            value: The value to compare with the field.

        Returns:
            A Q object representing the filter criteria.
        """
        operators = {
            "eq": Q(**{field: value}),
            "lt": Q(**{field + "__lt": value}),
            "gt": Q(**{field + "__gt": value}),
            # Add more operators as needed (e.g., "contains", "in")
        }
        return operators.get(operator, None)  # Raise an error for unsupported operators

# import json
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import YourModel  # Replace with your actual model
# class SearchAPIView(APIView):
#     filter_class = SearchFilter

#     def get(self, request):
#         filter_data = request.GET.get('search', None)
#         if not filter_data:
#             return Response({'error': 'Missing filter data'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             filter_data = json.loads(filter_data)
#             print("filter_data")
#         except json.JSONDecodeError:
#             return Response({'error': 'Invalid JSON filter data'}, status=status.HTTP_400_BAD_REQUEST)

#         queryset = YourModel.objects.all()
#         filtered_queryset = self.filter_class.filter_queryset(queryset, filter_data)
#         serializer = YourModelSerializer(filtered_queryset, many=True)
#         return Response(serializer.data)