# app/main.py
from flask import Flask, jsonify, request
import redis
import os
from dotenv import load_dotenv
from middleware import config_aware_rate_limiter
from auth import generate_token

load_dotenv()

"""
Step 1 - You open Postman or your browser and hit: http://localhost:5000/get-data
Step 2 - Flask receives the request and sees @rate_limit(redis_client)
Step 3 - Middleware checks who is making request, has they hit the max number of allowed requests in this minute
Step 4 - If under limit, runs the get_data function and prints {"message": "Here is your data!"}
         else, gives {"error": "Too Many Requests"}. 
"""

def create_app():
    # creating an instance of app in the Flask factory pattern
    app = Flask(__name__)
    # This initializes Redis connection
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )
    rate_limit_decorator = config_aware_rate_limiter(redis_client)

    print(f"[Limiter] Using: {type(rate_limit_decorator).__name__}")

    # Now when a user hits this endpoint, the request first goes through the rate limiter
    @app.route("/get-data")
    @rate_limit_decorator
    # If the limiter says “OK” → it runs get_data() and returns data
    def get_data():
        return jsonify({"message": "Here is your data!"})
    # You return the Flask app so it can be used by a WSGI server or other context

    # Now when a user hits this endpoint, the request first goes through the rate limiter
    @app.route("/login")
    @rate_limit_decorator
    # If the limiter says “OK” → it makes login successful
    def login():
        return jsonify({"message": "Login successful!"})
    # You return the Flask app so it can be used by a WSGI server or other context

    @app.route("/search")
    @rate_limit_decorator
    # If the limiter says “OK” → it gives back what were searched
    def search():
        return jsonify({"message": "Here are your search results"})
    # You return the Flask app so it can be used by a WSGI server or other context

    @app.route("/chat")
    @rate_limit_decorator
    # If the limiter says “OK” → it returns all the chats
    def chat():
        return jsonify({"message": "Chat loaded!"})

    @app.route("/auth/token" , methods = ["POST"])
    def issue_token(): 
        """
        This is a FAKE login endpoint to issue a JWT.
        Send JSON like: { "user_id": "user123", "role": "free" }
        """
        data = request.get_json()
        token = generate_token(data["user_id"] , data["role"])
        return jsonify({"token" : token})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
