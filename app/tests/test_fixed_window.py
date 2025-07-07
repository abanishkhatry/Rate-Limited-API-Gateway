import pytest
import redis
import time
import os
from dotenv import load_dotenv
from limiters.fixed_window import FixedWindowRateLimiter

load_dotenv()

@pytest.fixture
def redis_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

@pytest.fixture
def fixed_limiter(redis_client):
    # Allow 5 requests every 10 seconds
    return FixedWindowRateLimiter(redis_client, max_requests=5, window_size=10)

# checking if the user can make request while being under limit 
def test_allows_requests_under_limit(fixed_limiter):
    user_id = "test_user_fw1"
    fixed_limiter.redis.delete(user_id)

    for i in range(5):
        allowed = fixed_limiter.is_allowed(user_id)
        assert allowed is True, f"Request {i+1} unexpectedly blocked"

# checking if user gets blocked while making a new request once already out of limits
def test_blocks_requests_over_limit(fixed_limiter):
    user_id = "test_user_fw2"
    fixed_limiter.redis.flushdb()
    for _ in range(5):
        assert fixed_limiter.is_allowed(user_id) is True
    assert fixed_limiter.is_allowed(user_id) is False

# checking if user can add a request after fixed window is reset. 
def test_allows_new_window_requests(fixed_limiter):
    user_id = "test_user_fw3"
    fixed_limiter.redis.flushdb()
    for _ in range(5):
        assert fixed_limiter.is_allowed(user_id) is True
    assert fixed_limiter.is_allowed(user_id) is False
    time.sleep(11)  # wait for next window (window_size=10s)
    assert fixed_limiter.is_allowed(user_id) is True        

