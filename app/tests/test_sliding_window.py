import pytest 
import redis 
import time 
import os
from dotenv import load_dotenv
from limiters.sliding_window import SlidingWindowRateLimiter

load_dotenv()

# loading the Redis
@pytest.fixture
def redis_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

# setting up the Token Bucket Rate Limiter with following rules. 
@pytest.fixture
def sliding_limiter(redis_client):
    # Allow 5 requests per 10 seconds
    return SlidingWindowRateLimiter(redis_client, max_requests=5, window_size=10)

# Test that checks if user is allowed to make more requests while being under the limit
def test_under_limit_allows_requests(sliding_limiter): 
    user_id = "test_user_sw1"
    sliding_limiter.redis.delete(user_id)

    for _ in range(5): 
        allowed = sliding_limiter.is_allowed(user_id)
        assert allowed is True

# Test that checks if the user is blocked to make the extra requests if max request has already reached. 
def test_over_limit_blocks_request(sliding_limiter):
    user_id = "test_user_sw2"
    sliding_limiter.redis.delete(user_id)

    # Make 5 allowed requests
    for _ in range(5):
        allowed = sliding_limiter.is_allowed(user_id)
        assert allowed is True

    # 6th request within the same window should be blocked
    assert sliding_limiter.is_allowed(user_id) is False


# checking if user is allowed to make new request once the first request slips out of the sliding window limiter. 
def test_expired_timestamps_allow_new_requests(sliding_limiter):
    user_id = "test_user_sw3"
    sliding_limiter.redis.delete(user_id)

    # Fill the window with max requests
    for _ in range(5):
        assert sliding_limiter.is_allowed(user_id) is True

    # 6th request should be blocked immediately
    assert sliding_limiter.is_allowed(user_id) is False

    # Wait for the window to expire (window_size = 10s)
    time.sleep(11)

    # Old timestamps should now be expired — request should be allowed again
    assert sliding_limiter.is_allowed(user_id) is True


# checking if user is allowed to make spaced out requests within the time window. 
def test_evenly_spaced_requests_within_limit(sliding_limiter):
    user_id = "test_user_sw4"
    sliding_limiter.redis.delete(user_id)

    for i in range(5):
        allowed = sliding_limiter.is_allowed(user_id)
        assert allowed is True, f"Request {i+1} unexpectedly blocked"
        time.sleep(2)  # Wait 2 seconds between requests

    # 6th request will go *just* past 10-second window start → should be allowed
    # Optional check:
    # assert sliding_limiter.is_allowed(user_id) is True
