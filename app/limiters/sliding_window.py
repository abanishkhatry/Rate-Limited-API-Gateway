import time
from .base import BaseRateLimiter

"""
Sliding window limiter, checks requests based on last seconds rather than bucket of 60 sec. 
if you make first req at 12.02 and remaining at 12.30, 12.32, 12.36 and 12.38 thats the 60 mark window
starting from 12.02. So at 13.03 you could make only one more request as 12.02 is passed the 60 secs. 
So for this , the 60 sec window size starts at 12.30. So, you can make next request at 13.31. 

"""
class SlidingWindowRateLimiter(BaseRateLimiter):
    def __init__(self, redis_client, max_requests=5, window_size=60):
        super().__init__(redis_client)
        self.max_requests = max_requests
        self.window_size = window_size

    def is_allowed(self, user_id: str) -> bool:
        current_time = int(time.time())
        key = f"rate_limit:sliding:{user_id}"

        # Step 1: Remove old timestamps (older than window_size)
        self.redis.zremrangebyscore(key, 0, current_time - self.window_size)

        # Step 2: Count how many valid timestamps are left
        request_count = self.redis.zcard(key)

        if request_count < self.max_requests:
            # Step 3: Add the current request timestamp
            self.redis.zadd(key, {str(current_time): current_time})
            # Step 4: Set expiration (optional safety)
            self.redis.expire(key, self.window_size)
            return True
        else:
            return False
