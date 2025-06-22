# app/main.py

from flask import Flask, jsonify
import redis
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

    @app.route("/get-data")
    def get_data():
        return jsonify({"message": "Here is your data!"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
