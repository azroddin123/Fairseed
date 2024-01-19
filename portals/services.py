
import jwt
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
def generate_token(email):
    payload = {
        "email" :email
    }
    token = jwt.encode(payload, "asdfghjkhgfdsasdrtyu765rewsazxcvbnjkio908765432wsxcdfrt", algorithm="HS256")
    return token



# Forget Password API
def my_mail(mail,otp):  
        subject = "One Time Password for Fairseed  password reset"  
        msg     = "Your one time password for resetting the password at Fairseed  is as follows : "+str(otp)+"\nPlease do not share this with anyone."  
        res     = send_mail(subject, msg,'33azharoddin@gmail.com', [mail],fail_silently=False)  
        if(res == 1):  
            msg = 1  
        else:  
            print("no")
            msg = 0
        return msg  

from django.core.paginator import Paginator, EmptyPage

def paginate_model_data(model, serializer, request, filter_key=None):
    try:
        limit = max(int(request.GET.get('limit', 0)), 1)
        page_number = max(int(request.GET.get('page', 0)), 1)
        if filter_key:
            filter_value = request.GET.get(filter_key)
            data = model.objects.filter(**{filter_key: filter_value})
        else:
            data = model.objects.all()

        paginator = Paginator(data, limit)
        try:
            current_page_data = paginator.get_page(page_number)
        except EmptyPage:
             return Response({"error": True, "message": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized_data = serializer(current_page_data, many=True).data
        response_data = {
            "error": False,
            "pages_count": paginator.num_pages,
            "count": paginator.count,
            "rows": serialized_data
        }
        return response_data
    except Exception as e:
        return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# def paginate_model_data(model, serializer, request, filter_key=None):
    try:
        limit = int(request.GET.get('limit', 1))
        page_number = int(request.GET.get('page', 1))

        if filter_key:
            filter_value = request.GET.get(filter_key)
            data = model.objects.filter(**{filter_key: filter_value})
        else:
            data = model.objects.all()

        paginator = Paginator(data, limit)

        try:
            current_page_data = paginator.get_page(page_number)
        except EmptyPage:
            return Response({"error": True, "message": "Page not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serialized_data = serializer(current_page_data, many=True).data
        except Exception as e:
            return Response({"error": True, "message": f"Serialization error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = {
            "error": False,
            "pages_count": paginator.num_pages,
            "count": paginator.count,
            "rows": serialized_data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)