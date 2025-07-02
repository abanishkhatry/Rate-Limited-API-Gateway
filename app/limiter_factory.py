import os 
from limiters.fixed_window import FixedWindowRateLimiter
from limiters.sliding_window import SlidingWindowRateLimiter
from limiters.token_bucket import TokenBucketRateLimiter
from rate_limit_config import rate_limit_config


def get_limiter_for_route(route, redis_client) : 
    config = rate_limit_config.get(route)
    if not config: 
        raise ValueError(f"No rate limiting config found for route: {route}")
    
    algo = config["algo"]
    params = config["params"]

    if algo == "sliding_window": 
        return SlidingWindowRateLimiter(redis_client, **params)
    
    elif algo == "token_bucket" : 
        return TokenBucketRateLimiter(redis_client,**params)
    elif algo == "fixed_window": 
        return FixedWindowRateLimiter(redis_client, **params)
    
    else:
        raise ValueError(f"Unsupported algorithm type: {algo}")
