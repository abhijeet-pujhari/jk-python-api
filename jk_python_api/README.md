# JK Python Book API

## Overview
A modular, async FastAPI application for book management, review aggregation, and AI-powered summaries using a local Llama3 model.

## Features
- Async PostgreSQL with SQLAlchemy
- JWT authentication
- Modular routers/services
- Llama3 (Ollama) integration for summaries
- Unit test structure
- Docker support

## Setup
1. **Clone the repository**
2. **Install dependencies**
   ```sh
   python3 -m pip install -r requirements.txt
   ```
3. **Configure environment**
   - Copy `.env.example` to `.env` and set your DB and secret values.
4. **Run PostgreSQL** (locally or via Docker)
5. **Run database migrations** (if using Alembic)
6. **Start the FastAPI app**
   ```sh
   uvicorn app.main:app --reload
   ```
7. **(Optional) Start Ollama/Llama3 model locally**

## API Usage
- Visit `/docs` for Swagger UI and try endpoints.
- Use `/auth/token` to get a JWT token for protected endpoints.

## User Registration
- Register a new user at `/auth/register` with a username and password.
- Login at `/auth/token` to receive a JWT for authenticated requests.

## Caching
- Book recommendations are cached in Redis for 5 minutes.
- Start Redis locally: `docker run -p 6379:6379 redis`

## SageMaker Integration
- To use AWS SageMaker for AI, set the `SAGEMAKER_ENDPOINT` environment variable and use the `services/sagemaker.py` utility.

## Testing
```sh
pytest
```

## Docker
1. Build: `docker build -t jk-python-api .`
2. Run: `docker run -p 8000:8000 --env-file .env jk-python-api`

## Deployment
- See comments in Dockerfile for cloud deployment.

## Advanced Deployment & CI/CD
- Use GitHub Actions or GitLab CI for automated testing and Docker image builds.
- Deploy to AWS ECS, EC2, or Lambda with RDS for PostgreSQL.
- Use AWS Secrets Manager for secret management.
- (Optional) Use AWS ElastiCache for caching recommendations.

## Security Notes
- All endpoints require JWT authentication except /auth/token.
- Use HTTPS in production.
- Use strong secrets and rotate regularly.

## API Documentation
- Interactive docs available at `/docs` (Swagger UI) and `/redoc`.

## Notes
- User authentication is stubbed (no user table yet).
- Llama3 integration expects Ollama running locally.
