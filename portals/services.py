
import jwt
def generate_token(email):
    payload = {
        'id': id
    }
    token = jwt.encode(payload, "asdfghjkhgfdsasdrtyu765rewsazxcvbnjkio908765432wsxcdfrt", algorithm="HS256")
    return token