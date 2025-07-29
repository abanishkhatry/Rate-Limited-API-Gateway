# 1. Use Python base image
FROM python:3.10-slim

# 2. Set working directory in the container
WORKDIR /app

# 3. Copy requirements.txt first to leverage Docker cache.
COPY requirements.txt .

# 4. Install Python dependencies (Like Flask, Redis, etc)
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the app into the container
COPY . .

# 5. Setting up environment variables 
# telling flask where the entry point is
ENV FLASK_APP=app/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5050

# 6. Expose port
EXPOSE 5050

# 7. Run the Flask app
CMD ["flask", "run"]

