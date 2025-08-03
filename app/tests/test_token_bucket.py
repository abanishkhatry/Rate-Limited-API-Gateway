import time
import pytest
import redis
from dotenv import load_dotenv
import os
from limiters.token_bucket import TokenBucketRateLimiter

load_dotenv()

@pytest.fixture
def redis_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

# setting up the Token Bucket Rate Limiter with following rules. 
@pytest.fixture
def limiter(redis_client):
    # Allow 5 requests per 10 seconds
    return TokenBucketRateLimiter(redis_client, bucket_capacity=5, refill_rate=0.5)  # 0.5 tokens/sec = 5 tokens per 10s

# testing if user can make requests while under limit of allowed request. 
def test_under_limit_allows_requests(limiter):
    user_id = "user1"

    # We reset Redis to delete any old token data for this user.
    limiter.redis.delete(user_id)

    # Make 3 requests (under the limit of 5)
    assert limiter.is_allowed(user_id) is True
    assert limiter.is_allowed(user_id) is True
    assert limiter.is_allowed(user_id) is True

# this test checks what happens when a user exceeds their rate limit.
def test_over_limit_blocks_requests(limiter):
    user_id = "user2"
    limiter.redis.delete(user_id)  # clear tokens before test, to start fresh

    # Let's say bucket has capacity=5 and fill_rate=1/s
    # Use all 5 tokens quickly
    for _ in range(5):
        assert limiter.is_allowed(user_id) is True

    # Now the 6th request should be not allowed because no tokens left
    assert limiter.is_allowed(user_id) is False

# test that verifies after tokens run out, they get refilled over time, allowing new requests again. 
def test_token_refill_allows_future_requests(limiter):
    user_id = "user3"
    limiter.redis.delete(f"token_bucket:tokens:{user_id}")
    limiter.redis.delete(f"token_bucket:timestamp:{user_id}")

    # Use all 5 tokens
    for _ in range(5):
        assert limiter.is_allowed(user_id) is True

    assert limiter.is_allowed(user_id) is False  # Should fail now

    # Wait until 2 tokens refill, with timeout
    allowed_count = 0
    start = time.time()
    while allowed_count < 2 and (time.time() - start) < 5:
        if limiter.is_allowed(user_id):
            allowed_count += 1
        else:
            time.sleep(0.2)

    assert allowed_count == 2, f"Expected 2 allowed requests after refill, got {allowed_count}"



