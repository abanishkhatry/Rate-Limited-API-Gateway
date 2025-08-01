import time 
from .base import BaseRateLimiter

"""
class to track and enforce limits. 
In fixed window, you are given a window of 60 secs (lets say), then you will can do 5 requests at 
time during that timeframe. It resets after 60s passes, and again gives you another 60 sec window
where you could make 5 requests.

"""
class FixedWindowRateLimiter(BaseRateLimiter): 
    # constructor 
    def __init__(self, redis_client, max_requests=5, window_size=60): 
        super().__init__(redis_client) 
        self.max_requests = max_requests
        # meaning 1-minute window
        self.window_size = window_size
    # abstract function. 
    def is_allowed(self, user_id: str) -> bool: 
        # Here we are creating a bucket for every minute, where we limit the user with max 5 request that minute. 
        current_window = int(time.time()) // self.window_size 
        # So all request within the same minute will share the same key like rate_limit:192.168.1.5:31576812
        key = f"rate_limit:{user_id}:{current_window}"    
        # get the user's key and check if there is a bucket for this user in this time window
        count = self.redis.get(key) 
        # This means that's the user's first request, so we have to create a new bucket and add 1 token in it.
        if count is None: 
            self.redis.set(key, 1, ex=self.window_size)
            # this lets request go through. They’re under the limit.
            return True
        # This means that the user already has a bucket and they are under limit, so add it and increase the token count. 
        elif int(count) < self.max_requests: 
            self.redis.incr(key)
            return True 
        # This means the bucket is already full. 
        else: return False










