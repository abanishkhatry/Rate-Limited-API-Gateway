"""
abc = Abstract Base Classes module in Python
ABC: A special base class that means “I am an interface — I define rules but not behavior”
abstractmethod: Says “You must implement this method in your subclass”
"""

"""
Why Using Redis ? 
Since we are building an API gateway that needs to:

Track how many requests each user (or IP) is making
Reset that tracking after a certain time (e.g., 60 seconds)
Make this logic super fast
Work for hundreds or thousands of users at the same time

Redis does this for us. Redis is a 
 - A very fast key-value database
 - Lives in memory (like RAM), not on disk — so it’s super quick
 - Can auto-delete keys after a timeout (TTL)
 - Can increment values, store lists, sort by time, etc.

"""
from abc import ABC, abstractmethod 


# Acts as a template/interface
class BaseRateLimiter(ABC):
    # injecting the Redis client into every subclass
    # **kwargs = allows you to pass other optional configs (e.g., max_requests, window_size, etc.)
    def __init__(self, redis_client, **kwargs):
        self.redis = redis_client

    @abstractmethod # this suggests, this method should be filled by whoever inherits this class.
    def is_allowed(self, user_id: str) -> bool:
        pass    