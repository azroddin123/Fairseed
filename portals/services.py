
import jwt
from django.core.mail import send_mail
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


def paginated_data():
    pass