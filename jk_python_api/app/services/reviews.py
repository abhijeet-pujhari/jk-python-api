from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import models, schemas
from typing import List, Optional

# Reviews service logic

async def get_reviews_for_book(db: AsyncSession, book_id: int) -> List[models.Review]:
    """
    Get all reviews for a book.
    """
    result = await db.execute(select(models.Review).where(models.Review.book_id == book_id))
    return result.scalars().all()

async def create_review(db: AsyncSession, book_id: int, review: schemas.ReviewCreate) -> models.Review:
    """
    Create a review for a book.
    """
    db_review = models.Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_review_summary(db: AsyncSession, book_id: int):
    """
    Get average rating and review count for a book.
    """
    try:
        reviews = await get_reviews_for_book(db, book_id)
        if not reviews:
            return {"average_rating": None, "review_count": 0}
        avg_rating = sum([r.rating for r in reviews]) / len(reviews)
        return {"average_rating": avg_rating, "review_count": len(reviews)}
    except Exception:
        return {"average_rating": None, "review_count": 0}
