# Recommendations service logic

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import models
from typing import List
import json
from app.main import redis

async def get_recommendations(db: AsyncSession, genre: str = None, min_rating: float = 0) -> List[models.Book]:
    """
    Recommend books by genre and minimum average rating, with Redis caching.
    """
    cache_key = f"recommendations:{genre}:{min_rating}"
    if redis:
        cached = await redis.get(cache_key)
        if cached:
            # Deserialize list of dicts to Book objects if needed
            books_data = json.loads(cached)
            # This assumes BookRead schema for serialization
            from app.db.schemas import BookRead
            return [BookRead(**b) for b in books_data]
    # ...existing recommendation logic...
    query = select(models.Book)
    if genre:
        query = query.where(models.Book.genre == genre)
    result = await db.execute(query)
    books = result.scalars().all()
    recommended = []
    for book in books:
        if book.reviews:
            avg_rating = sum([r.rating for r in book.reviews]) / len(book.reviews)
            if avg_rating >= min_rating:
                recommended.append(book)
        elif min_rating == 0:
            recommended.append(book)
    # Cache the result
    if redis:
        from app.db.schemas import BookRead
        await redis.set(cache_key, json.dumps([BookRead.from_orm(b).dict() for b in recommended]), ex=300)
    return recommended
