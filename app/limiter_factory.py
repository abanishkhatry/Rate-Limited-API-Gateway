import os 
from limiters.fixed_window import FixedWindowRateLimiter
from limiters.sliding_window import SlidingWindowRateLimiter
from limiters.token_bucket import TokenBucketRateLimiter
from rate_limit_config import  RATE_LIMIT_CONFIG


def get_limiter_for_route(route, redis_client, role) : 
    
    if route not in RATE_LIMIT_CONFIG: 
        raise ValueError(f"No rate limiting config found for route: {route}")
    
    role_config = RATE_LIMIT_CONFIG[route].get(role)

    if not role_config: 
        raise ValueError(f"No config for role '{role} on route {route}")
    
    algo_type = role_config["type"]
    limit = role_config["requests"]
    window = role_config["window"]

    if algo_type == "sliding": 
        return SlidingWindowRateLimiter(redis_client, limit, window)
    
    elif algo_type == "token" : 
        return TokenBucketRateLimiter(redis_client,limit, window)
    elif algo_type == "fixed": 
        return FixedWindowRateLimiter(redis_client, limit, window)
    
    else:
        raise ValueError(f"Unsupported algorithm type: {algo_type}")
