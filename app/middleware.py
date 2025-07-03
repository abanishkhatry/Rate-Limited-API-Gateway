# request: lets you access info like user IP address
# jsonify: used to return a proper JSON response if rejected
# wraps: a Python tool to preserve function metadata when wrapping a function
from flask import request, jsonify
from functools import wraps
from limiter_factory import get_limiter_for_route
from auth import decode_token 

"""
Creating a system that can sit in front of API route and check if the user is 
under limit request limit. 
"""
def config_aware_rate_limiter(redis_client): 
    def decorator(f): 
        @wraps(f)
        def wrapper(*args, **kwargs):
          route = request.path
          token_payload = decode_token()

          if token_payload is None : 
             return jsonify({"error": "Unauthorized – valid token required"}), 401
          
          user_id = token_payload.get("user_id")
          role = token_payload.get("role")
          try: 
             limiter = get_limiter_for_route(route, redis_client,role)
             if not limiter.is_allowed(user_id): 
                return jsonify({"error": "Too Many Requests"}), 429
             
          except ValueError as e: 
             return jsonify({"error": str(e)}), 500
          
          return f(*args, **kwargs)
        
        return wrapper
    
    return decorator
