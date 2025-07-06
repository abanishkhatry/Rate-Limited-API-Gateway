import logging

"""
helps to know the route accessed, who accessed it, which limiter was used
, was it allowed or blocked.
"""

def setup_logger():
    # giving name to our logger
    logger = logging.getLogger("RateLimiterLogger")
    # sets how chatty/informative our logger should be
    logger.setLevel(logging.DEBUG)

    # setting a format for the logger on how the logs should look when printed.
    formatter = logging.Formatter(
        # currentTime, seriousness of message, actual message, currentTime's format. 
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    # a handler that decides where logs will go/ where it should print it.
    # By default, it prints on the terminal.  
    console_handler = logging.StreamHandler()

    # sets the previous defined format for displaying the msg. 
    console_handler.setFormatter(formatter)
    # connecting logger and handler, so that logger knows how to display logs 
    # and where to send them. 
    logger.addHandler(console_handler)

    return logger

# calls the function and creates the logger object as soon as the file is imported. 
logger = setup_logger()
