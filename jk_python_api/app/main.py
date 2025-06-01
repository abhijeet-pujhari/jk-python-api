from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import books, reviews, recommendations, auth
import aioredis
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI(title="JK Python Book API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(recommendations.router)

redis = None

@app.on_event("startup")
async def startup_event():
    global redis
    redis = await aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)

@app.on_event("shutdown")
async def shutdown_event():
    global redis
    if redis:
        await redis.close()
