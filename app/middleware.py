# request: lets you access info like user IP address
# jsonify: used to return a proper JSON response if rejected
# wraps: a Python tool to preserve function metadata when wrapping a function
from flask import request, jsonify
from functools import wraps
from .limiter import FixedWindowRateLimiter

"""
Creating a system that can sit in front of API route and check if the user is 
under limit request limit. 
"""
def rate_limit(redis_client): 
    limiter = FixedWindowRateLimiter(redis_client)

    def decorator(f): 
        @wraps(f)
        def wrapper(*args, **kwargs):
          user_ip = request.remote_addr
          if limiter.is_allowed(user_ip): 
             return f(*args, **kwargs)
          else: 
             return jsonify({"error": "Too Many Requests"}), 429
        return wrapper
    
    return decorator
