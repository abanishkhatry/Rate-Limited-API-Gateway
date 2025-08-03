import time
from .base import BaseRateLimiter
import math
"""
In Token Bucket, you are initially given a bucket with certain requests (lets say 10). you can use 
those 10 requests instantly or over a certain time. After every specific time interval the bucket
gets refilled with a specific rate like, bucket gets filled by 1 request every 5 sec.

For this redis stores - How many tokens you have ?
                      - When you last refilled your bucket ?
"""

# inheriting BaseRateLimiter means you have to implement is_allowed(user_id)
class TokenBucketRateLimiter(BaseRateLimiter):

    # user can hold up to 10 tokens max. This means they can do 10 quick actions. 
    # we add back 1 token per second. 
    def __init__(self, redis_client, bucket_capacity=10, refill_rate=1):
        super().__init__(redis_client)
        self.bucket_capacity = bucket_capacity  # max tokens
        self.refill_rate = refill_rate          # tokens per second
    
    # checking if the user can do something right now based on how many tokens they have. 
    def is_allowed(self, user_id: str) -> bool:
        token_key = f"token_bucket:tokens:{user_id}"
        time_key = f"token_bucket:timestamp:{user_id}"

        current_time = time.time()

        token_count = self.redis.get(token_key)
        last_refill_time = self.redis.get(time_key)

        if token_count is None or last_refill_time is None:
            token_count = self.bucket_capacity
            last_refill_time = current_time
        else:
            token_count = float(token_count)
            last_refill_time = float(last_refill_time)

        time_passed = current_time - last_refill_time
        refill_tokens = math.floor(time_passed * self.refill_rate)
        token_count = min(self.bucket_capacity, token_count + refill_tokens)

        allowed = token_count >= 1
        if allowed:
            token_count -= 1
            self.redis.set(time_key, current_time)

        self.redis.set(token_key, token_count)
        return allowed

