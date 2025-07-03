# rate_limit_config.py

RATE_LIMIT_CONFIG = {
    "/get-data": {
        "free": {"type": "sliding", "requests": 5, "window": 60},
        "premium": {"type": "token", "requests": 20, "window": 60},
        "admin": {"type": "token", "requests": 100, "window": 60}
    },
    "/login": {
        "free": {"type": "fixed", "requests": 3, "window": 60},
        "premium": {"type": "fixed", "requests": 10, "window": 60},
        "admin": {"type": "fixed", "requests": 30, "window": 60}
    },
    "/search": {
        "free": {"type": "sliding", "requests": 10, "window": 60},
        "premium": {"type": "token", "requests": 50, "window": 60},
        "admin": {"type": "token", "requests": 200, "window": 60}
    },
    "/chat": {
        "free": {"type": "sliding", "requests": 8, "window": 60},
        "premium": {"type": "token", "requests": 30, "window": 60},
        "admin": {"type": "token", "requests": 100, "window": 60}
    }
}
