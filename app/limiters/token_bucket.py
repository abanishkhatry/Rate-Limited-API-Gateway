import time
from .base import BaseRateLimiter

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
        # stores how many tokens they have left. 
        token_key = f"token_bucket:tokens:{user_id}"
        # stores when we last added tokens
        time_key = f"token_bucket:timestamp:{user_id}"
        
        current_time = time.time()

        # Step 1: Get last known values from Redis
        token_count = self.redis.get(token_key)
        last_refill_time = self.redis.get(time_key)

        # Step 2: Parse values or initialize
        # for first time user, filling their values. 
        if token_count is None or last_refill_time is None:
            token_count = self.bucket_capacity
            last_refill_time = current_time
        else:
            token_count = float(token_count)
            last_refill_time = float(last_refill_time)

        # Step 3: Calculate tokens to refill
        # checking how long it has been since they have refilled
        time_passed = current_time - last_refill_time
        # getting number of tokens to refill.
        refill_tokens = time_passed * self.refill_rate
        # updating the token count
        token_count = min(self.bucket_capacity, token_count + refill_tokens)

        # if they have atleast one token, letting them through, else not and updating their time. 
        if token_count >= 1:
            token_count -= 1
            self.redis.set(token_key, token_count)
            self.redis.set(time_key, current_time)
            return True
        else:
            self.redis.set(token_key, token_count)
            self.redis.set(time_key, current_time)
            return False
