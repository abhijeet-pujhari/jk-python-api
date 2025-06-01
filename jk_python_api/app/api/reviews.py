from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db import schemas
from app.db.session import get_db
from app.services import reviews as review_service
from app.core.auth import get_current_user

router = APIRouter(prefix="/books/{book_id}/reviews", tags=["reviews"])

@router.post("/", response_model=schemas.ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(book_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await review_service.create_review(db, book_id, review)

@router.get("/", response_model=List[schemas.ReviewRead])
async def read_reviews(book_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await review_service.get_reviews_for_book(db, book_id)

@router.get("/summary")
async def get_review_summary(book_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    from app.services import reviews as review_service
    return await review_service.get_review_summary(db, book_id)
