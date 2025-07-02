rate_limit_config = {
    
    "/login" : {
        "algo": "fixed_window", 
        "params": {
            "max_requests": 5, 
            "window_size": 60
        }
    } , 

    "/search": {
        "algo": 'token_bucket', 
        "params": {
            "bucket_capacity": 20, 
            "refill_rate": 2
        }
    } , 

    "/chat": {
        "algo": "sliding_window", 
        "params": {
            "max_requests": 10, 
            "window_size": 60
        }
    }
}