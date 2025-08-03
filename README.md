
# 🚦 Rate-Limited API Gateway

![CI](https://github.com/abanishkhatry/Rate-Limited-API-Gateway/actions/workflows/ci.yml/badge.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue?logo=docker)
![Python](https://img.shields.io/badge/python-3.10-blue.svg)

A scalable, Dockerized Flask API Gateway that enforces intelligent **rate-limiting** using three industry-standard algorithms:  
- ⏲️ Fixed Window  
- 🧮 Sliding Window  
- 🪣 Token Bucket  

Backed by **Redis** for high-performance storage and **JWT-based authentication** for user-level request control. The project includes Swagger UI documentation, CI/CD via GitHub Actions, and a robust test suite with `pytest`.

---

## 📌 Features

- 🔐 **Secure JWT Authentication** via `/auth/token`
- 🧠 **Smart Request Limiting** per user using Redis-backed:
  - Fixed Window (e.g., 5 req/min)
  - Sliding Window (real-time lookback)
  - Token Bucket (refillable action burst)
- ⚙️ **Configurable Rate Limiter Middleware** with central `rate_limit_config.py`
- 🧪 **Unit Testing** with `pytest`
- 📦 **CI/CD Pipeline** using GitHub Actions with Redis service runner
- 🐳 **Dockerized App** with Redis via `docker-compose`
- 📄 **Interactive API Docs** powered by **Flasgger** (Swagger UI)

---

## 🛠️ Tech Stack

| Layer        | Stack                        |
|--------------|------------------------------|
| Backend API  | Flask                        |
| Rate Limiting| Redis + Custom Algorithms    |
| Auth         | JWT                          |
| Docs         | Flasgger (Swagger UI)        |
| Testing      | Pytest                       |
| CI/CD        | GitHub Actions               |
| Deployment   | Docker + Docker Compose      |

---

## 📂 Project Structure

```
📦 Rate-Limited-API-Gateway
├── .github/workflows/ci.yml        # GitHub Actions CI/CD Workflow
├── app/
│   ├── main.py                     # Entry point, Flask setup
│   ├── auth.py                     # Token-based Auth (JWT)
│   ├── middleware.py               # Core rate-limiting logic
│   ├── rate_limit_config.py        # Switch between limiter algorithms
│   ├── limiter_factory.py          # Factory to initialize limiters
│   ├── logger.py                   # Logging support
│   ├── limiters/
│   │   ├── base.py                 # Base interface
│   │   ├── fixed_window.py         # Fixed Window implementation
│   │   ├── sliding_window.py       # Sliding Window implementation
│   │   └── token_bucket.py         # Token Bucket implementation
│   └── tests/
│       ├── test_fixed_window.py    # Unit test: Fixed Window
│       ├── test_sliding_window.py  # Unit test: Sliding Window
│       └── test_token_bucket.py    # Unit test: Token Bucket
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 Setup & Run

### 1. 🐳 Local Docker Run

```bash
docker-compose up --build
```

Visit Swagger UI at: [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

---

### 2. 🧪 Run Tests

```bash
pytest
```

> Includes test coverage for all rate limiting algorithms.

---

### 3. 🔁 Example API Usage (Swagger)

1. **POST** `/auth/token` → get JWT token  
2. Use **Authorize** button in Swagger UI to input the token  
3. Test endpoints like:
   - `GET /chat`
   - `GET /get-data`
   - `GET /search`

---

## ✅ CI/CD with GitHub Actions

Every push or PR to `main` triggers:

- Redis service boot-up
- Python & dependency installation
- Full `pytest` suite execution

> Example CI config in `.github/workflows/ci.yml`

---

## 📈 Rate Limiting Algorithms (Overview)

| Algorithm      | Use Case                               | Real-World Analogy                                |
|----------------|-----------------------------------------|---------------------------------------------------|
| Fixed Window   | Simple quotas per time slot             | 5 ATM withdrawals per day                         |
| Sliding Window | Fairer rolling windows for burst users  | Highway entry limit across last 60 seconds        |
| Token Bucket   | Bursty actions with refill              | API rate limit for ChatGPT image uploads (free)   |

---

## ✍️ Author

**Abanish Khatry**  
📧 [khatriavanish@gmail.com](mailto:khatriavanish@gmail.com)  
🐙 [GitHub Profile](https://github.com/abanishkhatry)

---