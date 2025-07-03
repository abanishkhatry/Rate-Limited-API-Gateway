# jwt helps us create and read secret message tokens. 
import jwt
import datetime
# request: lets us see what a user sent us. 
# jsonify: helps us send data back to the user in a clean JSON format.
from flask import request, jsonify
# lets us read secret info from the environment
import os
# we're trying to get a secret password(key) from your environment, if not 
# found we use "super-secret-key"
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")

# making new token (digital passport) for a user
# user_id = who the user is , like their name or ID
# role = free or premium 
def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        # this token will stop working after 1 hour
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    # using payload, signing it with our secret link and making it use a 
    # recipe called "HS256". This whole will then generate a super long string. 
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

# this function checks who the person is when they show us a passport/token in their request.
def decode_token():
    # finding the token in user's request, that's hidden inside a special envelope 
    # called the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None

    try:
        # received auth_header is like Authorization: Bearer abc123tokenhere
        # so token is the second one, i.e. [1]
        token = auth_header.split(" ")[1]
        # opening the token/passport using the same secret ink and recipe
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        # returning a python dict, with user_id, role , and exp
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
