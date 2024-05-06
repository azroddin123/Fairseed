
import jwt
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives

def generate_token(email):
    payload = {
        "email" :email
    }
    token = jwt.encode(payload, "asdfghjkhgfdsasdrtyu765rewsazxcvbnjkio908765432wsxcdfrt", algorithm="HS256")
    return token


def my_mail(mail, otp):
    subject = "Fairseed Password Reset OTP"
    msg = "Your one time password for resetting the password at <strong>Fairseed</strong> is as follows: <strong>{}</strong> <br>\nPlease do not share this with anyone.".format(otp)
    # Create an EmailMultiAlternatives object to support HTML content
    email = EmailMultiAlternatives(subject, msg, '33azharoddin@gmail.com', [mail])
    email.attach_alternative(msg, "text/html")  # Specify HTML content type
    
    try:
        res = email.send()
        if res == 1:
            msg = 1
        else:
            print("no")
            msg = 0
    except Exception as e:
        print(e)
        msg = 0
    
    return msg

def campaign_creation_updation(mail,status,title,subject,msg):
    # subject = "Fairseed Campaign Creation Mail"
    # message = "Your Campaign is created and request is send for approval to admin"+title+"this is title"
    print(mail,status,title,subject,msg,"------------------------")
    email = EmailMultiAlternatives(subject, msg, '33azharoddin@gmail.com', [mail])
    email.attach_alternative(msg, "text/html")  # Specify HTML content type
    try:
        res = email.send()
        if res == 1:
            msg = 1
        else:
            print("no")
            msg = 0
    except Exception as e:
        print(e)
        msg = 0
    
    return msg




def donation_email(mail,campaign,amount):
    subject = "Fairseed Campaign "
    msg = "Your one time password for resetting the password at <strong>Fairseed</strong> is as follows: <strong>{}</strong> <br>\nPlease do not share this with anyone.".format(amount)
    # Create an EmailMultiAlternatives object to support HTML content
    email = EmailMultiAlternatives(subject, msg, '33azharoddin@gmail.com', [mail])
    email.attach_alternative(msg, "text/html")  # Specify HTML content type
    
    try:
        res = email.send()
        if res == 1:
            msg = 1
        else:
            print("no")
            msg = 0
    except Exception as e:
        print(e)
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
    
def paginate_data(model, serializer, request,data):
    try:
        limit = max(int(request.GET.get('limit', 1)), 1)
        page_number = max(int(request.GET.get('page', 1)), 1)
        data = data
        paginator = Paginator(data, limit)
        print(page_number,limit,"------------------------")
        try:
            current_page_data = paginator.get_page(page_number)
        except EmptyPage:
            print("--------------in emapty page ")
            return Response({"error": True, "message": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            print(serializer,"-----------------serializer------------")
            serialized_data = serializer(current_page_data, many=True).data
            print(serialized_data,"-----------------serializer------------")
        except Exception as e:
            print(" in exception ")
            return Response({"error": True, "message": f"Serialization error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
            "error": False,
            "pages_count": paginator.num_pages,
            "count": paginator.count,
            "rows": serialized_data
        }
        return response_data
    except Exception as e:
        return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

# def paginate_data(model, serializer, request, data):
#     try:
#         limit = max(int(request.GET.get('limit', 10)), 1)  # Default limit is 10 if not provided or invalid
#         page_number = max(int(request.GET.get('page', 1)), 1)
#         print(page_number,limit)
#         paginator = Paginator(data, limit)
#         current_page_data = paginator.get_page(page_number)
#         serialized_data = serializer(current_page_data, many=True).data
#         response_data = {
#             "error": False,
#             "pages_count": paginator.num_pages,
#             "count": paginator.count,
#             "rows": serialized_data
#         }
#         return response_data
#     except Exception as e:
#         return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    
