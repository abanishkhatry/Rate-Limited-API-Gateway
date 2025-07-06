# request: lets you access info like user IP address, URL, headers
# jsonify: used to return a proper JSON response 
# wraps: a Python tool to preserve function metadata when wrapping a function
from flask import request, jsonify
from functools import wraps
# picks the correct limiter algorith based on route and user role
from limiter_factory import get_limiter_for_route
# reads the JWT token and tells us who the user is and what their role is. 
from auth import decode_token 
# Imports your professional logger so you can log when users are allowed or blocked
from logger import logger


"""
Creating a system that can sit in front of API route and check if the user is 
under limit request limit. 
"""
def config_aware_rate_limiter(redis_client): 
    # decorator function that will wrap around each function
    def decorator(f): 
        # keeps the original name and docstring of the wrapped function 
        # This is like saying: "Even if I wrap you in something else, I still remember who you are."
        @wraps(f)
        # function where rate limiting logic lives. 
        def wrapper(*args, **kwargs):
          # gets the route the user is trying to access
          route = request.path
          # decoding user's JWT token to access their user_id and role. 
          token_payload = decode_token()
          # if no token 
          if token_payload is None : 
             logger.warning(f"Unauthorized access attempt to {route}")
             return jsonify({"error": "Unauthorized – valid token required"}), 401
          # extracting valid user_id and role
          user_id = token_payload.get("user_id")
          role = token_payload.get("role")

          try: 
             # asks limiter_factory to build the right limiter, based on route, redis instance and user's role. 
             limiter = get_limiter_for_route(route, redis_client,role)
             # checking if the user is under or over limit. 
             allowed  = limiter.is_allowed(user_id)
             logger.info(
                f"User{user_id} (role: {role} accessing {route})"
                f"with {type(limiter).__name__} : {'Allowed' if allowed else 'Blocked'}"
             )
             if not allowed: 
                return jsonify({"error": "Too Many Requests"}), 429
             
          except ValueError as e: 
             logger.error(f"Limiter error on route {route}: {str(e)}")
             return jsonify({"error": str(e)}), 500
          
          return f(*args, **kwargs)
        
        return wrapper
    # this wraps everything up and returns the fully baked decorator back to main.py
    return decorator
